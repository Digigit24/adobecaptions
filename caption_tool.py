#!/usr/bin/env python3
"""
Adobe Premiere AI Captioning Tool
Simple, fast, reliable captioning for internal use
Supports English, Hindi, and Marathi with proper Devanagari rendering
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import timedelta
import re

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("ERROR: faster-whisper not installed!")
    print("Run: pip install faster-whisper")
    sys.exit(1)


class CaptionTool:
    """Main captioning tool class"""

    SUPPORTED_FORMATS = ['.mp4', '.mov', '.avi', '.mkv']
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'mr': 'Marathi',
        'hi-en': 'Hinglish (Hindi + English)',
        'mr-en': 'English + Marathi',
        'mixed': 'Mixed (All Languages)',
        'auto': 'Auto-detect'
    }

    def __init__(self, model_size='base', device='cpu'):
        """
        Initialize the captioning tool

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large-v2)
            device: 'cpu' or 'cuda'
        """
        self.model_size = model_size
        self.device = device
        self.model = None

    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def extract_audio(self, video_path, audio_path):
        """
        Extract audio from video using FFmpeg

        Args:
            video_path: Path to input video file
            audio_path: Path to output audio file (WAV)
        """
        print(f"[1/3] Extracting audio from {Path(video_path).name}...")

        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', '16000',  # 16kHz sample rate (optimal for Whisper)
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            str(audio_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            if result.returncode != 0:
                print(f"ERROR: FFmpeg failed: {result.stderr.decode('utf-8', errors='ignore')}")
                return False

            print(f"✓ Audio extracted successfully")
            return True

        except Exception as e:
            print(f"ERROR: Failed to extract audio: {e}")
            return False

    def load_model(self):
        """Load Whisper model"""
        if self.model is None:
            print(f"[2/3] Loading Whisper {self.model_size} model...")
            try:
                self.model = WhisperModel(
                    self.model_size,
                    device=self.device,
                    compute_type="int8" if self.device == "cpu" else "float16"
                )
                print("✓ Model loaded successfully")
            except Exception as e:
                print(f"ERROR: Failed to load model: {e}")
                sys.exit(1)

    def transcribe_audio(self, audio_path, language=None):
        """
        Transcribe audio using Whisper

        Args:
            audio_path: Path to audio file
            language: Language code ('en', 'hi', 'mr', 'hi-en', 'mr-en', 'mixed', 'auto') or None for auto-detect

        Returns:
            segments: List of transcription segments with timestamps
            detected_language: Detected language code
        """
        self.load_model()

        print(f"[3/3] Transcribing audio...")

        # Handle mixed language scenarios
        # For Hinglish, English+Marathi, or mixed languages, use None to let Whisper handle code-switching
        whisper_language = None
        if language in ['hi-en', 'mr-en', 'mixed', 'auto', None]:
            whisper_language = None
            print(f"    Language: {self.SUPPORTED_LANGUAGES.get(language, 'Auto-detect')} (multi-language mode)")
        else:
            whisper_language = language
            print(f"    Language: {self.SUPPORTED_LANGUAGES.get(language, language)}")

        try:
            segments, info = self.model.transcribe(
                str(audio_path),
                language=whisper_language,
                beam_size=5,
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(min_silence_duration_ms=500)
            )

            detected_language = info.language
            print(f"✓ Transcription complete")
            print(f"  Detected language: {self.SUPPORTED_LANGUAGES.get(detected_language, detected_language)}")
            print(f"  Probability: {info.language_probability:.2%}")

            # Convert generator to list
            segments_list = list(segments)

            return segments_list, detected_language

        except Exception as e:
            print(f"ERROR: Transcription failed: {e}")
            sys.exit(1)

    def format_timestamp(self, seconds):
        """
        Format timestamp for SRT format (HH:MM:SS,mmm)

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)

        # Ensure no overflow
        millis = min(millis, 999)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def merge_segments_into_sentences(self, segments, max_duration=5.0, max_chars=84, max_words=15):
        """
        Merge small segments into sentence-level captions

        Args:
            segments: List of word/phrase segments
            max_duration: Maximum duration for a single caption (seconds)
            max_chars: Maximum characters per caption line
            max_words: Maximum words per caption line

        Returns:
            List of merged sentence segments
        """
        merged = []
        current_text = ""
        current_start = None
        current_end = None

        for segment in segments:
            text = segment.text.strip()

            if not text:
                continue

            # Start new segment
            if current_start is None:
                current_start = segment.start
                current_text = text
                current_end = segment.end
                continue

            # Check if we should merge or create new segment
            potential_text = current_text + " " + text
            duration = segment.end - current_start
            word_count = len(potential_text.split())

            # Split if too long, too many chars, too many words, or sentence boundary
            should_split = (
                duration > max_duration or
                len(potential_text) > max_chars or
                word_count > max_words or
                (current_text and current_text[-1] in '.!?')
            )

            if should_split:
                # Save current segment
                merged.append({
                    'start': current_start,
                    'end': current_end,
                    'text': current_text
                })
                # Start new segment
                current_start = segment.start
                current_text = text
                current_end = segment.end
            else:
                # Merge with current segment
                current_text = potential_text
                current_end = segment.end

        # Don't forget the last segment
        if current_text:
            merged.append({
                'start': current_start,
                'end': current_end,
                'text': current_text
            })

        # Post-process: Split any captions that still exceed max_words
        # This handles cases where a single Whisper segment is already too long
        final_segments = []
        for segment in merged:
            words = segment['text'].split()
            if len(words) <= max_words:
                final_segments.append(segment)
            else:
                # Split this segment into multiple parts
                start_time = segment['start']
                end_time = segment['end']
                duration = end_time - start_time
                time_per_word = duration / len(words)

                # Split into chunks of max_words
                for i in range(0, len(words), max_words):
                    chunk_words = words[i:i + max_words]
                    chunk_start = start_time + (i * time_per_word)
                    chunk_end = start_time + ((i + len(chunk_words)) * time_per_word)

                    final_segments.append({
                        'start': chunk_start,
                        'end': chunk_end,
                        'text': ' '.join(chunk_words)
                    })

        return final_segments

    def generate_srt(self, segments, output_path, max_words=15):
        """
        Generate SRT file from transcription segments

        Args:
            segments: List of transcription segments
            output_path: Path to output SRT file
            max_words: Maximum words per caption (default: 15)
        """
        print(f"\n[4/4] Generating SRT file...")
        print(f"    Max words per caption: {max_words}")

        # Merge into sentence-level captions
        merged_segments = self.merge_segments_into_sentences(segments, max_words=max_words)

        print(f"    Total captions generated: {len(merged_segments)}")

        # Verify all captions respect max_words
        long_captions = [seg for seg in merged_segments if len(seg['text'].split()) > max_words]
        if long_captions:
            print(f"    Warning: {len(long_captions)} captions exceed max_words (should have been split)")
        else:
            print(f"    ✓ All captions respect max_words limit")

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(merged_segments, start=1):
                    # SRT format:
                    # 1
                    # 00:00:00,000 --> 00:00:02,000
                    # Caption text
                    # (blank line)

                    start_time = self.format_timestamp(segment['start'])
                    end_time = self.format_timestamp(segment['end'])
                    text = segment['text']

                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n")
                    f.write("\n")

            print(f"✓ SRT file created: {output_path}")
            print(f"\n{'='*60}")
            print(f"SUCCESS! Caption file ready for Adobe Premiere Pro")
            print(f"{'='*60}")
            print(f"Output: {output_path}")
            print(f"\nTo import in Premiere Pro:")
            print(f"1. File > Import > {Path(output_path).name}")
            print(f"2. Drag SRT to timeline")
            print(f"3. Style captions using Caption Style presets")
            print(f"\nRecommended fonts for Hindi/Marathi:")
            print(f"  - Noto Sans Devanagari")
            print(f"  - Hind")
            print(f"  - Mukta")

        except Exception as e:
            print(f"ERROR: Failed to write SRT file: {e}")
            sys.exit(1)

    def process_video(self, video_path, output_path=None, language=None):
        """
        Main processing pipeline

        Args:
            video_path: Path to input video file
            output_path: Path to output SRT file (optional)
            language: Language code or None for auto-detect
        """
        video_path = Path(video_path)

        # Validate input
        if not video_path.exists():
            print(f"ERROR: Video file not found: {video_path}")
            sys.exit(1)

        if video_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            print(f"WARNING: Unusual video format: {video_path.suffix}")
            print(f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")

        # Check FFmpeg
        if not self.check_ffmpeg():
            print("ERROR: FFmpeg not found!")
            print("Please install FFmpeg and add it to PATH")
            print("Download: https://ffmpeg.org/download.html")
            sys.exit(1)

        # Determine output path
        if output_path is None:
            output_path = video_path.with_suffix('.srt')
        else:
            output_path = Path(output_path)

        # Create temp audio file
        temp_audio = video_path.with_suffix('.temp.wav')

        try:
            print(f"\n{'='*60}")
            print(f"Adobe Premiere AI Captioning Tool")
            print(f"{'='*60}")
            print(f"Input:  {video_path.name}")
            print(f"Output: {output_path.name}")
            print(f"Model:  Whisper {self.model_size}")
            print(f"{'='*60}\n")

            # Step 1: Extract audio
            if not self.extract_audio(video_path, temp_audio):
                sys.exit(1)

            # Step 2 & 3: Transcribe
            segments, detected_lang = self.transcribe_audio(temp_audio, language)

            # Step 4: Generate SRT
            self.generate_srt(segments, output_path)

        finally:
            # Cleanup temp audio file
            if temp_audio.exists():
                try:
                    temp_audio.unlink()
                except Exception:
                    pass


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Adobe Premiere AI Captioning Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python caption_tool.py video.mp4
  python caption_tool.py video.mp4 -o captions.srt
  python caption_tool.py video.mp4 -l hi
  python caption_tool.py video.mp4 -m small

Supported languages:
  en - English
  hi - Hindi
  mr - Marathi

Model sizes (larger = more accurate but slower):
  tiny, base, small, medium, large-v2
        """
    )

    parser.add_argument(
        'video',
        help='Input video file (MP4, MOV, etc.)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output SRT file path (default: same as video with .srt extension)'
    )

    parser.add_argument(
        '-l', '--language',
        choices=['en', 'hi', 'mr'],
        help='Language code (default: auto-detect)'
    )

    parser.add_argument(
        '-m', '--model',
        choices=['tiny', 'base', 'small', 'medium', 'large-v2'],
        default='base',
        help='Whisper model size (default: base)'
    )

    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Use GPU acceleration (requires CUDA)'
    )

    args = parser.parse_args()

    # Create tool instance
    device = 'cuda' if args.gpu else 'cpu'
    tool = CaptionTool(model_size=args.model, device=device)

    # Process video
    tool.process_video(
        video_path=args.video,
        output_path=args.output,
        language=args.language
    )


if __name__ == '__main__':
    main()
