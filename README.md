# Adobe Premiere AI Captioning Tool

**Simple, fast, reliable AI-powered captioning for Adobe Premiere Pro on Windows**

Internal-use tool for generating SRT captions from video files with support for English, Hindi, and Marathi (with proper Devanagari rendering).

---

## Features

- ✅ **Auto-extracts audio** from MP4/MOV/AVI/MKV files using FFmpeg
- ✅ **AI transcription** using OpenAI Whisper (local, no API required)
- ✅ **Auto-detects language** (English, Hindi, Marathi)
- ✅ **Sentence-level captions** (not word-by-word)
- ✅ **UTF-8 SRT output** compatible with Adobe Premiere Pro
- ✅ **Proper Devanagari rendering** for Hindi and Marathi
- ✅ **Clean timestamps** (no overflow issues)
- ✅ **One-click execution** via batch files
- ✅ **Progress logging** and error handling
- ✅ **GUI Application** with drag-and-drop and caption editor
- ✅ **Visual caption editor** for fixing spellings and timing

---

## 🆕 GUI Mode (Recommended for Beginners)

**NEW! Easy-to-use graphical interface with drag-and-drop and built-in caption editor.**

### Launch GUI

Double-click `start_gui.bat` or run:
```bash
python caption_gui.py
```

### Features
- 🎯 **Drag & drop** video files
- 📊 **Visual progress** tracking
- ✏️ **Built-in caption editor** with spelling correction
- 🎨 **Edit timestamps** and caption text
- 💾 **Save directly** to SRT
- 📋 **Export info** for Premiere Pro

### Quick Workflow
1. Double-click `start_gui.bat`
2. Drag video file into window
3. Click "Generate Captions"
4. Edit captions in built-in editor
5. Save and import to Premiere Pro

**See [GUI_GUIDE.md](GUI_GUIDE.md) for detailed GUI documentation.**

---

## Quick Start

### 1. Prerequisites

- **Windows 10/11**
- **Python 3.11.9** (already installed)
- **FFmpeg** (see installation below)

### 2. Install FFmpeg

**Option A: Using Chocolatey (recommended)**
```bash
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH
4. Restart command prompt

**Verify installation:**
```bash
ffmpeg -version
```

### 3. Install Python Dependencies

Open Command Prompt in this folder and run:

```bash
pip install -r requirements.txt
```

This installs `faster-whisper`, an optimized implementation of OpenAI Whisper.

**First run will auto-download Whisper model files (~150MB for base model)**

---

## Usage

### Simple Mode (Drag & Drop)

1. **Drag and drop** your video file onto `caption_video.bat`
2. Wait for processing
3. Find the `.srt` file in the same folder as your video

### Advanced Mode (More Options)

1. **Drag and drop** your video file onto `caption_video_advanced.bat`
2. Select language (or auto-detect)
3. Select model size
4. Wait for processing

### Command Line Mode

```bash
# Basic usage (auto-detect language)
python caption_tool.py video.mp4

# Specify language
python caption_tool.py video.mp4 -l hi

# Specify output file
python caption_tool.py video.mp4 -o captions.srt

# Use larger model for better accuracy
python caption_tool.py video.mp4 -m small

