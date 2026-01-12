#!/usr/bin/env python3
"""
Adobe Premiere AI Captioning Tool - GUI Version
Drag-and-drop interface with caption editor
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
import re
from datetime import timedelta

# Import the caption tool
from caption_tool import CaptionTool


class SRTParser:
    """Parse and manage SRT files"""

    @staticmethod
    def parse_srt(file_path):
        """Parse SRT file into list of caption objects"""
        captions = []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by double newline to get caption blocks
        blocks = re.split(r'\n\n+', content.strip())

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])

                    # Parse timestamps
                    start, end = timestamp.split(' --> ')

                    captions.append({
                        'index': index,
                        'start': start.strip(),
                        'end': end.strip(),
                        'text': text.strip()
                    })
                except (ValueError, IndexError):
                    continue

        return captions

    @staticmethod
    def save_srt(captions, file_path):
        """Save captions to SRT file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, caption in enumerate(captions, start=1):
                caption['index'] = i  # Renumber
                f.write(f"{caption['index']}\n")
                f.write(f"{caption['start']} --> {caption['end']}\n")
                f.write(f"{caption['text']}\n")
                f.write("\n")


class CaptionEditorWindow:
    """Caption editor window with edit functionality"""

    def __init__(self, parent, srt_path, on_save_callback=None):
        self.srt_path = srt_path
        self.on_save_callback = on_save_callback
        self.captions = SRTParser.parse_srt(srt_path)
        self.modified = False

        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Caption Editor - {Path(srt_path).name}")
        self.window.geometry("1000x600")

        # Set icon (if available)
        try:
            self.window.iconbitmap('icon.ico')
        except:
            pass

        self.setup_ui()
        self.populate_captions()

        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Setup the UI layout"""

        # Top toolbar
        toolbar = ttk.Frame(self.window)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="💾 Save", command=self.save_captions).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="↻ Reload", command=self.reload_captions).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="➕ Add Caption", command=self.add_caption).pack(side=tk.LEFT, padx=2)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)

        ttk.Label(toolbar, text=f"Total: {len(self.captions)} captions").pack(side=tk.LEFT, padx=10)

        ttk.Button(toolbar, text="📋 Export to Premiere", command=self.export_info).pack(side=tk.RIGHT, padx=2)

        # Main container with scrollbar
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Store canvas for scrolling
        self.canvas = canvas

        # Bind mouse wheel
        self.window.bind_all("<MouseWheel>", self._on_mousewheel)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.window, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def populate_captions(self):
        """Populate the caption list"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Header
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(header_frame, text="#", width=5, font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Start", width=12, font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="End", width=12, font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Caption Text", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=10)

        ttk.Separator(self.scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)

        # Create caption entries
        for i, caption in enumerate(self.captions):
            self.create_caption_row(i, caption)

    def create_caption_row(self, index, caption):
        """Create a row for editing a caption"""
        row_frame = ttk.Frame(self.scrollable_frame)
        row_frame.pack(fill=tk.X, padx=5, pady=3)

        # Add alternating background colors
        if index % 2 == 0:
            row_frame.configure(style='Even.TFrame')

        # Index
        ttk.Label(row_frame, text=str(caption['index']), width=5).pack(side=tk.LEFT)

        # Start time (editable)
        start_var = tk.StringVar(value=caption['start'])
        start_entry = ttk.Entry(row_frame, textvariable=start_var, width=12, font=('Courier', 9))
        start_entry.pack(side=tk.LEFT, padx=2)
        start_entry.bind('<FocusOut>', lambda e, idx=index, var=start_var: self.update_start_time(idx, var))

        # End time (editable)
        end_var = tk.StringVar(value=caption['end'])
        end_entry = ttk.Entry(row_frame, textvariable=end_var, width=12, font=('Courier', 9))
        end_entry.pack(side=tk.LEFT, padx=2)
        end_entry.bind('<FocusOut>', lambda e, idx=index, var=end_var: self.update_end_time(idx, var))

        # Text (editable)
        text_frame = ttk.Frame(row_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        text_widget = tk.Text(text_frame, height=2, wrap=tk.WORD, font=('Arial', 10))
        text_widget.insert('1.0', caption['text'])
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_widget.bind('<FocusOut>', lambda e, idx=index, widget=text_widget: self.update_text(idx, widget))

        # Delete button
        delete_btn = ttk.Button(row_frame, text="🗑", width=3,
                               command=lambda idx=index: self.delete_caption(idx))
        delete_btn.pack(side=tk.LEFT, padx=2)

    def update_start_time(self, index, var):
        """Update start time"""
        self.captions[index]['start'] = var.get().strip()
        self.modified = True
        self.status_var.set("Modified - don't forget to save!")

    def update_end_time(self, index, var):
        """Update end time"""
        self.captions[index]['end'] = var.get().strip()
        self.modified = True
        self.status_var.set("Modified - don't forget to save!")

    def update_text(self, index, widget):
        """Update caption text"""
        self.captions[index]['text'] = widget.get('1.0', 'end-1c').strip()
        self.modified = True
        self.status_var.set("Modified - don't forget to save!")

    def delete_caption(self, index):
        """Delete a caption"""
        if messagebox.askyesno("Delete Caption", f"Delete caption #{self.captions[index]['index']}?"):
            del self.captions[index]
            self.modified = True
            self.populate_captions()
            self.status_var.set(f"Deleted caption. Total: {len(self.captions)}")

    def add_caption(self):
        """Add a new caption"""
        # Get last caption's end time or use 00:00:00,000
        if self.captions:
            last_end = self.captions[-1]['end']
        else:
            last_end = "00:00:00,000"

        new_caption = {
            'index': len(self.captions) + 1,
            'start': last_end,
            'end': "00:00:05,000",
            'text': "New caption text"
        }

        self.captions.append(new_caption)
        self.modified = True
        self.populate_captions()
        self.status_var.set("Added new caption")

    def save_captions(self):
        """Save captions to file"""
        try:
            SRTParser.save_srt(self.captions, self.srt_path)
            self.modified = False
            self.status_var.set(f"✓ Saved {len(self.captions)} captions to {Path(self.srt_path).name}")
            messagebox.showinfo("Saved", f"Captions saved successfully!\n\n{self.srt_path}")

            if self.on_save_callback:
                self.on_save_callback()
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save captions:\n{e}")

    def reload_captions(self):
        """Reload captions from file"""
        if self.modified:
            if not messagebox.askyesno("Reload", "You have unsaved changes. Reload anyway?"):
                return

        try:
            self.captions = SRTParser.parse_srt(self.srt_path)
            self.modified = False
            self.populate_captions()
            self.status_var.set("Reloaded from file")
        except Exception as e:
            messagebox.showerror("Reload Error", f"Failed to reload captions:\n{e}")

    def export_info(self):
        """Show export information"""
        info = f"""SRT file ready for Adobe Premiere Pro!

File: {self.srt_path}
Captions: {len(self.captions)}

To import in Premiere Pro:
1. File → Import (Ctrl+I)
2. Select this SRT file
3. Drag to timeline above video
4. Style using Caption Style presets

Recommended fonts for Hindi/Marathi:
• Noto Sans Devanagari
• Hind
• Mukta
"""
        messagebox.showinfo("Export to Premiere Pro", info)

    def on_close(self):
        """Handle window close"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Save before closing?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_captions()

        self.window.destroy()


class CaptionGUI:
    """Main GUI application"""

    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Adobe Premiere AI Captioning Tool")
        self.root.geometry("800x600")

        # Variables
        self.video_path = None
        self.srt_path = None
        self.processing = False

        # Caption tool
        self.caption_tool = None

        self.setup_ui()

        # Center window
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Setup the main UI"""

        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(
            title_frame,
            text="🎬 Adobe Premiere AI Captioning Tool",
            font=('Arial', 16, 'bold')
        ).pack()

        ttk.Label(
            title_frame,
            text="Generate AI captions for your videos",
            font=('Arial', 10)
        ).pack()

        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=20, pady=10)

        # Language selection
        lang_frame = ttk.Frame(settings_frame)
        lang_frame.pack(fill=tk.X, pady=5)

        ttk.Label(lang_frame, text="Language:", width=15).pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value="auto")
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=["Auto-detect", "English", "Hindi", "Marathi"],
            state='readonly',
            width=20
        )
        lang_combo.pack(side=tk.LEFT)
        lang_combo.current(0)

        # Model selection
        model_frame = ttk.Frame(settings_frame)
        model_frame.pack(fill=tk.X, pady=5)

        ttk.Label(model_frame, text="Model:", width=15).pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["tiny (fast)", "base (balanced)", "small (better)", "medium (best)"],
            state='readonly',
            width=20
        )
        model_combo.pack(side=tk.LEFT)
        model_combo.current(1)

        ttk.Label(model_frame, text="  💡 Larger = slower but more accurate",
                 font=('Arial', 8)).pack(side=tk.LEFT, padx=10)

        # Drop zone
        drop_frame = ttk.LabelFrame(self.root, text="Drop Video Here", padding=20)
        drop_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.drop_label = tk.Label(
            drop_frame,
            text="🎥\n\nDrag & Drop Video File Here\n\nor click Browse\n\n(MP4, MOV, AVI, MKV)",
            font=('Arial', 14),
            bg='#f0f0f0',
            relief=tk.RIDGE,
            borderwidth=2,
            cursor='hand2'
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True)

        # Enable drag and drop
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_label.bind('<Button-1>', lambda e: self.browse_file())

        # Progress frame
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill=tk.X, padx=20, pady=10)

        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(
            self.progress_frame,
            textvariable=self.progress_var,
            font=('Arial', 10)
        )
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=300
        )

        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.browse_btn = ttk.Button(
            button_frame,
            text="📁 Browse Video",
            command=self.browse_file
        )
        self.browse_btn.pack(side=tk.LEFT, padx=5)

        self.process_btn = ttk.Button(
            button_frame,
            text="▶ Generate Captions",
            command=self.process_video,
            state=tk.DISABLED
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)

        self.edit_btn = ttk.Button(
            button_frame,
            text="✏ Edit Captions",
            command=self.open_editor,
            state=tk.DISABLED
        )
        self.edit_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = ttk.Button(
            button_frame,
            text="📋 Export Info",
            command=self.show_export_info,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready - Drop a video file or click Browse")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_drop(self, event):
        """Handle file drop"""
        # Get file path (remove {} if present)
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]

        self.load_video(file_path)

    def browse_file(self):
        """Browse for video file"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.mov *.avi *.mkv"),
                ("MP4 Files", "*.mp4"),
                ("MOV Files", "*.mov"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.load_video(file_path)

    def load_video(self, file_path):
        """Load a video file"""
        file_path = Path(file_path)

        if not file_path.exists():
            messagebox.showerror("Error", f"File not found:\n{file_path}")
            return

        self.video_path = file_path
        self.srt_path = file_path.with_suffix('.srt')

        # Update UI
        self.drop_label.config(
            text=f"✓ Video Loaded\n\n{file_path.name}\n\n({self.format_size(file_path.stat().st_size)})",
            bg='#e8f5e9'
        )

        self.status_var.set(f"Loaded: {file_path.name}")
        self.process_btn.config(state=tk.NORMAL)

        # Check if SRT already exists
        if self.srt_path.exists():
            response = messagebox.askyesno(
                "Captions Found",
                f"Caption file already exists:\n{self.srt_path.name}\n\nDo you want to open the editor?"
            )
            if response:
                self.edit_btn.config(state=tk.NORMAL)
                self.export_btn.config(state=tk.NORMAL)
                self.open_editor()

    def format_size(self, size_bytes):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def get_language_code(self):
        """Get language code from selection"""
        lang_map = {
            "Auto-detect": None,
            "English": "en",
            "Hindi": "hi",
            "Marathi": "mr"
        }
        return lang_map.get(self.language_var.get())

    def get_model_name(self):
        """Get model name from selection"""
        model_map = {
            "tiny (fast)": "tiny",
            "base (balanced)": "base",
            "small (better)": "small",
            "medium (best)": "medium"
        }
        return model_map.get(self.model_var.get(), "base")

    def process_video(self):
        """Process video in background thread"""
        if self.processing:
            messagebox.showwarning("Processing", "Already processing a video!")
            return

        if not self.video_path:
            messagebox.showerror("Error", "No video loaded!")
            return

        # Confirm if SRT exists
        if self.srt_path.exists():
            if not messagebox.askyesno(
                "Overwrite?",
                f"Caption file already exists:\n{self.srt_path.name}\n\nOverwrite?"
            ):
                return

        # Start processing
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.browse_btn.config(state=tk.DISABLED)
        self.edit_btn.config(state=tk.DISABLED)

        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)

        # Run in thread
        thread = threading.Thread(target=self.process_video_thread, daemon=True)
        thread.start()

    def process_video_thread(self):
        """Process video in background"""
        try:
            # Update status
            self.root.after(0, lambda: self.progress_var.set("⏳ Initializing..."))

            # Get settings
            language = self.get_language_code()
            model_name = self.get_model_name()

            # Create caption tool
            self.caption_tool = CaptionTool(model_size=model_name, device='cpu')

            # Check FFmpeg
            self.root.after(0, lambda: self.progress_var.set("⏳ Checking FFmpeg..."))
            if not self.caption_tool.check_ffmpeg():
                self.root.after(0, lambda: messagebox.showerror(
                    "FFmpeg Not Found",
                    "FFmpeg is not installed or not in PATH.\n\n"
                    "Please install FFmpeg:\n"
                    "1. choco install ffmpeg\n"
                    "2. Or download from ffmpeg.org"
                ))
                return

            # Extract audio
            self.root.after(0, lambda: self.progress_var.set("🎵 Extracting audio..."))
            temp_audio = self.video_path.with_suffix('.temp.wav')

            if not self.caption_tool.extract_audio(self.video_path, temp_audio):
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    "Failed to extract audio from video!"
                ))
                return

            # Transcribe
            self.root.after(0, lambda: self.progress_var.set("🤖 Loading AI model..."))
            segments, detected_lang = self.caption_tool.transcribe_audio(temp_audio, language)

            self.root.after(0, lambda: self.progress_var.set("💬 Generating captions..."))

            # Generate SRT
            self.caption_tool.generate_srt(segments, self.srt_path)

            # Cleanup
            if temp_audio.exists():
                temp_audio.unlink()

            # Success!
            self.root.after(0, self.processing_complete)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Processing Error",
                f"Failed to process video:\n\n{str(e)}"
            ))
            self.root.after(0, self.processing_failed)
        finally:
            self.processing = False

    def processing_complete(self):
        """Called when processing completes successfully"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        self.progress_var.set("✅ Captions generated successfully!")
        self.status_var.set(f"✓ Saved: {self.srt_path.name}")

        self.process_btn.config(state=tk.NORMAL)
        self.browse_btn.config(state=tk.NORMAL)
        self.edit_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.NORMAL)

        # Show success message
        response = messagebox.askyesno(
            "Success!",
            f"Captions generated successfully!\n\n"
            f"File: {self.srt_path.name}\n\n"
            f"Do you want to open the caption editor?"
        )

        if response:
            self.open_editor()

    def processing_failed(self):
        """Called when processing fails"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        self.progress_var.set("❌ Processing failed")
        self.status_var.set("Error - check console for details")

        self.process_btn.config(state=tk.NORMAL)
        self.browse_btn.config(state=tk.NORMAL)

    def open_editor(self):
        """Open caption editor window"""
        if not self.srt_path or not self.srt_path.exists():
            messagebox.showerror("Error", "No caption file found!")
            return

        # Open editor window
        CaptionEditorWindow(self.root, self.srt_path, on_save_callback=self.on_editor_save)

    def on_editor_save(self):
        """Called when editor saves"""
        self.status_var.set(f"✓ Captions saved: {self.srt_path.name}")

    def show_export_info(self):
        """Show export information"""
        if not self.srt_path or not self.srt_path.exists():
            messagebox.showerror("Error", "No caption file found!")
            return

        info = f"""SRT file ready for Adobe Premiere Pro!

File: {self.srt_path}
Size: {self.format_size(self.srt_path.stat().st_size)}

To import in Premiere Pro:
1. File → Import (Ctrl+I)
2. Select the SRT file
3. Drag to timeline above video
4. Style using Caption Style presets

Recommended fonts for Hindi/Marathi:
• Noto Sans Devanagari
• Hind
• Mukta

Location:
{self.srt_path.absolute()}
"""
        messagebox.showinfo("Export to Premiere Pro", info)

    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = CaptionGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application:\n\n{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
