#fuckooredoo/__main__.py
"""
Command-line interface for F_ooredoo torrent downloader
Entry point: fuckooredoo
"""

import sys
import os
import subprocess
import platform


def check_tor_installed():
    """Check if Tor is installed and provide installation instructions"""
    system = platform.system().lower()
    
    # Check if tor is available in PATH
    try:
        if system == "windows":
            subprocess.run(["where", "tor"], capture_output=True, check=True)
        else:
            subprocess.run(["which", "tor"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Tor not found, provide installation instructions
    print("\n⚠️  Tor is not installed on your system!")
    print("\n📦 Installation Instructions:\n")
    
    if system == "linux":
        print("Ubuntu/Debian:")
        print("  sudo apt update && sudo apt install tor")
        print("\nFedora:")
        print("  sudo dnf install tor")
        print("\nArch Linux:")
        print("  sudo pacman -S tor")
    elif system == "darwin":
        print("macOS:")
        print("  brew install tor")
        print("\nOr visit: https://www.torproject.org/download/")
    elif system == "windows":
        print("Windows:")
        print("  Download Tor Browser from: https://www.torproject.org/download/")
        print("  Or use Chocolatey: choco install tor")
    
    print("\n❌ Please install Tor and run 'fuckooredoo' again.\n")
    return False


def check_tor_running():
    """Check if Tor service is running"""
    system = platform.system().lower()
    
    try:
        import socket
        # Try to connect to default Tor SOCKS port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 9050))
        sock.close()
        
        if result == 0:
            return True
        else:
            print("\n⚠️  Tor is installed but not running!")
            print("\n🚀 Starting Tor:\n")
            
            if system == "linux":
                print("  sudo systemctl start tor")
                print("  # Or: sudo service tor start")
            elif system == "darwin":
                print("  brew services start tor")
            elif system == "windows":
                print("  Start Tor Browser or run: tor.exe")
            
            print("\n❌ Please start Tor and run 'fuckooredoo' again.\n")
            return False
    except Exception as e:
        print(f"\n⚠️  Could not check Tor status: {e}")
        return False


def main():
    """Main entry point for the application"""
    print("=" * 70)
    print("🚀 F_ooredoo - Secure Torrent Downloader v1.0.2")
    print("   By Mohamed Aziz Bahloul")
    print("=" * 70)
    print()
    
    # Check if Tor is installed
    if not check_tor_installed():
        sys.exit(1)
    
    # Check if Tor is running
    if not check_tor_running():
        sys.exit(1)
    
    # Check for GUI availability and offer auto-install if missing
    try:
        from fuckooredoo import GUI_IMPORT_ERROR
    except Exception:
        GUI_IMPORT_ERROR = None
    
    if GUI_IMPORT_ERROR is not None and "--headless" not in sys.argv:
        print("\n⚠️  GUI (tkinter) not detected.")
        print("🔧 Attempting automatic installation...\n")
        
        try:
            from fuckooredoo.install_tkinter import install_tkinter
            if install_tkinter():
                print("\n✅ tkinter installed! Please restart the command to use the GUI.")
                print("   Or run now in headless mode: fuckooredoo --headless\n")
                sys.exit(0)
            else:
                print("\n❌ Automatic installation failed or not supported on this system.")
                print("Please install manually and try again.\n")
                sys.exit(1)
        except Exception as e:
            print(f"\n❌ Auto-install error: {e}")
            print("Please install tkinter manually.\n")
            sys.exit(1)
    
    print("✅ Tor is running!")
    print("🔒 All traffic will be routed through Tor")
    print("🚀 Starting F_ooredoo...\n")
    
    # Check for headless mode flag (--headless). If provided, run client without GUI
    headless = False
    magnet_arg = None
    if "--headless" in sys.argv:
        headless = True
        # Accept optional --magnet <uri>
        if "--magnet" in sys.argv:
            try:
                idx = sys.argv.index("--magnet")
                magnet_arg = sys.argv[idx + 1]
            except Exception:
                magnet_arg = None

    if headless:
        try:
            from fuckooredoo.torrent_client import TorrentClient
            client = TorrentClient()
            client.start_updates()
            print("\n✅ Running in headless mode. TorrentClient started and routing via Tor.")
            if magnet_arg:
                print(f"Adding magnet: {magnet_arg[:80]}")
                added = client.add_torrent(magnet_arg)
                print("Added:" if added else "Failed to add magnet")
            print("Press Ctrl-C to exit and shutdown the client.")
            try:
                while True:
                    # Keep process alive to let updates run
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down headless client...")
                client.shutdown()
                sys.exit(0)
        except Exception as e:
            print(f"\n❌ Headless mode failed: {e}")
            sys.exit(1)

    # Check for GUI import problems first (e.g. missing tkinter)
    try:
        # `GUI_IMPORT_ERROR` is set at package import time if importing the GUI failed
        from fuckooredoo import GUI_IMPORT_ERROR
    except Exception:
        GUI_IMPORT_ERROR = None

    if GUI_IMPORT_ERROR is not None:
        print(f"\n❌ GUI not available: {GUI_IMPORT_ERROR}")
        print("\nThis is usually caused by the system Python Tk (tkinter) not being installed.")
        print("Please install the OS package for tkinter and try again. Examples:")
        print("\nLinux (Debian/Ubuntu):")
        print("  sudo apt update && sudo apt install python3-tk")
        print("\nFedora:")
        print("  sudo dnf install python3-tkinter")
        print("\nArch Linux:")
        print("  sudo pacman -S tk")
        print("\nmacOS (Homebrew Python):")
        print("  brew install tcl-tk && \n  # then reinstall Python or set environment variables so Python links against brewed tcl-tk")
        print("\nWindows:")
        print("  Install Python from python.org and ensure Tcl/Tk option is enabled in the installer.")
        print("\nIf you use conda, run: conda install -c conda-forge tk")
        sys.exit(1)

    # Import and run the main application
    try:
        import customtkinter as ctk
        from fuckooredoo.torrent_client import TorrentClient
        from fuckooredoo.gui import TorrentGUI

        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create the torrent client with Tor enabled
        client = TorrentClient()

        # Create and run the GUI
        app = TorrentGUI(client)
        app.run()

    except KeyboardInterrupt:
        print("\n\n✋ Application stopped by user")
        sys.exit(0)
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\n📦 Please reinstall the package:")
        print("   pip install --upgrade fuckooredoo")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
