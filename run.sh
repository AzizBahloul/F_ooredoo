#run.sh

# Run script for Secure Torrent Downloader
# Automatically activates venv and runs the application

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  ./setup.sh"
    exit 1
fi

# Check if Tor is running
if ! pgrep -x "tor" > /dev/null; then
    echo "⚠️  Tor is not running!"
    echo "Starting Tor..."
    tor &
    sleep 5
fi

# Activate virtual environment
echo "🚀 Starting Secure Torrent Downloader..."
source venv/bin/activate

# Run the application
python main.py

# Deactivate when done
deactivate
