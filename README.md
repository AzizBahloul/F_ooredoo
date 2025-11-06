# 🚀 Secure Torrent Downloader - Tor-Based Anti-Throttling Edition

A modern, encrypted torrent client specifically designed to bypass ISP throttling through Tor network routing and advanced traffic encryption.

## 🔒 Features

### Anti-Throttling Technology
- **Tor Network Routing**: All traffic routed through Tor SOCKS5 proxy for maximum ISP bypass
- **RC4/MSE Protocol Encryption**: Forced encryption on all BitTorrent connections
- **Deep Packet Inspection (DPI) Bypass**: Traffic obfuscation combined with Tor routing
- **DHT Obfuscation**: Encrypted peer discovery through Tor
- **uTP Protocol Support**: Additional layer to bypass throttling
- **Randomized Ports**: Avoids common BitTorrent port blocking
- **Traffic Pattern Randomization**: Makes it harder to identify torrent traffic

### User Experience
- **Modern GUI**: Built with CustomTkinter for a sleek, dark-themed interface
- **Real-time Progress**: Live download/upload speeds and peer count
- **Tor Status**: Visual indicator showing Tor proxy is active
- **Magnet Link Support**: Just paste and download
- **.torrent File Support**: Browse and select torrent files
- **Multi-torrent Management**: Download multiple files simultaneously

## 📋 Requirements

- Python 3.8 or higher
- Linux, Windows, or macOS
- Tor (installed and running)
- Internet connection (obviously!)

## 🛠️ Installation

### Automated Setup (Recommended)

The easiest way to set up the project is to use the setup script:

```bash
# Navigate to the project directory
cd /home/siaziz/Desktop/foreedo

# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

This will:
- Create a virtual environment (venv)
- Install all system dependencies
- Install all Python packages
- Configure everything properly

### Install Tor

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tor
```

**Fedora:**
```bash
sudo dnf install tor
```

**Arch Linux:**
```bash
sudo pacman -S tor
```

### Manual Installation (Alternative)

If you prefer to install manually:

**Step 1: Install System Dependencies (Linux)**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-libtorrent python3-tk python3-venv tor

# Fedora
sudo dnf install python3-libtorrent python3-tkinter tor

# Arch Linux
sudo pacman -S libtorrent-rasterbar python-libtorrent tk tor
```

**Step 2: Create Virtual Environment**

```bash
# Create virtual environment with Python 3.12 (or python3)
python3.12 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**Step 3: Install Python Packages**

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Running the Application

### Using the Run Script (Recommended)

```bash
# Make the run script executable (first time only)
chmod +x run.sh

# Run the application
./run.sh
```

The run script will:
- Check if Tor is running and start it if needed
- Activate the virtual environment
- Launch the GUI application with Tor proxy enabled

### Running Tests

```bash
# Make the test script executable (first time only)
chmod +x test_run.sh

# Run tests with Tor proxy
./test_run.sh --magnet "your_magnet_link_here"
```

The test script will:
- Check if Tor is running and start it if needed
- Activate the virtual environment
- Run the torrent test with Tor proxy

### Manual Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py

# When done, deactivate
deactivate
```

### Headless Max-Speed CLI (No GUI)

Use the included headless downloader to test maximum speed and bypass ISP throttling:

```bash
# Activate venv
source venv/bin/activate

# Show options
python test_download.py --help

# Run normally (no proxy)
python test_download.py

# Auto-detect local SSH SOCKS5 tunnel on 127.0.0.1:1080 (if you ran: ssh -D 1080 user@server)
python test_download.py --auto-proxy

# Explicitly use a proxy
python test_download.py --use-proxy --proxy socks5://127.0.0.1:1080

# Try TCP-only if your ISP filters UDP/uTP
python test_download.py --no-utp --prefer-tcp

# Force encryption (may reduce peers)
python test_download.py --enc forced
```

See `BYPASS_OOREDOO.md` for more details on setting up an SSH tunnel or VPN.

### Testing Dependencies

```bash
# Make test script executable (first time only)
chmod +x test.sh

# Run tests
./test.sh
```

Or manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Test dependencies
python test_dependencies.py

# Deactivate
deactivate
```

## 🎯 How to Use

### Adding a Torrent

1. **Copy a Magnet Link**:
   - Find a magnet link (starts with `magnet:?xt=urn:btih:...`)
   - Copy it to your clipboard

2. **Add to Downloader**:
   - Paste the magnet link in the input field
   - Click "⬇ Download" button
   - The download will start automatically with encryption enabled!

