# Quick Setup Guide

Follow these steps to get the Adobe Premiere AI Captioning Tool running on your Windows machine.

## Prerequisites Checklist

- [ ] Windows 10 or Windows 11
- [ ] Python 3.11.9 installed
- [ ] FFmpeg installed
- [ ] Internet connection (for first run only)

---

## Step-by-Step Setup

### 1. Install FFmpeg

**Option A: Using Chocolatey (Easiest)**

1. Open PowerShell as Administrator
2. Install Chocolatey if not already installed:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Install FFmpeg:
   ```powershell
   choco install ffmpeg
   ```

**Option B: Manual Installation**

1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Download the "ffmpeg-release-essentials.zip" file
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Under System Variables, select "Path" → Edit
   - Click "New" → Add `C:\ffmpeg\bin`
   - Click OK on all dialogs
5. Restart Command Prompt

**Verify FFmpeg:**
```bash
ffmpeg -version
```

### 2. Install Python Dependencies

1. Open Command Prompt
2. Navigate to this folder:
   ```bash
   cd path\to\adobecaptions
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Note:** First run will download Whisper models (~150MB). This is normal.

### 3. Test the Tool

**Option A: GUI Mode (Recommended)**

1. Double-click `start_gui.bat`
2. Drag a test video file (MP4 or MOV) into the window
3. Click "Generate Captions"
4. Wait for processing
5. Edit captions in the built-in editor
6. Save and check the `.srt` file

**Option B: Command Line Mode**

1. Get a test video file (MP4 or MOV)
2. Drag and drop it onto `caption_video.bat`
3. Wait for processing
4. Check for the `.srt` file in the same folder

---

## Troubleshooting

### "FFmpeg not found"
- Make sure FFmpeg is in your PATH
- Restart Command Prompt after adding to PATH
- Test with: `ffmpeg -version`

### "pip not found"
- Reinstall Python 3.11.9
- Make sure "Add Python to PATH" is checked during installation

### "faster-whisper not installed"
- Run: `pip install faster-whisper`
- If it fails, try: `pip install --upgrade pip` first

### First run is very slow
- This is normal! The tool downloads model files on first run
- Subsequent runs will be much faster
- You can use `-m tiny` for faster processing (less accurate)

---

## Quick Reference

### Basic Commands

```bash
# Auto-detect language
python caption_tool.py video.mp4

# Force Hindi
python caption_tool.py video.mp4 -l hi

# Force Marathi
python caption_tool.py video.mp4 -l mr

# Use better model
python caption_tool.py video.mp4 -m small
```

### Model Sizes

- `tiny` - Fastest, least accurate (~75 MB)
- `base` - **Recommended** - Balanced (~150 MB)
- `small` - Better accuracy (~500 MB)
- `medium` - Best accuracy, slowest (~1.5 GB)

---

## Next Steps

1. Read the full README.md for detailed usage
2. Test with a short video first
3. Import the SRT into Premiere Pro
4. Set up your Caption Style presets
5. Use recommended fonts for Hindi/Marathi

---

## Support

For issues, check the Troubleshooting section in README.md or contact your internal dev team.
