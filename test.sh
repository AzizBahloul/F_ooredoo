#test.sh

# Test script for Secure Torrent Downloader
# Tests dependencies and runs verification

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🧪 Testing Secure Torrent Downloader..."
echo ""
source venv/bin/activate

# Run comprehensive verification
python verify.py

TEST_RESULT=$?

# Deactivate when done
deactivate

exit $TEST_RESULT
