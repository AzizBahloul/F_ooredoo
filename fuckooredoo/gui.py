#gui.py

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
from typing import Optional
from .torrent_client import TorrentClient
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Native file chooser helpers: prefer GTK (PyGObject) on Zorin/Ubuntu, fall back to zenity, then tkinter
def _choose_directory_native(title: str, mustexist: bool = False):
    """Return a directory path selected using the native OS dialog.
    Tries GTK via PyGObject first, then zenity, then tkinter.filedialog.
    """
    # 1) Try PyGObject (GTK)
    try:
        from gi.repository import Gtk  # type: ignore

        dialog = Gtk.FileChooserDialog(title=title, parent=None, action=Gtk.FileChooserAction.SELECT_FOLDER,
                                       buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_select_multiple(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
        else:
            path = None
        dialog.destroy()
        return path
    except Exception:
        pass

    # 2) Try zenity (good fallback on many Linux desktops)
    try:
        zenity_cmd = ["zenity", "--file-selection", "--directory", "--title", title]
        p = subprocess.run(zenity_cmd, capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout.strip()
    except Exception:
        pass

    # 3) Last resort: tkinter native chooser
    try:
        return filedialog.askdirectory(title=title, mustexist=mustexist)
    except Exception:
        return None


def _choose_file_native(title: str, filetypes=None):
    """Return a file path selected using the native OS dialog.
    Tries GTK via PyGObject first, then zenity, then tkinter.filedialog.
    """
    # 1) PyGObject (GTK)
    try:
        from gi.repository import Gtk  # type: ignore

        dialog = Gtk.FileChooserDialog(title=title, parent=None, action=Gtk.FileChooserAction.OPEN,
                                       buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_select_multiple(False)
        if filetypes:
            filt = Gtk.FileFilter()
            for desc, pattern in filetypes:
                filt.add_pattern(pattern)
            dialog.add_filter(filt)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
        else:
            path = None
        dialog.destroy()
        return path
    except Exception:
        pass

    # 2) zenity
    try:
        zenity_cmd = ["zenity", "--file-selection", "--title", title]
        if filetypes:
            for desc, pattern in filetypes:
                zenity_cmd.extend(["--file-filter", f"{desc} | {pattern}"])

        p = subprocess.run(zenity_cmd, capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout.strip()
    except Exception:
        pass

    # 3) tkinter fallback
    try:
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    except Exception:
        return None


class TorrentGUI:
    """Modern GUI application for torrent downloading"""
    
    def __init__(self, client: TorrentClient):
        logger.info("Initializing TorrentGUI...")
        self.client = client
        self.client.status_callback = self._update_torrent_list
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("🚀 Secure Torrent Downloader - Tor Anti-Throttling")
        self.root.geometry("1300x850")
        
        # Set minimum window size
        self.root.minsize(1000, 700)
        
        # Store torrent frames for updates
        self.torrent_frames = {}
        
        logger.info("Prompting user to select download path...")
        # Force user to select download path on startup
        self._force_select_download_path()
        
        # Build the UI
        self._build_ui()
        
        logger.info("GUI initialized successfully")
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _build_ui(self):
        """Build the complete user interface"""
        logger.info("Building user interface...")
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Top control panel
        self._build_control_panel()
        
        # Main content area
        self._build_content_area()
        
        # Bottom status bar
        self._build_status_bar()
        logger.info("User interface built successfully")
    
    def _force_select_download_path(self):
        """Force user to select download path on startup"""
        logger.info("Forcing user to select download directory...")
        # If the client already has a valid download path, don't force the dialog.
        try:
            current_path = self.client.download_path
        except Exception:
            current_path = None

        if current_path and os.path.isdir(current_path) and os.access(current_path, os.W_OK):
            logger.info(f"Existing download path is valid: {current_path} - skipping prompt")
            return
        while True:
            # Use the system/native directory chooser. Allow user to type a new path.
            path = _choose_directory_native(title="🗂️ Select Download Directory", mustexist=False)
            
            if not path:
                logger.warning("User cancelled directory selection, asking again...")
                response = messagebox.askyesno(
                    "Download Path Required",
                    "You must select a download directory to continue.\n\nClick 'Yes' to select again or 'No' to exit."
                )
                if not response:
                    logger.info("User chose to exit without selecting download path")
                    self.root.quit()
                    exit(0)
                continue
            
            logger.info(f"User selected download path: {path}")
            # If the path doesn't exist, ask the user if they'd like to create it.
            if not os.path.exists(path):
                create = messagebox.askyesno(
                    "Create Directory?",
                    f"The directory '{path}' does not exist. Create it?"
                )
                if not create:
                    logger.info("User declined to create the selected directory; asking again...")
                    continue
            # set_download_path will ensure the directory exists (it calls makedirs)
            self.client.set_download_path(path)
            logger.info(f"Download path set to: {path}")
            break
    
    def _build_control_panel(self):
        """Build top control panel with input and buttons"""
        control_frame = ctk.CTkFrame(self.root, corner_radius=10)
        control_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            control_frame,
            text="🔒 Encrypted Torrent Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(15, 5), padx=20, sticky="w")
        
        # Subtitle with encryption info
        subtitle_label = ctk.CTkLabel(
            control_frame,
            text="✓ RC4/MSE Encryption Active  •  ✓ DPI Bypass Enabled  •  ✓ Anti-Throttling Protection",
            font=ctk.CTkFont(size=12),
            text_color="lime"
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 15), padx=20, sticky="w")
        
        # Magnet link input
        magnet_label = ctk.CTkLabel(
            control_frame,
            text="Magnet Link / Torrent File:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        magnet_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 5), sticky="w")
        
        self.magnet_entry = ctk.CTkEntry(
            control_frame,
            placeholder_text="Paste magnet link here (magnet:?xt=urn:btih:...)",
            height=45,
            font=ctk.CTkFont(size=13)
        )
        self.magnet_entry.grid(row=3, column=0, padx=(20, 10), pady=(0, 20), sticky="ew")
        
        # Buttons frame
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=3, column=1, padx=10, pady=(0, 20), sticky="e")
        
        # Browse button
        browse_btn = ctk.CTkButton(
            button_frame,
            text="📁 Browse .torrent",
            command=self._browse_torrent,
            width=150,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#3B3B3B"
        )
        browse_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Add button
        add_btn = ctk.CTkButton(
            button_frame,
            text="⬇ Download",
            command=self._add_torrent,
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1E88E5",
            hover_color="#1565C0"
        )
        add_btn.grid(row=0, column=1, padx=(0, 20))
    
    def _build_content_area(self):
        """Build main content area with torrent list"""
        content_frame = ctk.CTkFrame(self.root, corner_radius=10)
        content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="📥 Active Downloads",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header_label.pack(side="left")
        
        # Settings button
        settings_btn = ctk.CTkButton(
            header_frame,
            text="⚙️ Settings",
            command=self._open_settings,
            width=120,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#424242",
            hover_color="#525252"
        )
        settings_btn.pack(side="right", padx=(0, 10))
        
        # Clear all button
        clear_btn = ctk.CTkButton(
            header_frame,
            text="🗑️ Clear All",
            command=self._clear_all,
            width=120,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#D32F2F",
            hover_color="#B71C1C"
        )
        clear_btn.pack(side="right")
        
        # Scrollable frame for torrents
        self.scroll_frame = ctk.CTkScrollableFrame(
            content_frame,
            corner_radius=10,
            fg_color="#1A1A1A"
        )
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Empty state message
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="No active downloads\n\nPaste a magnet link above and click 'Download' to start",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.empty_label.grid(row=0, column=0, pady=100)
    
    def _build_status_bar(self):
        """Build bottom status bar"""
        status_frame = ctk.CTkFrame(self.root, height=60, corner_radius=10)
        status_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Global speed indicator (left side)
        speed_frame = ctk.CTkFrame(status_frame, fg_color="#1E1E1E", corner_radius=8)
        speed_frame.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        speed_icon = ctk.CTkLabel(
            speed_frame,
            text="🌐",
            font=ctk.CTkFont(size=18)
        )
        speed_icon.pack(side="left", padx=(10, 5))
        
        self.global_download_label = ctk.CTkLabel(
            speed_frame,
            text="⬇ 0.00 MB/s",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4CAF50"
        )
        self.global_download_label.pack(side="left", padx=5)
        
        self.global_upload_label = ctk.CTkLabel(
            speed_frame,
            text="⬆ 0.00 MB/s",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FF9800"
        )
        self.global_upload_label.pack(side="left", padx=(5, 10))
        
        # Tor status indicator
        tor_frame = ctk.CTkFrame(status_frame, fg_color="#1E1E1E", corner_radius=8)
        tor_frame.grid(row=0, column=0, padx=(200, 15), pady=10, sticky="w")
        
        tor_icon = ctk.CTkLabel(
            tor_frame,
            text="🧅",
            font=ctk.CTkFont(size=18)
        )
        tor_icon.pack(side="left", padx=(10, 5))
        
        tor_label = ctk.CTkLabel(
            tor_frame,
            text="Tor Active",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4CAF50"
        )
        tor_label.pack(side="left", padx=(5, 10))
        
        # Download path (center)
        path_container = ctk.CTkFrame(status_frame, fg_color="transparent")
        path_container.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        path_label = ctk.CTkLabel(
            path_container,
            text="📁 Download Path:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        path_label.pack(side="left", padx=(5, 5))
        
        self.path_value = ctk.CTkLabel(
            path_container,
            text=self.client.download_path,
            font=ctk.CTkFont(size=11),
            text_color="#90A4AE"
        )
        self.path_value.pack(side="left", padx=5)
        
        # Change path button (right)
        change_path_btn = ctk.CTkButton(
            status_frame,
            text="📂 Change",
            command=self._change_download_path,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#424242",
            hover_color="#525252",
            corner_radius=8
        )
        change_path_btn.grid(row=0, column=2, padx=15, pady=10)
    
    def _browse_torrent(self):
        """Browse for .torrent file"""
        logger.info("User opening file browser for .torrent selection...")
        filename = _choose_file_native(
            title="Select Torrent File",
            filetypes=[("Torrent Files", "*.torrent"), ("All Files", "*.*")]
        )
        if filename:
            logger.info(f"User selected torrent file: {filename}")
            self.magnet_entry.delete(0, 'end')
            self.magnet_entry.insert(0, filename)
        else:
            logger.info("User cancelled file browser")
    
    def _add_torrent(self):
        """Add a new torrent"""
        magnet_uri = self.magnet_entry.get().strip()
        
        logger.info(f"User attempting to add torrent: {magnet_uri[:80]}...")
        
        if not magnet_uri:
            logger.warning("User tried to add torrent without providing magnet link or file")
            messagebox.showwarning("Warning", "Please enter a magnet link or select a torrent file!")
            return
        
        # Add torrent in background thread
        def add_thread():
            logger.info(f"Starting thread to add torrent...")
            success = self.client.add_torrent(magnet_uri)
            if success:
                logger.info("Torrent added successfully")
                self.magnet_entry.delete(0, 'end')
                self._show_notification("✅ Torrent Added", "Download started with encryption enabled!")
            else:
                logger.error(f"Failed to add torrent: {magnet_uri}")
                self._show_notification("❌ Error", "Failed to add torrent. Check the link/file.", error=True)
        
        threading.Thread(target=add_thread, daemon=True).start()
    
    def _update_torrent_list(self, torrents):
        """Update the torrent list display"""
        # Run in main thread
        self.root.after(0, lambda: self._update_torrent_list_ui(torrents))
    
    def _update_torrent_list_ui(self, torrents):
        """Update torrent list UI (must be called from main thread)"""
        # Hide/show empty label
        if torrents:
            self.empty_label.grid_forget()
        else:
            self.empty_label.grid(row=0, column=0, pady=100)
            # Reset global speeds when no torrents
            self.global_download_label.configure(text="⬇ 0.00 MB/s", text_color="#757575")
            self.global_upload_label.configure(text="⬆ 0.00 MB/s", text_color="#757575")
            return
        
        # Calculate total speeds
        total_download = sum(t['download_speed'] for t in torrents)
        total_upload = sum(t['upload_speed'] for t in torrents)
        
        # Update global speed display
        dl_color = "#4CAF50" if total_download > 0 else "#757575"
        ul_color = "#FF9800" if total_upload > 0 else "#757575"
        
        self.global_download_label.configure(
            text=f"⬇ {total_download:.2f} MB/s",
            text_color=dl_color
        )
        self.global_upload_label.configure(
            text=f"⬆ {total_upload:.2f} MB/s",
            text_color=ul_color
        )
        
        # Update or create torrent cards
        current_names = set()
        
        for i, status in enumerate(torrents):
            name = status['name']
            current_names.add(name)
            
            if name not in self.torrent_frames:
                # Create new torrent card
                self._create_torrent_card(name, i)
            
            # Update torrent card
            self._update_torrent_card(name, status)
        
        # Remove torrents that no longer exist
        for name in list(self.torrent_frames.keys()):
            if name not in current_names:
                self.torrent_frames[name]['frame'].destroy()
                del self.torrent_frames[name]
    
    def _create_torrent_card(self, name: str, row: int):
        """Create a new torrent display card"""
        # Main card frame with gradient-like effect
        card_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=15, fg_color="#2A2A2A", border_width=2, border_color="#3A3A3A")
        card_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Header with name and buttons
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=name,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        # Button frame
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")
        
        pause_btn = ctk.CTkButton(
            btn_frame,
            text="⏸",
            command=lambda: self._pause_torrent(name),
            width=45,
            height=35,
            font=ctk.CTkFont(size=16),
            fg_color="#424242",
            hover_color="#525252",
            corner_radius=8
        )
        pause_btn.grid(row=0, column=0, padx=3)
        
        resume_btn = ctk.CTkButton(
            btn_frame,
            text="▶",
            command=lambda: self._resume_torrent(name),
            width=45,
            height=35,
            font=ctk.CTkFont(size=16),
            fg_color="#43A047",
            hover_color="#2E7D32",
            corner_radius=8
        )
        resume_btn.grid(row=0, column=1, padx=3)
        
        remove_btn = ctk.CTkButton(
            btn_frame,
            text="🗑",
            command=lambda: self._remove_torrent(name),
            width=45,
            height=35,
            font=ctk.CTkFont(size=16),
            fg_color="#E53935",
            hover_color="#C62828",
            corner_radius=8
        )
        remove_btn.grid(row=0, column=2, padx=3)
        
        # Progress percentage and status
        progress_status_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        progress_status_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 5))
        progress_status_frame.grid_columnconfigure(1, weight=1)
        
        progress_label = ctk.CTkLabel(
            progress_status_frame,
            text="0%",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4FC3F7"
        )
        progress_label.grid(row=0, column=0, sticky="w")
        
        state_label = ctk.CTkLabel(
            progress_status_frame,
            text="Initializing...",
            font=ctk.CTkFont(size=12),
            text_color="#90A4AE"
        )
        state_label.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        # Progress bar with enhanced styling
        progress_bar = ctk.CTkProgressBar(
            card_frame,
            height=25,
            corner_radius=12,
            progress_color="#1E88E5",
            fg_color="#1A1A1A"
        )
        progress_bar.grid(row=2, column=0, padx=20, pady=(5, 15), sticky="ew")
        progress_bar.set(0)
        
        # Stats grid - 2 rows, 3 columns
        stats_frame = ctk.CTkFrame(card_frame, fg_color="#1E1E1E", corner_radius=10)
        stats_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Row 1: Download Speed, Upload Speed, Peers
        download_label = ctk.CTkLabel(
            stats_frame,
            text="⬇ 0.00 MB/s",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4CAF50"
        )
        download_label.grid(row=0, column=0, padx=15, pady=(12, 6), sticky="w")
        
        upload_label = ctk.CTkLabel(
            stats_frame,
            text="⬆ 0.00 MB/s",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FF9800"
        )
        upload_label.grid(row=0, column=1, padx=15, pady=(12, 6), sticky="w")
        
        peers_label = ctk.CTkLabel(
            stats_frame,
            text="👥 0 peers",
            font=ctk.CTkFont(size=13),
            text_color="#B0BEC5"
        )
        peers_label.grid(row=0, column=2, padx=15, pady=(12, 6), sticky="e")
        
        # Row 2: Size, Remaining Time, Encryption Status
        size_label = ctk.CTkLabel(
            stats_frame,
            text="📦 0 MB / 0 MB",
            font=ctk.CTkFont(size=12),
            text_color="#B0BEC5"
        )
        size_label.grid(row=1, column=0, padx=15, pady=(6, 12), sticky="w")
        
        eta_label = ctk.CTkLabel(
            stats_frame,
            text="⏱ ∞",
            font=ctk.CTkFont(size=12),
            text_color="#FFC107"
        )
        eta_label.grid(row=1, column=1, padx=15, pady=(6, 12), sticky="w")
        
        encryption_label = ctk.CTkLabel(
            stats_frame,
            text="🔒 Encrypted",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00E676"
        )
        encryption_label.grid(row=1, column=2, padx=15, pady=(6, 12), sticky="e")
        
        # Store references
        self.torrent_frames[name] = {
            'frame': card_frame,
            'progress_bar': progress_bar,
            'progress_label': progress_label,
            'state_label': state_label,
            'download_label': download_label,
            'upload_label': upload_label,
            'peers_label': peers_label,
            'size_label': size_label,
            'eta_label': eta_label,
            'encryption_label': encryption_label,
        }
    
    def _update_torrent_card(self, name: str, status: dict):
        """Update a torrent card with current status"""
        if name not in self.torrent_frames:
            return
        
        frame_data = self.torrent_frames[name]
        
        # Update progress bar
        progress = status['progress'] / 100.0
        frame_data['progress_bar'].set(progress)
        
        # Update progress percentage
        frame_data['progress_label'].configure(text=f"{status['progress']:.1f}%")
        
        # Update state
        frame_data['state_label'].configure(text=status['state'].title())
        
        # Update download speed with color
        dl_speed = status['download_speed']
        dl_color = "#4CAF50" if dl_speed > 0 else "#757575"
        frame_data['download_label'].configure(
            text=f"⬇ {dl_speed:.2f} MB/s",
            text_color=dl_color
        )
        
        # Update upload speed with color
        ul_speed = status['upload_speed']
        ul_color = "#FF9800" if ul_speed > 0 else "#757575"
        frame_data['upload_label'].configure(
            text=f"⬆ {ul_speed:.2f} MB/s",
            text_color=ul_color
        )
        
        # Update peers
        num_peers = status['num_peers']
        num_seeds = status['num_seeds']
        peers_color = "#4CAF50" if num_peers > 0 else "#757575"
        frame_data['peers_label'].configure(
            text=f"👥 {num_peers} peers ({num_seeds} seeds)",
            text_color=peers_color
        )
        
        # Update size (downloaded / total)
        downloaded_mb = status['downloaded'] / (1024 * 1024)
        total_mb = status['total_size'] / (1024 * 1024)
        
        if total_mb >= 1024:  # Show in GB if > 1GB
            downloaded_gb = downloaded_mb / 1024
            total_gb = total_mb / 1024
            size_text = f"📦 {downloaded_gb:.2f} GB / {total_gb:.2f} GB"
        else:
            size_text = f"📦 {downloaded_mb:.1f} MB / {total_mb:.1f} MB"
        
        frame_data['size_label'].configure(text=size_text)
        
        # Update ETA
        eta = status.get('eta', '∞')
        eta_color = "#FFC107" if eta != "∞" else "#757575"
        frame_data['eta_label'].configure(
            text=f"⏱ {eta}",
            text_color=eta_color
        )
        
        # Update encryption status with animation-like effect
        encryption = status['encryption']
        if "Encrypted" in encryption:
            frame_data['encryption_label'].configure(
                text="🔒 Encrypted",
                text_color="#00E676"
            )
        elif "Connecting" in encryption:
            frame_data['encryption_label'].configure(
                text="⏳ Connecting...",
                text_color="#FFC107"
            )
        else:
            frame_data['encryption_label'].configure(
                text=encryption,
                text_color="#90A4AE"
            )
    
    def _pause_torrent(self, name: str):
        """Pause a torrent"""
        logger.info(f"User pausing torrent: {name}")
        self.client.pause_torrent(name)
        logger.info(f"Torrent paused: {name}")
    
    def _resume_torrent(self, name: str):
        """Resume a torrent"""
        logger.info(f"User resuming torrent: {name}")
        self.client.resume_torrent(name)
        logger.info(f"Torrent resumed: {name}")
    
    def _remove_torrent(self, name: str):
        """Remove a torrent after confirmation"""
        logger.info(f"User attempting to remove torrent: {name}")
        response = messagebox.askyesnocancel(
            "Remove Torrent",
            f"Remove '{name}'?\n\nYes = Keep files\nNo = Delete files\nCancel = Don't remove"
        )
        
        if response is None:  # Cancel
            logger.info(f"User cancelled torrent removal: {name}")
            return
        
        delete_files = not response  # No = delete files
        logger.info(f"Removing torrent: {name} (delete_files={delete_files})")
        self.client.remove_torrent(name, delete_files)
    
    def _clear_all(self):
        """Clear all torrents"""
        logger.info("User attempting to clear all torrents...")
        if not self.torrent_frames:
            logger.info("No torrents to clear")
            return
        
        response = messagebox.askyesno(
            "Clear All",
            "Remove all torrents?\n\nFiles will be kept."
        )
        
        if response:
            logger.info("User confirmed clearing all torrents")
            for name in list(self.torrent_frames.keys()):
                logger.info(f"Removing torrent: {name}")
                self.client.remove_torrent(name, delete_files=False)
        else:
            logger.info("User cancelled clear all operation")
    
    def _change_download_path(self):
        """Change download directory"""
        logger.info("User requesting to change download path...")
        # Allow creation of a new directory from the native dialog
        path = _choose_directory_native(title="Select Download Directory", mustexist=False)
        if not path:
            logger.info("User cancelled path selection")
            return

        logger.info(f"User selected new download path: {path}")
        if not os.path.exists(path):
            create = messagebox.askyesno(
                "Create Directory?",
                f"The directory '{path}' does not exist. Create it?"
            )
            if not create:
                logger.info("User declined to create the selected directory; aborting change")
                return

        # set_download_path will create the directory if needed
        self.client.set_download_path(path)
        self.path_value.configure(text=path)
        logger.info(f"Download path changed to: {path}")
    
    def _open_settings(self):
        """Open settings window"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("600x500")
        settings_window.transient(self.root)
        
        # Wait for window to be visible before grabbing
        settings_window.after(100, lambda: settings_window.grab_set())
        
        # Title
        title = ctk.CTkLabel(
            settings_window,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Info frame
        info_frame = ctk.CTkFrame(settings_window, corner_radius=10)
        info_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        info_text = """
🔒 Tor-Based Anti-Throttling:
   • All traffic routed through Tor (SOCKS5: 127.0.0.1:9050)
   • Protocol: RC4/MSE (Message Stream Encryption)
   • Mode: Forced encryption + Tor routing
   • DHT: Enabled with obfuscation
   • uTP: Enabled for additional DPI bypass
   
✓ Active Protection:
   • Tor Network Routing (Maximum ISP Bypass)
   • Deep Packet Inspection (DPI) Bypass
   • Traffic Pattern Randomization
   • Port Randomization
   • Encrypted Peer Discovery
   
📊 Performance:
   • Connection Limit: 500 peers
   • Download Speed: Unlimited
   • Upload Speed: Unlimited (helps ratio)
   
💡 Tips:
   • Keep the application running for best speeds
   • The encryption adds minimal CPU overhead
   • Works best with popular torrents (more encrypted peers)
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=20, pady=20, anchor="w")
        
        # Close button
        close_btn = ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            width=120,
            height=35
        )
        close_btn.pack(pady=20)
    
    def _show_notification(self, title: str, message: str, error: bool = False):
        """Show a notification message"""
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def _on_closing(self):
        """Handle window close event"""
        logger.info("User attempting to close application...")
        response = messagebox.askyesno(
            "Confirm Exit",
            "Are you sure you want to exit?\n\nAll downloads will be paused."
        )
        
        if response:
            logger.info("User confirmed application exit")
            logger.info("Shutting down torrent client...")
            self.client.shutdown()
            logger.info("Destroying GUI...")
            self.root.quit()
            self.root.destroy()
            logger.info("Application closed successfully")
        else:
            logger.info("User cancelled application exit")
    
    def run(self):
        """Start the GUI main loop"""
        # Start torrent client updates
        self.client.start_updates()
        
        # Start the GUI main loop
        self.root.mainloop()
