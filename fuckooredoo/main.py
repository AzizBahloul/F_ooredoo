#fuckooredoo/main.py
"""
Secure Torrent Downloader with Tor-based Anti-Throttling
Bypasses ISP throttling through Tor network routing and traffic encryption
"""

import customtkinter as ctk
from .torrent_client import TorrentClient
from .gui import TorrentGUI
import sys


def main():
    """Main application entry point"""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create the torrent client with encryption enabled
    client = TorrentClient()
    
    # Create and run the GUI
    app = TorrentGUI(client)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
