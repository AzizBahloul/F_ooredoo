#install.sh

# Installation script for Secure Torrent Downloader
# Makes installation easy and automated

echo "🚀 Secure Torrent Downloader - Installation Script"
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo "Installing pip3..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

echo "✓ pip3 is available"
echo ""

# Install system dependencies for libtorrent (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Installing system dependencies..."
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        echo "Detected Debian/Ubuntu system"
        sudo apt-get update
        sudo apt-get install -y python3-libtorrent python3-tk
    elif command -v dnf &> /dev/null; then
        echo "Detected Fedora system"
        sudo dnf install -y python3-libtorrent python3-tkinter
    elif command -v pacman &> /dev/null; then
        echo "Detected Arch Linux system"
        sudo pacman -S --noconfirm libtorrent-rasterbar python-libtorrent tk
    else
        echo "⚠️  Unknown Linux distribution - you may need to install libtorrent manually"
    fi
    echo ""
fi

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt --user

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully!"
else
    echo "⚠️  Some packages failed to install. Trying alternative method..."
    pip3 install libtorrent customtkinter Pillow darkdetect typing-extensions --user
fi

echo ""
echo "=================================================="
echo "✅ Installation Complete!"
echo "=================================================="
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Or make it executable and run directly:"
echo "  chmod +x main.py"
echo "  ./main.py"
echo ""
echo "🔒 Remember: This app uses encryption to bypass ISP throttling!"
echo "=================================================="
