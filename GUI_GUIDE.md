# GUI User Guide

**Adobe Premiere AI Captioning Tool - Graphical Interface**

Easy-to-use drag-and-drop interface for generating and editing video captions.

---

## Quick Start

### 1. Launch the GUI

Double-click `start_gui.bat`

Or from command line:
```bash
python caption_gui.py
```

### 2. Load a Video

**Option A: Drag & Drop**
- Drag your video file (MP4, MOV, AVI, MKV) onto the drop zone
- The file will load automatically

**Option B: Browse**
- Click "Browse Video" button
- Select your video file
- Click "Open"

### 3. Configure Settings

**Language:**
- Auto-detect (recommended)
- English
- Hindi
- Marathi

**Model:**
- tiny (fast) - Quick previews
- base (balanced) - **Recommended**
- small (better) - Better accuracy
- medium (best) - Maximum accuracy

### 4. Generate Captions

1. Click "▶ Generate Captions"
2. Wait for processing (progress bar shows status)
3. When complete, choose to open the editor

### 5. Edit Captions

The caption editor opens automatically after generation, or click "✏ Edit Captions"

**In the Editor:**
- View all captions with timestamps
- Click any field to edit:
  - Start time
  - End time
  - Caption text
- Delete captions with 🗑 button
- Add new captions with "➕ Add Caption"
- Save changes with "💾 Save"

### 6. Export to Premiere Pro

1. Click "📋 Export Info" to see import instructions
2. Import the SRT file in Premiere Pro (File → Import)
3. Style your captions

---

## Main Window Features

### Drop Zone
- **Large central area** for drag-and-drop
- Shows video info when loaded
- Green background when video is loaded

### Settings Panel
- **Language Selection**: Choose target language or auto-detect
- **Model Selection**: Balance speed vs accuracy

### Control Buttons
- **📁 Browse Video**: Open file picker
- **▶ Generate Captions**: Start processing
- **✏ Edit Captions**: Open caption editor
- **📋 Export Info**: Show Premiere Pro import instructions

### Progress Indicator
- Shows current processing step:
  - ⏳ Initializing...
  - 🎵 Extracting audio...
  - 🤖 Loading AI model...
  - 💬 Generating captions...
  - ✅ Complete!

### Status Bar
- Shows current status and loaded file name
- Displays errors if any occur

---

## Caption Editor Features

### Overview
The caption editor is a full-featured SRT editor with:
- View all captions in sequence
- Edit timestamps and text
- Add/delete captions
- Save changes

### Toolbar Buttons

**💾 Save**
- Save all changes to SRT file
- Prompts for confirmation if you close without saving

**↻ Reload**
- Reload from original file
- Discards unsaved changes (asks for confirmation)

**➕ Add Caption**
- Adds a new caption at the end
- Default 5-second duration
- Edit the text and timestamps after adding

**📋 Export to Premiere**
- Shows import instructions for Premiere Pro
- Lists recommended fonts for Hindi/Marathi

### Editing Captions

**Edit Start/End Times:**
- Click on timestamp field
- Type new time in format: `HH:MM:SS,mmm`
- Example: `00:01:23,500` = 1 minute, 23.5 seconds
- Press Tab or click elsewhere to save

**Edit Caption Text:**
- Click in text area
- Type or paste new text
- Supports multi-line captions
- Supports Unicode (Hindi/Marathi/etc)
- Auto-saves when you click elsewhere

**Delete Caption:**
- Click 🗑 button next to caption
- Confirms before deleting
- Renumbers remaining captions automatically

**Add Caption:**
- Click "➕ Add Caption" button
- New caption appears at bottom
- Edit the text and timestamps
- Click "💾 Save" when done

### Keyboard Shortcuts

- **Mouse Wheel**: Scroll through captions
- **Tab**: Move to next field
- **Shift+Tab**: Move to previous field

### Caption Format

Each caption has:
1. **Index**: Sequential number (auto-updated)
2. **Start Time**: When caption appears (HH:MM:SS,mmm)
3. **End Time**: When caption disappears (HH:MM:SS,mmm)
4. **Text**: Caption content (can be multi-line)

### Tips for Editing

**Fixing Spelling Errors:**
1. Locate the caption with error
2. Click in text area
3. Correct the spelling
4. Click elsewhere to auto-save
5. Click "💾 Save" to save to file

**Adjusting Timing:**
1. Play video in separate player to find exact time
2. Edit start/end timestamps in editor
3. Save changes
4. Re-import in Premiere to test

**Splitting Long Captions:**
1. Note the timestamp where you want to split
2. Edit the first caption's end time
3. Click "➕ Add Caption"
4. Set new caption's start time (same as first's end time)
5. Cut/paste text into new caption
6. Save changes

**Merging Captions:**
1. Copy text from second caption
2. Paste into first caption
3. Update first caption's end time
4. Delete second caption
5. Save changes

---

## Processing Status Messages

### During Processing

| Message | Meaning |
|---------|---------|
| ⏳ Initializing... | Starting up the caption tool |
| ⏳ Checking FFmpeg... | Verifying FFmpeg is installed |
| 🎵 Extracting audio... | Converting video to audio (WAV) |
| 🤖 Loading AI model... | Loading Whisper AI model |
| 💬 Generating captions... | Creating SRT file |
| ✅ Captions generated successfully! | Complete! |

### Error Messages

| Message | Solution |
|---------|----------|
| FFmpeg Not Found | Install FFmpeg (see SETUP.md) |
| Failed to extract audio | Check video file isn't corrupted |
| Processing Error | Check console for details |

---

## Workflow Examples

### Example 1: Basic Workflow

