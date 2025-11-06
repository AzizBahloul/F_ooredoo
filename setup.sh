#setup.sh

# Setup script for Secure Torrent Downloader
# This creates a virtual environment and installs all dependencies properly

echo "🚀 Secure Torrent Downloader - Setup Script"
echo "=================================================="
echo ""

# Check if Python 3.12 is installed
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 is not installed!"
    echo "Trying to use python3 instead..."
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python3.12"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"
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

# Remove old venv if it exists
if [ -d "venv" ]; then
    echo "🗑️  Removing old virtual environment..."
    rm -rf venv
    echo ""
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment!"
    echo "Make sure you have python3-venv installed:"
    echo "  sudo apt-get install python3-venv"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Setup Complete!"
    echo "=================================================="
    echo ""
    echo "To run the application:"
    echo "  1. Activate the virtual environment:"
    echo "     source venv/bin/activate"
    echo ""
    echo "  2. Run the application:"
    echo "     python main.py"
    echo ""
    echo "Or use the run script:"
    echo "  ./run.sh"
    echo ""
    echo "To test dependencies:"
    echo "  source venv/bin/activate"
    echo "  python test_dependencies.py"
    echo ""
    echo "🔒 Remember: This app uses encryption to bypass ISP throttling!"
    echo "=================================================="
else
    echo "⚠️  Some packages failed to install."
    echo "Please check the error messages above."
    exit 1
fi
