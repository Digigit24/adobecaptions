# Web Interface Guide

**Adobe Premiere AI Captioning Tool - Browser-Based Interface**

Use the captioning tool directly in your web browser with a beautiful, modern interface.

---

## Quick Start

### 1. Launch the Web Server

**Double-click `start_web.bat`**

Or from command line:
```bash
python web_server.py
```

### 2. Open in Browser

The server will start and display:
```
🌐 Open in your browser:
   http://localhost:5000
```

Open that URL in your browser (Chrome, Firefox, Edge, etc.)

### 3. Use the Interface

1. **Drag & drop** your video file
2. **Select settings** (language & accuracy)
3. Click **"Generate Captions"**
4. **Edit captions** in the browser
5. **Save and download** the SRT file

---

## Features

### 🎯 Drag & Drop Interface
- Drag video files directly into the browser
- Instant file validation
- File size display

### ⚙️ Settings Panel

**Language Selection:**
- Auto-detect (Recommended)
- English
- Hindi (हिंदी)
- Marathi (मराठी)

**Model Accuracy (NEW!):**
- **Tiny** - ⚡⚡⚡⚡ Fastest (Low Accuracy)
  - Best for: Quick previews, testing
  - Speed: ~30 seconds for 5-min video

- **Base** - ⚡⚡⚡ Balanced (Recommended)
  - Best for: Most videos, daily use
  - Speed: ~2-3 minutes for 5-min video
  - Accuracy: Good

- **Small** - ⚡⚡ Better Accuracy (Slower)
  - Best for: Important videos, presentations
  - Speed: ~5-7 minutes for 5-min video
  - Accuracy: Very good

- **Medium** - ⚡ Best Accuracy (Slowest)
  - Best for: Professional work, final versions
  - Speed: ~10-15 minutes for 5-min video
  - Accuracy: Excellent

### 📊 Real-Time Progress
- Visual progress bar
- Status messages:
  - ⏳ Initializing...
  - 🎵 Extracting audio...
  - 🤖 Loading AI model...
  - 💬 Generating captions...
  - ✅ Complete!

### ✏️ Built-in Caption Editor
- View all captions in browser
- Edit caption text (fix spellings)
- Edit timestamps (start/end times)
- Delete unwanted captions
- Live caption count
- Detected language display

### 💾 Save & Download
- Save edits directly in browser
- Download SRT file
- Auto-saves to server

---

## Step-by-Step Workflow

### 1. Start the Server
```
Double-click: start_web.bat
```

Server starts and opens on port 5000.

### 2. Open Browser
```
Navigate to: http://localhost:5000
```

You'll see the web interface with purple gradient design.

### 3. Configure Settings

**Choose Language:**
- For mixed content: Auto-detect
- For specific language: Select English/Hindi/Marathi

**Choose Model Accuracy:**
- First time / Testing: Tiny (fastest)
- Regular use: Base (recommended)
- Important videos: Small
- Professional work: Medium

### 4. Load Video

**Option A: Drag & Drop**
- Drag video file from File Explorer
- Drop onto the drop zone
- Green checkmark appears

**Option B: Click to Browse**
- Click the drop zone
- Browse for video file
- Select and open

### 5. Generate Captions

Click **"▶️ Generate Captions"**

Watch the progress:
- Progress bar fills up
- Status messages update
- Typical time: 2-3 minutes for 5-minute video

### 6. Edit Captions

When complete, captions appear in editor:

```
#1  | 00:00:00,000 → 00:00:02,500 |
    | Welcome to the tutorial    |

#2  | 00:00:02,500 → 00:00:05,000 |
    | Today we'll learn...       |
```

**Edit Text:**
- Click in text area
- Fix spelling errors
- Modify wording
- Add line breaks

**Edit Timestamps:**
- Click on start/end time
- Format: HH:MM:SS,mmm
- Example: 00:01:23,500

**Delete Caption:**
- Click 🗑️ Delete button
- Confirm deletion

### 7. Save Changes

Click **"💾 Save Changes"** to save edits to server.

Status bar shows: "✅ Saved successfully"

### 8. Download SRT

Click **"💾 Download SRT"** to download the file.