1. Double-click `start_gui.bat`
2. Drag `my_video.mp4` into window
3. Leave settings as default (Auto-detect, base)
4. Click "▶ Generate Captions"
5. Wait ~2-3 minutes for 5-minute video
6. Click "Yes" to open editor
7. Review captions
8. Click "💾 Save"
9. Import SRT into Premiere Pro

### Example 2: Hindi Video with Editing

1. Launch GUI
2. Load Hindi video
3. Set language to "Hindi"
4. Set model to "small (better)" for accuracy
5. Click "▶ Generate Captions"
6. Wait for processing
7. Open editor
8. Fix any spelling errors in Devanagari
9. Adjust timestamps if needed
10. Click "💾 Save"
11. Import into Premiere
12. Use "Noto Sans Devanagari" font

### Example 3: Quick Preview

1. Launch GUI
2. Load video
3. Set model to "tiny (fast)"
4. Generate captions (very fast)
5. Review in editor
6. If quality is poor, regenerate with "base" or "small"

### Example 4: Batch Processing

For multiple videos:
1. Process first video
2. Don't close GUI
3. Load next video (drag or browse)
4. Generate captions
5. Edit and save
6. Repeat for all videos

---

## Tips & Tricks

### Speed Up Processing
- Use "tiny" model for quick previews
- Process shorter clips (split long videos first)
- Close other applications to free up CPU

### Improve Accuracy
- Use "small" or "medium" model
- Specify language instead of auto-detect
- Ensure clean audio (minimal background noise)

### Editing Efficiently
- Use Tab key to navigate fields quickly
- Edit multiple captions before saving
- Use "↻ Reload" if you make mistakes

### Working with Hindi/Marathi
- The editor supports Devanagari input
- Copy/paste from other sources works
- Make sure your system has Devanagari fonts installed
- Test in Premiere with "Noto Sans Devanagari" font

### Handling Long Videos
- Split video into chunks first (e.g., 10-minute segments)
- Process each chunk separately
- Merge SRT files manually if needed
- Or use "medium" model and wait longer

---

## Keyboard Navigation

In main window:
- **Alt+B**: Browse for video (if supported)
- **Alt+G**: Generate captions (if video loaded)

In editor:
- **Mouse Wheel**: Scroll through captions
- **Tab**: Next field
- **Shift+Tab**: Previous field
- **Ctrl+S**: Save (if implemented)

---

## Troubleshooting GUI

### GUI Won't Start

**Error: Python not found**
- Install Python 3.11.9
- Make sure "Add to PATH" was checked during install

**Error: No module named 'tkinterdnd2'**
- Run: `pip install tkinterdnd2`
- Or: `pip install -r requirements.txt`

**Error: No module named 'caption_tool'**
- Make sure `caption_tool.py` is in the same folder
- Don't move files around

### GUI is Slow or Freezes

**During processing:**
- This is normal! Processing takes time
- Progress bar shows it's working
- Don't close the window

**When scrolling captions:**
- Normal for 100+ captions
- Editor loads all at once
- Close and reopen editor if it freezes

### Drag & Drop Doesn't Work

**Solutions:**
1. Use "Browse" button instead
2. Make sure file is a valid video format
3. Try running as Administrator
4. Check file isn't in use by another program

### Editor Won't Open

**Check:**
- SRT file exists in same folder as video
- File isn't corrupted
- You have read/write permissions

### Can't Save Edits

**Check:**
- You have write permission to folder
- File isn't open in another program
- Disk isn't full

---

## Advanced Features

### Manual SRT Editing

You can also edit SRT files manually in any text editor:

```
1
00:00:00,000 --> 00:00:02,500
First caption text

2
00:00:02,500 --> 00:00:05,000
Second caption text
```

Then reload in GUI editor to verify format.

### Custom Output Location

For now, SRT is saved next to video file. To save elsewhere:
1. Generate captions normally
2. Use File Explorer to move SRT file
3. In editor, "File → Save As" (if implemented)

### Re-processing

To regenerate captions:
1. Load the same video again
2. GUI will ask if you want to overwrite
3. Click "Yes" to regenerate
4. Old SRT is replaced

---

## Comparison: GUI vs Command Line

| Feature | GUI | Command Line |
|---------|-----|--------------|
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual feedback | ✅ Progress bar | ❌ Text only |
| Caption editor | ✅ Built-in | ❌ Use external |
| Batch processing | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Automation | ❌ Manual | ✅ Scriptable |
| Speed | Same | Same |

**Use GUI when:**
- You want visual interface
- You need to edit captions
- You're processing one video at a time
- You prefer drag-and-drop

**Use Command Line when:**
- You're processing many videos
- You want to automate with scripts
- You're comfortable with terminal
- You need advanced options

---

## FAQ

**Q: Can I run multiple GUI instances?**
A: Yes, but each processes one video at a time.

**Q: Can I edit captions while generating?**
A: No, wait for generation to complete first.

**Q: Can I cancel processing?**
A: Close the GUI window (may leave temp files).

**Q: Where are temp files stored?**
A: Same folder as video (`.temp.wav` files). Deleted after processing.

**Q: Can I use GPU acceleration in GUI?**
A: Not in GUI. Use command line with `--gpu` flag.

**Q: Does the editor auto-save?**
A: No, click "💾 Save" to save changes to file.

**Q: Can I undo edits?**
A: Use "↻ Reload" to discard unsaved changes.

**Q: How do I close the editor?**
A: Click X button. You'll be prompted to save if modified.

**Q: Can I have multiple editor windows open?**
A: Yes, one per SRT file.

---

## Getting Help

1. Check this guide
2. See TROUBLESHOOTING.md
3. See README.md for general info
4. Contact your internal dev team

---

**Enjoy the GUI! 🎬**

Last updated: 2026-01-11