3. **Or Use a .torrent File**:
   - Click "📁 Browse .torrent" button
   - Select your .torrent file
   - Click "⬇ Download"

### Managing Downloads

- **Pause**: Click the ⏸ button on any torrent
- **Resume**: Click the ▶ button on a paused torrent
- **Remove**: Click the 🗑 button to remove a torrent
- **Change Download Location**: Click "Change" in the bottom status bar

### Monitoring Encryption

- Each torrent card shows "🔒 Encrypted" when encryption is active
- Green color indicates the connection is properly encrypted
- The status changes to "⏳ Connecting..." while finding encrypted peers

## 🔧 Configuration

The application is pre-configured with optimal settings for bypassing ISP throttling:

- **Encryption Mode**: Forced (only encrypted connections)
- **Protocol**: RC4/MSE (Message Stream Encryption)
- **DHT**: Enabled with obfuscation
- **uTP**: Enabled for additional DPI bypass
- **Connection Limit**: 500 peers
- **Speeds**: Unlimited (adjust in code if needed)

To view settings, click the "⚙️ Settings" button in the application.

## 📁 Project Structure

```
fuckOreedooo/
├── main.py              # Application entry point
├── torrent_client.py    # Core torrent client with encryption
├── gui.py               # Modern GUI implementation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🛡️ How It Works

### Bypassing ISP Throttling

1. **Protocol Encryption**: All BitTorrent traffic is encrypted using RC4/MSE, making it unreadable to ISP Deep Packet Inspection (DPI)

2. **Traffic Obfuscation**: The encrypted traffic doesn't have the typical BitTorrent handshake pattern that ISPs look for

3. **Port Randomization**: Using random ports instead of common BitTorrent ports (6881-6889) avoids simple port-based blocking

4. **uTP Protocol**: Micro Transport Protocol adds another layer that helps bypass some throttling mechanisms

5. **DHT Obfuscation**: Peer discovery is also encrypted, hiding your torrent activity

### Why This Works

ISPs typically throttle torrent traffic by:
- Detecting BitTorrent handshake patterns
- Monitoring specific ports
- Deep packet inspection of unencrypted traffic

By encrypting everything and randomizing patterns, your torrent traffic looks like regular HTTPS traffic to your ISP.

## 💡 Tips for Best Performance

1. **Keep the Application Running**: Don't close it immediately after downloads finish - seeding helps the network and your ratio

2. **Popular Torrents**: Work best because more peers support encryption

3. **VPN Combo**: For maximum privacy, combine this with a VPN (though encryption alone defeats throttling)

4. **Firewall**: Make sure to allow the application through your firewall

5. **Antivirus**: Some antivirus software may flag torrent clients - add an exception if needed

## ⚠️ Legal Notice

This software is designed to bypass unfair ISP throttling on **legal torrent traffic**. 

- Always respect copyright laws in your country
- Only download content you have the right to download
- This tool is for educational purposes and legitimate use cases
- The developers are not responsible for any misuse

## 🐛 Troubleshooting

### "No module named 'libtorrent'" Error

Install libtorrent:
```bash
pip install libtorrent
```

If that doesn't work, install system package:
```bash
# Ubuntu/Debian
sudo apt-get install python3-libtorrent
```

### "No module named 'customtkinter'" Error

Install CustomTkinter:
```bash
pip install customtkinter
```

### Downloads Are Slow

- Check if you have encrypted peers (look for the 🔒 indicator)
- Try a more popular torrent (more peers = better speeds)
- Verify your internet connection speed
- Some ISPs still throttle even with encryption (consider using a VPN)

### Application Won't Start

Make sure you have Python 3.8+:
```bash
python3 --version
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🔮 Future Enhancements

Potential features for future versions:
- Built-in VPN integration
- Bandwidth limiting options
- RSS feed support for automatic downloads
- Download scheduling
- Torrent search integration
- Mobile companion app

## 📝 License

This project is provided as-is for educational purposes. Use responsibly and legally.

## 🤝 Contributing

Feel free to improve this project! Some areas that could use work:
- Better error handling
- More encryption options
- Performance optimizations
- Additional obfuscation techniques

## 📧 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Make sure all dependencies are installed
3. Verify you're using Python 3.8+
4. Check your firewall settings

---

**Made with ❤️ to fight unfair ISP throttling**

*Remember: Encryption is your right. Privacy matters.* 🔒