# All options
python caption_tool.py video.mp4 -l mr -m medium -o output.srt
```

### Available Options

| Option | Description | Values |
|--------|-------------|--------|
| `-l, --language` | Force specific language | `en`, `hi`, `mr` (default: auto-detect) |
| `-m, --model` | Whisper model size | `tiny`, `base`, `small`, `medium`, `large-v2` (default: `base`) |
| `-o, --output` | Output SRT file path | Any valid path (default: same as video) |
| `--gpu` | Use GPU acceleration | Requires CUDA (advanced users) |

### Model Selection Guide

| Model | Speed | Accuracy | Size | Recommended For |
|-------|-------|----------|------|-----------------|
| `tiny` | ⚡⚡⚡⚡ | ⭐⭐ | ~75 MB | Quick previews |
| `base` | ⚡⚡⚡ | ⭐⭐⭐ | ~150 MB | **Default - balanced** |
| `small` | ⚡⚡ | ⭐⭐⭐⭐ | ~500 MB | Better accuracy |
| `medium` | ⚡ | ⭐⭐⭐⭐⭐ | ~1.5 GB | Maximum accuracy |

---

## Importing Captions into Adobe Premiere Pro

### Step 1: Import SRT File

1. Open your Premiere Pro project
2. **File → Import** or press `Ctrl+I`
3. Select the generated `.srt` file
4. Click **Import**

### Step 2: Add to Timeline

1. Drag the `.srt` file from **Project Panel** to your **Timeline**
2. Place it on a track above your video
3. Captions will appear as a purple/magenta clip

### Step 3: Style Your Captions

**Method A: Using Caption Style Presets**
1. Select the caption clip on timeline
2. Open **Essential Graphics** panel
3. Click **Edit** tab
4. Modify:
   - Font (see recommended fonts below)
   - Size
   - Color
   - Background
   - Position
5. Right-click style → **Save Style** to reuse

**Method B: Using Text Panel**
1. Window → **Captions and Graphics**
2. Select caption clip
3. Modify styling in the **Text** panel

### Recommended Fonts for Hindi & Marathi

For proper Devanagari rendering, use these fonts (pre-installed on Windows 10/11):

1. **Noto Sans Devanagari** (recommended - best rendering)
2. **Hind** (clean, modern)
3. **Mukta** (lightweight)
4. **Mangal** (Windows default)

If fonts are missing, download from [Google Fonts](https://fonts.google.com/?subset=devanagari).

---

## Folder Structure

```
adobecaptions/
│
├── caption_tool.py              # Main Python script (command-line)
├── caption_gui.py               # GUI application (NEW!)
├── start_gui.bat                # Launch GUI (double-click this!)
├── caption_video.bat            # Simple drag-and-drop launcher (CLI)
├── caption_video_advanced.bat   # Advanced launcher with options (CLI)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── GUI_GUIDE.md                 # GUI user guide (NEW!)
├── SETUP.md                     # Quick setup guide
├── TROUBLESHOOTING.md           # Troubleshooting guide
├── LICENSE.txt                  # License information
│
├── examples/                    # Example files
│   └── sample_output.srt
│
└── .gitignore                   # Git ignore file
```

---

## Troubleshooting

### FFmpeg not found
**Error:** `ERROR: FFmpeg not found!`

**Solution:**
1. Install FFmpeg (see step 2 above)
2. Restart Command Prompt
3. Verify with `ffmpeg -version`

### faster-whisper not installed
**Error:** `ERROR: faster-whisper not installed!`

**Solution:**
```bash
pip install faster-whisper
```

### First run is slow
**This is normal!** The first run downloads Whisper model files (~150MB for base model). Subsequent runs will be much faster.

### Audio extraction fails
**Check:** Is your video file corrupted? Try playing it in VLC first.

### Transcription is inaccurate
**Solutions:**
- Use a larger model: `-m small` or `-m medium`
- Ensure audio is clear (no heavy background noise)
- Manually specify language: `-l hi` instead of auto-detect

### Devanagari text looks broken in Premiere
**Solution:** Make sure you're using a proper Devanagari font (see recommended fonts above). Default fonts like Arial won't render Devanagari correctly.

### SRT timing is off
The tool uses Whisper's Voice Activity Detection (VAD) to align timing. If timing is still off:
- Ensure your video audio is synced properly
- Check if the original video has audio sync issues

---

## Performance Tips

### For Faster Processing
- Use `tiny` or `base` models
- Process shorter clips (split long videos first)
- Close other heavy applications

### For Better Accuracy
- Use `small` or `medium` models
- Ensure clear audio (reduce background noise)
- Specify language explicitly (`-l en/hi/mr`)

### GPU Acceleration (Advanced)
If you have an NVIDIA GPU with CUDA:

1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Install cuDNN
3. Use `--gpu` flag:
   ```bash
   python caption_tool.py video.mp4 --gpu
   ```

This can speed up processing by 5-10x.

---

## Supported File Formats

### Input Video Formats
- `.mp4` (recommended)
- `.mov`
- `.avi`
- `.mkv`
- Any format supported by FFmpeg

### Output Format
- `.srt` (SubRip) - UTF-8 encoded

---

## Batch Processing Multiple Videos

Create a batch script for multiple files:

```batch
@echo off
for %%F in (*.mp4) do (
    echo Processing %%F...
    python caption_tool.py "%%F"
)
echo All videos processed!
pause
```

Save as `batch_process.bat` and run in your video folder.

---

## Known Limitations

- **Not a Premiere extension** - operates independently
- **No real-time preview** - must import SRT after generation
- **CPU-based by default** - GPU requires CUDA setup
- **No built-in styling** - style captions inside Premiere
- **Single audio track** - doesn't handle multi-track audio

---

## Technical Details

### Audio Extraction
- **Codec:** PCM 16-bit
- **Sample Rate:** 16kHz (optimal for Whisper)
- **Channels:** Mono

### Whisper Processing
- **Implementation:** faster-whisper (CTranslate2 backend)
- **VAD:** Enabled with 500ms min silence duration
- **Beam Size:** 5
- **Compute Type:** int8 (CPU) / float16 (GPU)

### Caption Merging
- **Max Duration:** 5 seconds per caption
- **Max Characters:** 84 chars per line
- **Sentence Detection:** Splits on `.!?`

### SRT Format
- **Encoding:** UTF-8 with BOM support
- **Timestamp Format:** `HH:MM:SS,mmm`
- **No styling tags** - pure text

---

## Examples

### Example 1: Auto-detect Language
```bash
python caption_tool.py interview.mp4
# Output: interview.srt (auto-detects language)
```

### Example 2: Hindi Video
```bash
python caption_tool.py movie_scene.mp4 -l hi -m small
# Output: movie_scene.srt (Hindi, better accuracy)
```

### Example 3: Marathi with Custom Output
```bash
python caption_tool.py speech.mov -l mr -o marathi_captions.srt
# Output: marathi_captions.srt (Marathi)
```

### Example 4: Fast Preview
```bash
python caption_tool.py test.mp4 -m tiny
# Output: test.srt (fastest processing)
```

---

## FAQ

**Q: Do I need an OpenAI API key?**
A: No! This tool uses the open-source Whisper models locally.

**Q: Does it work offline?**
A: Yes, after the first run downloads the model files.

**Q: Can I use this for commercial projects?**
A: This is an internal tool. Check OpenAI Whisper license for commercial use.

**Q: What about other languages?**
A: Whisper supports 100+ languages. Modify `SUPPORTED_LANGUAGES` in `caption_tool.py` to add more.

**Q: Can I customize caption styling in the SRT?**
A: No. Style captions inside Premiere Pro using Caption Style presets. This keeps the workflow simple and flexible.

**Q: Why not build a Premiere extension?**
A: Extensions require CEP/UXP development and are slower to build. This standalone tool is simpler, faster to develop, and more reliable for internal use.

---

## Credits

- **OpenAI Whisper** - Speech recognition model
- **faster-whisper** - Optimized Whisper implementation
- **FFmpeg** - Audio extraction
- **Adobe Premiere Pro** - Video editing and caption styling

---

## License

Internal use only. Not for distribution.

---

## Support

For issues or questions, contact your internal dev team.

**Happy Captioning! 🎬**
