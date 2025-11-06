#verify.py
"""
Comprehensive verification script for Secure Torrent Downloader
Checks all dependencies, configurations, and settings
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("🔍 Secure Torrent Downloader - Verification Script")
print("=" * 70)
print()

# Track all checks
all_passed = True

# Check 1: Virtual Environment
print("1️⃣  Checking Virtual Environment...")
venv_path = Path("venv")
if venv_path.exists():
    print("   ✅ Virtual environment exists")
    
    # Check if we're running inside venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Running inside virtual environment")
        print(f"   📍 Python location: {sys.executable}")
    else:
        print("   ⚠️  NOT running inside virtual environment!")
        print("   Please run: source venv/bin/activate")
        all_passed = False
else:
    print("   ❌ Virtual environment not found!")
    print("   Please run: ./setup.sh")
    all_passed = False

print()

# Check 2: Python Version
print("2️⃣  Checking Python Version...")
version = sys.version_info
print(f"   📍 Python {version.major}.{version.minor}.{version.micro}")
if version.major == 3 and version.minor >= 8:
    print("   ✅ Python version is compatible (3.8+)")
else:
    print("   ❌ Python version too old! Need 3.8 or higher")
    all_passed = False

print()

# Check 3: Dependencies
print("3️⃣  Checking Dependencies...")

# libtorrent
try:
    import libtorrent as lt
    print(f"   ✅ libtorrent {lt.__version__}")
except ImportError as e:
    print(f"   ❌ libtorrent not found: {e}")
    all_passed = False

# customtkinter
try:
    import customtkinter as ctk
    print(f"   ✅ customtkinter")
except ImportError as e:
    print(f"   ❌ customtkinter not found: {e}")
    all_passed = False

# Pillow
try:
    from PIL import Image
    import PIL
    print(f"   ✅ Pillow {PIL.__version__}")
except ImportError as e:
    print(f"   ❌ Pillow not found: {e}")
    all_passed = False

# darkdetect
try:
    import darkdetect
    print(f"   ✅ darkdetect")
except ImportError as e:
    print(f"   ❌ darkdetect not found: {e}")
    all_passed = False

# typing-extensions
try:
    import typing_extensions
    print(f"   ✅ typing-extensions")
except ImportError as e:
    print(f"   ❌ typing-extensions not found: {e}")
    all_passed = False

print()

# Check 4: Project Files
print("4️⃣  Checking Project Files...")
required_files = [
    "main.py",
    "torrent_client.py",
    "gui.py",
    "requirements.txt",
    "setup.sh",
    "run.sh",
    "test.sh"
]

for file in required_files:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING!")
        all_passed = False

print()

# Check 5: Import Project Modules
print("5️⃣  Checking Project Modules...")

try:
    from torrent_client import TorrentClient
    print("   ✅ TorrentClient can be imported")
except Exception as e:
    print(f"   ❌ Failed to import TorrentClient: {e}")
    all_passed = False

try:
    from gui import TorrentGUI
    print("   ✅ TorrentGUI can be imported")
except Exception as e:
    print(f"   ❌ Failed to import TorrentGUI: {e}")
    all_passed = False

print()

# Check 6: Encryption Configuration
print("6️⃣  Checking Encryption Configuration...")
try:
    from torrent_client import TorrentClient
    client = TorrentClient()
    settings = client.session.get_settings()
    
    # Check encryption settings
    enc_policy = settings.get('out_enc_policy', None)
    if enc_policy is not None:
        print("   ✅ Encryption settings configured")
        print(f"   🔒 Encryption policy: {enc_policy}")
    else:
        print("   ⚠️  Could not verify encryption settings")
    
    print("   ✅ TorrentClient initialized successfully")
except Exception as e:
    print(f"   ❌ Failed to initialize TorrentClient: {e}")
    all_passed = False

print()

# Check 7: Download Directory
print("7️⃣  Checking Download Directory...")
from pathlib import Path
download_dir = Path.home() / "Downloads" / "Torrents"
print(f"   📍 Default location: {download_dir}")
if download_dir.exists():
    print("   ✅ Download directory exists")
else:
    print("   ℹ️  Download directory will be created on first use")

print()

# Final Summary
print("=" * 70)
if all_passed:
    print("✅ ALL CHECKS PASSED!")
    print("=" * 70)
    print()
    print("🎉 Your installation is working correctly!")
    print()
    print("To run the application:")
    print("  ./run.sh")
    print()
    print("Or manually:")
    print("  source venv/bin/activate")
    print("  python main.py")
    print()
else:
    print("❌ SOME CHECKS FAILED!")
    print("=" * 70)
    print()
    print("Please fix the issues above and run this script again.")
    print()
    print("To reinstall:")
    print("  rm -rf venv")
    print("  ./setup.sh")
    print()
    sys.exit(1)

print("=" * 70)