File downloads to your Downloads folder.

### 9. Import to Premiere Pro

1. File → Import
2. Select downloaded SRT file
3. Drag to timeline
4. Style captions

---

## Interface Layout

### Top Section
```
┌─────────────────────────────────────┐
│  🎬 Adobe Premiere AI Captioning    │
│  Generate and edit AI captions      │
├─────────────────────────────────────┤
│  ⚙️ Settings                        │
│  Language: [Auto-detect ▼]          │
│  Model:    [Base - Balanced ▼]      │
├─────────────────────────────────────┤
│         🎥                          │
│   Drag & Drop Video Here            │
│   or click to browse                │
└─────────────────────────────────────┘
```

### Progress Section
```
┌─────────────────────────────────────┐
│ ████████░░░░░░░░░░ 40%             │
│ 🤖 Loading AI model...             │
└─────────────────────────────────────┘
```

### Editor Section
```
┌─────────────────────────────────────┐
│ ✏️ Caption Editor | 50 captions    │
│ [💾 Save Changes]                   │
├─────────────────────────────────────┤
│ #1 | 00:00:00,000 → 00:00:02,500   │
│    | [Caption text here...]         │
│    | [🗑️ Delete]                    │
├─────────────────────────────────────┤
│ #2 | 00:00:02,500 → 00:00:05,000   │
│    | [Caption text here...]         │
│    | [🗑️ Delete]                    │
└─────────────────────────────────────┘
```

### Bottom Section
```
┌─────────────────────────────────────┐
│ [📁 Browse] [▶️ Generate] [💾 Download] │
├─────────────────────────────────────┤
│ Status: ✅ Captions generated!      │
└─────────────────────────────────────┘
```

---

## Model Accuracy Comparison

| Model | Speed | Accuracy | Best For | File Size |
|-------|-------|----------|----------|-----------|
| Tiny | ⚡⚡⚡⚡ | ⭐⭐ | Quick tests | 75 MB |
| Base | ⚡⚡⚡ | ⭐⭐⭐ | Daily use | 150 MB |
| Small | ⚡⚡ | ⭐⭐⭐⭐ | Important videos | 500 MB |
| Medium | ⚡ | ⭐⭐⭐⭐⭐ | Professional | 1.5 GB |

**Processing Time Examples (5-minute video):**
- Tiny: ~30 seconds
- Base: ~2-3 minutes
- Small: ~5-7 minutes
- Medium: ~10-15 minutes

**Accuracy Examples:**

**Tiny:**
- May miss words
- Basic sentence structure
- OK for rough drafts

**Base (Recommended):**
- Good word recognition
- Proper sentence structure
- Minimal editing needed

**Small:**
- Very accurate words
- Better punctuation
- Handles accents well

**Medium:**
- Excellent accuracy
- Perfect punctuation
- Handles multiple speakers
- Best for Devanagari

---

## Tips & Tricks

### Choosing the Right Model

**Use Tiny when:**
- Testing the tool for first time
- Previewing a video quickly
- You'll heavily edit anyway
- You're in a hurry

**Use Base when:**
- Regular daily use
- Audio quality is good
- English videos
- Balance of speed and quality

**Use Small when:**
- Important presentation
- Hindi/Marathi with Devanagari
- Multiple speakers
- Background noise present

**Use Medium when:**
- Professional/client work
- Final production
- Heavy accent in speech
- Maximum accuracy needed
- Complex Hindi/Marathi content

### Improving Accuracy

1. **Clean audio** = Better results
   - Minimize background noise
   - Clear speech
   - Good microphone

2. **Specify language** instead of auto-detect
   - If you know it's Hindi, select Hindi
   - More accurate than auto-detect

3. **Use larger model** for difficult content
   - Multiple speakers
   - Technical terms
   - Heavy accents

4. **Edit in browser** before downloading
   - Fix obvious errors immediately
   - Easier than editing in text editor later

---

## Keyboard Shortcuts

In the browser:
- **Ctrl + Click** on drop zone to browse
- **Scroll** in caption editor to view all
- **Tab** to navigate between fields
- **Ctrl + F** to find text in captions (browser feature)

---

## Troubleshooting

### Server Won't Start

