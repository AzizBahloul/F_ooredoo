#!/bin/bash

# test_run.sh
# Run test script with Tor proxy
# Automatically activates venv and runs the test

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
echo "🚀 Starting test with Tor proxy..."
source venv/bin/activate

# Run the test script
python test_download.py "$@"

# Deactivate when done
deactivate