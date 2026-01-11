#!/usr/bin/env python3
"""
Adobe Premiere AI Captioning Tool - Web Server
Simple Flask server for web-based interface
"""

import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
import threading
import time
import json

from caption_tool import CaptionTool

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Processing status storage
processing_status = {}
processing_lock = threading.Lock()


def update_status(job_id, status, message, progress=0):
    """Update processing status"""
    with processing_lock:
        processing_status[job_id] = {
            'status': status,
            'message': message,
            'progress': progress,
            'timestamp': time.time()
        }


def process_video_background(job_id, video_path, language, model_name, max_words=15):
    """Process video in background thread"""
    try:
        update_status(job_id, 'processing', 'Initializing...', 10)

        # Create caption tool
        caption_tool = CaptionTool(model_size=model_name, device='cpu')

        # Check FFmpeg
        update_status(job_id, 'processing', 'Checking FFmpeg...', 15)
        if not caption_tool.check_ffmpeg():
            update_status(job_id, 'error', 'FFmpeg not found! Please install FFmpeg.', 0)
            return

        # Extract audio
        update_status(job_id, 'processing', 'Extracting audio...', 25)
        video_path = Path(video_path)
        temp_audio = video_path.with_suffix('.temp.wav')

        if not caption_tool.extract_audio(video_path, temp_audio):
            update_status(job_id, 'error', 'Failed to extract audio', 0)
            return

        # Transcribe
        update_status(job_id, 'processing', 'Loading AI model...', 50)
        segments, detected_lang = caption_tool.transcribe_audio(temp_audio, language)

        update_status(job_id, 'processing', 'Generating captions...', 80)

        # Generate SRT
        output_srt = OUTPUT_FOLDER / f"{video_path.stem}.srt"
        caption_tool.generate_srt(segments, output_srt, max_words=max_words)

        # Cleanup
        if temp_audio.exists():
            temp_audio.unlink()

        # Success
        update_status(job_id, 'complete', f'Complete! Detected language: {detected_lang}', 100)

        # Store output file info
        with processing_lock:
            processing_status[job_id]['output_file'] = str(output_srt)
            processing_status[job_id]['detected_language'] = detected_lang

    except Exception as e:
        update_status(job_id, 'error', f'Error: {str(e)}', 0)
    finally:
        # Cleanup
        try:
            if temp_audio.exists():
                temp_audio.unlink()
        except:
            pass


@app.route('/')
def index():
    """Serve the main HTML page"""
    html_file = Path(__file__).parent / 'web_interface.html'
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "Error: web_interface.html not found!", 404


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'video' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Get parameters
    language = request.form.get('language', 'auto')
    if language == 'auto':
        language = None

    model_name = request.form.get('model', 'base')
    max_words = int(request.form.get('max_words', '15'))

    # Save file
    filename = secure_filename(file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)

    # Create job ID
    job_id = f"{int(time.time())}_{filename}"

    # Start processing in background
    update_status(job_id, 'queued', 'Starting...', 0)

    thread = threading.Thread(
        target=process_video_background,
        args=(job_id, filepath, language, model_name, max_words),
        daemon=True
    )
    thread.start()

    return jsonify({
        'job_id': job_id,
        'filename': filename,
        'message': 'Processing started'
    })


@app.route('/status/<job_id>')
def get_status(job_id):
    """Get processing status"""
    with processing_lock:
        if job_id in processing_status:
            return jsonify(processing_status[job_id])
        else:
            return jsonify({'error': 'Job not found'}), 404


@app.route('/captions/<job_id>')
def get_captions(job_id):
    """Get generated captions"""
    with processing_lock:
        if job_id not in processing_status:
            return jsonify({'error': 'Job not found'}), 404

        status = processing_status[job_id]

        if status['status'] != 'complete':
            return jsonify({'error': 'Processing not complete'}), 400

        output_file = Path(status['output_file'])

        if not output_file.exists():
            return jsonify({'error': 'Caption file not found'}), 404

        # Parse SRT
        captions = []
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by double newline
        import re
        blocks = re.split(r'\n\n+', content.strip())

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])

                    start, end = timestamp.split(' --> ')

                    captions.append({
                        'index': index,
                        'start': start.strip(),
                        'end': end.strip(),
                        'text': text.strip()
                    })
                except:
                    continue

        return jsonify({
            'captions': captions,
            'filename': output_file.name,
            'detected_language': status.get('detected_language', 'unknown')
        })


@app.route('/save/<job_id>', methods=['POST'])
def save_captions(job_id):
    """Save edited captions"""
    with processing_lock:
        if job_id not in processing_status:
            return jsonify({'error': 'Job not found'}), 404

        status = processing_status[job_id]
        output_file = Path(status['output_file'])

    # Get captions from request
    captions = request.json.get('captions', [])

    # Save to SRT
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, caption in enumerate(captions, start=1):
            f.write(f"{i}\n")
            f.write(f"{caption['start']} --> {caption['end']}\n")
            f.write(f"{caption['text']}\n")
            f.write("\n")

    return jsonify({'message': 'Saved successfully', 'filename': output_file.name})


@app.route('/download/<job_id>')
def download_captions(job_id):
    """Download SRT file"""
    with processing_lock:
        if job_id not in processing_status:
            return "Job not found", 404

        status = processing_status[job_id]
        output_file = Path(status['output_file'])

    if not output_file.exists():
        return "File not found", 404

    return send_from_directory(
        output_file.parent,
        output_file.name,
        as_attachment=True
    )


def main():
    """Start the web server"""
    print("=" * 60)
    print("Adobe Premiere AI Captioning Tool - Web Interface")
    print("=" * 60)
    print("\nStarting server...")
    print("\n🌐 Open in your browser:")
    print("   http://localhost:5000")
    print("\n📝 To stop the server, press Ctrl+C")
    print("=" * 60)
    print()

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)


if __name__ == '__main__':
    main()