**Error: Port 5000 already in use**
- Another program is using port 5000
- Close other apps or change port in web_server.py

**Error: Flask not installed**
- Run: `pip install flask flask-cors`
- Or: `pip install -r requirements.txt`

### Can't Access in Browser

**Try:**
1. Check server is running (command window open)
2. Try: http://127.0.0.1:5000
3. Check firewall isn't blocking
4. Restart browser

### Upload Fails

**Check:**
- File size under 500MB
- Valid video format (MP4, MOV, AVI, MKV)
- Internet connection (even for local server)
- Disk space available

### Progress Stuck

**If stuck at same percentage:**
- Wait 2-3 more minutes
- First run downloads models (takes time)
- Large videos take longer
- Check console/terminal for errors

### Editor Not Loading

**Solutions:**
- Refresh the page
- Re-upload the video
- Check browser console (F12) for errors
- Try different browser

### Can't Save Edits

**Check:**
- Server is still running
- You have write permissions
- Disk isn't full

---

## Advanced Usage

### Access from Other Devices

The server runs on all network interfaces (0.0.0.0), so you can access from other devices:

1. Find your computer's IP address
   ```
   Windows: ipconfig
   Look for IPv4 Address: 192.168.x.x
   ```

2. On other device (phone, tablet, another PC):
   ```
   http://192.168.x.x:5000
   ```

**Note:** Both devices must be on same network.

### Multiple Users

The web server supports multiple users simultaneously:
- Each user can upload their own video
- Processing happens in queue
- Each gets their own job ID

### Batch Processing

Process multiple videos:
1. Upload first video → Generate
2. While processing, open new browser tab
3. Upload second video → Generate
4. Both process in background

---

## File Management

### Where Files Are Stored

**Uploads folder:**
```
adobecaptions/uploads/
```
Original video files are stored here.

**Outputs folder:**
```
adobecaptions/outputs/
```
Generated SRT files are stored here.

### Cleanup

Periodically delete old files to save space:
```
Delete files from:
- uploads/
- outputs/
```

Or clear while server is stopped.

---

## Comparison: Web vs Desktop GUI vs CLI

| Feature | Web | Desktop GUI | CLI |
|---------|-----|-------------|-----|
| Interface | Browser | Windows app | Terminal |
| Drag & drop | ✅ | ✅ | ❌ |
| Model selection | ✅ | ✅ | ✅ |
| Caption editor | ✅ | ✅ | ❌ |
| Multi-device access | ✅ | ❌ | ❌ |
| No installation | ✅ (just browser) | ❌ (need tkinter) | ✅ |
| Offline use | ✅ | ✅ | ✅ |
| Mobile friendly | ✅ (responsive) | ❌ | ❌ |

**Use Web when:**
- You want browser-based interface
- Access from multiple devices
- Modern, clean UI
- No GUI installation wanted

**Use Desktop GUI when:**
- Prefer native Windows app
- No need for web server
- Single-user on one PC

**Use CLI when:**
- Batch processing many files
- Automation with scripts
- Minimal overhead

---

## FAQ

**Q: Do I need internet?**
A: Only for first run (downloads AI models). After that, works offline.

**Q: Can I use on Mac/Linux?**
A: Yes! Run `python web_server.py` and open browser.

**Q: Is it secure?**
A: It's for local use only. Don't expose to internet without security.

**Q: Can multiple people use it?**
A: Yes, on same network. Share the URL: http://your-ip:5000

**Q: Does it save my videos?**
A: Videos are saved in uploads/ folder. Delete them when done.

**Q: Can I change the port?**
A: Yes, edit web_server.py and change port from 5000 to another.

**Q: Why is first run slow?**
A: Downloads AI model files (~150MB for base). Subsequent runs are faster.

---

## Stopping the Server

**To stop the web server:**
1. Go to command window running the server
2. Press **Ctrl + C**
3. Server stops
4. Close browser tab

---

## Getting Help

1. Check this guide
2. See TROUBLESHOOTING.md
3. Check browser console (F12 → Console tab)
4. Check server console for error messages
5. Contact your dev team

---

**Enjoy the web interface! 🌐**

Last updated: 2026-01-11
