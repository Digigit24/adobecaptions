# Troubleshooting Guide

Quick solutions to common issues with the Adobe Premiere AI Captioning Tool.

---

## Installation Issues

### FFmpeg Not Found

**Error:**
```
ERROR: FFmpeg not found!
Please install FFmpeg and add it to PATH
```

**Solutions:**

1. **Check if FFmpeg is installed:**
   ```bash
   ffmpeg -version
   ```

2. **If not installed, install it:**
   - Using Chocolatey: `choco install ffmpeg`
   - Or download manually from: https://ffmpeg.org/download.html

3. **Add FFmpeg to PATH:**
   - Windows Search → "Environment Variables"
   - Edit System PATH
   - Add FFmpeg bin folder (e.g., `C:\ffmpeg\bin`)
   - **Restart Command Prompt**

4. **Verify:**
   ```bash
   where ffmpeg
   ```

---

### faster-whisper Not Installed

**Error:**
```
ERROR: faster-whisper not installed!
Run: pip install faster-whisper
```

**Solutions:**

1. **Install the package:**
   ```bash
   pip install faster-whisper
   ```

2. **If installation fails:**
   ```bash
   # Update pip first
   pip install --upgrade pip

   # Then try again
   pip install faster-whisper
   ```

3. **Alternative (if faster-whisper doesn't work):**
   ```bash
   pip install openai-whisper
   ```
   Then modify `caption_tool.py` to use `whisper` instead of `faster_whisper`.

---

## Processing Issues

### First Run is Very Slow

**Symptom:** Tool seems to hang or takes 5-10 minutes on first run.

**Explanation:** This is **NORMAL**. The tool downloads Whisper model files on first run:
- `tiny`: ~75 MB
- `base`: ~150 MB
- `small`: ~500 MB
- `medium`: ~1.5 GB

**Solutions:**
- Wait patiently for the download to complete
- Subsequent runs will be much faster
- Check your internet connection

**To see download progress:**
- Look for console output showing model download
- Check `~/.cache/whisper/` folder size

---

### Audio Extraction Fails

**Error:**
```
ERROR: FFmpeg failed: [error details]
```

**Solutions:**

1. **Check video file:**
   - Play video in VLC to ensure it's not corrupted
   - Check if file path contains special characters
   - Try moving video to a simpler path (e.g., `C:\videos\test.mp4`)

2. **Check file format:**
   - Supported: MP4, MOV, AVI, MKV
   - If unusual format, convert to MP4 first

3. **Check permissions:**
   - Ensure you have read access to the video file
   - Ensure you have write access to the output folder

4. **Try manual FFmpeg command:**
   ```bash
   ffmpeg -i your_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 test.wav
   ```

---

### Transcription is Inaccurate

**Symptom:** Generated captions don't match the audio or have many errors.

**Solutions:**

1. **Use a larger model:**
   ```bash
   # Instead of default 'base', use 'small' or 'medium'
   python caption_tool.py video.mp4 -m small
   ```

2. **Specify language explicitly:**
   ```bash
   # Instead of auto-detect, force the language
   python caption_tool.py video.mp4 -l hi  # for Hindi
   python caption_tool.py video.mp4 -l mr  # for Marathi
   python caption_tool.py video.mp4 -l en  # for English
   ```

3. **Check audio quality:**
   - Heavy background noise reduces accuracy
   - Low volume audio causes issues
   - Multiple speakers talking over each other
   - Music louder than speech

4. **Audio preprocessing (advanced):**
   - Use audio editing software to clean up audio first
   - Boost volume if too quiet
   - Apply noise reduction
   - Export as clean WAV file

---

### Language Detection is Wrong

**Symptom:** Tool detects wrong language (e.g., detects Hindi as English).

**Solutions:**

1. **Force the correct language:**
   ```bash
   python caption_tool.py video.mp4 -l hi  # Force Hindi
   ```

2. **Check audio content:**
   - If video has mixed languages, choose the dominant language
   - If intro/outro is in different language, edit video first

3. **Language probability:**
   - Check the console output for "Probability: XX%"
   - Low probability (<70%) indicates uncertain detection
   - Use manual language specification for better results

---

## Adobe Premiere Pro Issues

### SRT File Won't Import

**Symptom:** Premiere Pro won't import the SRT file or shows errors.

**Solutions:**

1. **Check file encoding:**
   - SRT must be UTF-8 encoded (tool already does this)
   - Open SRT in Notepad and check for garbled text

2. **Check SRT format:**
   - Open SRT in text editor
   - Verify format is correct (see example below)

3. **Reimport:**
   - Delete the SRT from Premiere project
   - Restart Premiere Pro
   - Import again

**Correct SRT format:**
```
1
00:00:00,000 --> 00:00:02,500
Caption text here

2
00:00:02,500 --> 00:00:05,000
Next caption text

```

---

### Devanagari Text Looks Broken

**Symptom:** Hindi/Marathi captions show boxes, question marks, or broken characters.

**Solutions:**

1. **Use proper Devanagari font:**
   - Noto Sans Devanagari (recommended)
   - Hind
   - Mukta
   - Mangal

2. **In Premiere Pro:**
   - Select caption clip
   - Open "Essential Graphics" panel
   - Change font to a Devanagari-compatible font
   - Save as Caption Style preset for reuse

3. **Install missing fonts:**
   - Download from Google Fonts: https://fonts.google.com/?subset=devanagari
   - Install on Windows
   - Restart Premiere Pro

**Common fonts that DON'T work:**
- Arial (no Devanagari support)
- Times New Roman (no Devanagari support)
- Helvetica (no Devanagari support)

---

### Captions Are Out of Sync

**Symptom:** Captions appear too early or too late compared to audio.

**Possible Causes:**

1. **Original video has audio sync issues:**
   - Check if video itself has sync problems
   - Test by playing in VLC

2. **Variable frame rate video:**
   - Some screen recordings use VFR (variable frame rate)
   - Solution: Convert to constant frame rate first
   ```bash
   ffmpeg -i input.mp4 -r 30 -vcodec libx264 -acodec copy output.mp4
   ```

3. **Premiere Pro timeline settings:**
   - Ensure timeline frame rate matches video
   - Check audio sync in Premiere timeline

**Not the tool's fault if:**
- Timestamps in SRT are correct when opened in text editor
- Playing SRT in VLC shows correct sync
- Issue only appears in Premiere

---

## Performance Issues

### Processing is Too Slow

**Symptom:** Takes 10+ minutes to process a short video.

**Solutions:**

1. **Use smaller model:**
   ```bash
   python caption_tool.py video.mp4 -m tiny
   ```

2. **Process shorter clips:**
   - Split long videos into chunks
   - Process separately
   - Merge SRT files manually

3. **Close other applications:**
   - Free up CPU and RAM
   - Close browser, Discord, etc.

4. **GPU acceleration (advanced):**
   - If you have NVIDIA GPU with CUDA:
   ```bash
   python caption_tool.py video.mp4 --gpu
   ```
   - Requires CUDA Toolkit installation

**Expected processing times (base model, CPU):**
- 5 min video: ~2-3 minutes
- 30 min video: ~10-15 minutes
- 1 hour video: ~20-30 minutes

---

### Out of Memory Errors

**Symptom:** Python crashes with memory error.

**Solutions:**

1. **Use smaller model:**
   ```bash
   python caption_tool.py video.mp4 -m tiny
   ```

2. **Close other applications:**
   - Free up RAM
   - Check Task Manager for memory usage

3. **Process shorter videos:**
   - Split long videos first
   - Process in chunks

4. **Upgrade RAM:**
   - Minimum 8 GB recommended
   - 16 GB ideal for medium/large models

---

## File/Path Issues

### "File not found" Error

**Symptom:** Tool can't find the video file.

**Solutions:**

1. **Check file path:**
   - Use full absolute path
   - Avoid special characters in filename
   - Avoid spaces (or use quotes)

2. **Use quotes for paths with spaces:**
   ```bash
   python caption_tool.py "C:\My Videos\video.mp4"
   ```

3. **Move file to simpler location:**
   - Copy to `C:\videos\test.mp4`
   - Try again

---

### "Permission denied" Error

**Symptom:** Can't write SRT file or extract audio.

**Solutions:**

1. **Run as Administrator:**
   - Right-click Command Prompt
   - "Run as Administrator"

2. **Check folder permissions:**
   - Ensure write access to video folder
   - Try saving to a different folder using `-o`

3. **Check if file is open:**
   - Close video file in other programs
   - Close SRT file if open in Premiere

---

## Still Having Issues?

### Diagnostic Checklist

Run these commands to diagnose:

```bash
# Check Python
python --version

# Check pip
pip --version

# Check FFmpeg
ffmpeg -version

# Check faster-whisper
pip show faster-whisper

# List installed packages
pip list
```

### Get Detailed Error Info

Run the tool in verbose mode:

```bash
python caption_tool.py video.mp4 2>&1 | more
```

This shows detailed error messages.

### Report the Issue

When reporting issues to your dev team, include:

1. Full error message
2. Python version
3. Windows version
4. Video file format and size
5. Command you ran
6. Output of diagnostic checklist above

---

## Advanced Troubleshooting

### Clear Whisper Cache

If models are corrupted:

```bash
# Delete cache folder
rmdir /s %USERPROFILE%\.cache\whisper
```

Next run will redownload models.

### Reinstall Dependencies

If packages are corrupted:

```bash
pip uninstall faster-whisper
pip install --no-cache-dir faster-whisper
```

### Test FFmpeg Separately

Verify FFmpeg works:

```bash
ffmpeg -i test.mp4 -t 10 test.wav
```

This extracts first 10 seconds of audio.

---

## Contact Support

If none of these solutions work:

1. Check README.md for more details
2. Contact your internal dev team
3. Provide full diagnostic information (see above)

---

**Last Updated:** 2026-01-11
