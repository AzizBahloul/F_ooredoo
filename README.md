# 🖕 F**k Ooredoo - The Ultimate "Fuck You" to ISP Throttling

**Version 1.0.2** by **Mohamed Aziz Bahloul**

## 😤 Why This Exists

So Ooredoo thinks they can **fuck with our torrents**, huh? They think throttling our bandwidth and blocking our downloads is cool? **FUCK THAT NOISE.**

This isn't just a torrent client. This is a **middle finger wrapped in encryption, delivered through Tor, straight to Ooredoo's DPI systems.**

[![PyPI version](https://img.shields.io/pypi/v/fuckooredoo.svg)](https://pypi.org/project/fuckooredoo/)
[![Fuck Throttling](https://img.shields.io/badge/Fuck-Throttling-red.svg)]()
[![Fuck DPI](https://img.shields.io/badge/Fuck-DPI-orange.svg)]()
[![Made With Spite](https://img.shields.io/badge/Made%20With-Spite-purple.svg)]()

---

## 🔥 What Makes This Special?

### It Says "Fuck You" to Ooredoo in 7 Different Ways:

1. **🧅 Tor Routing** - All your traffic goes through Tor. Ooredoo can't see shit.
2. **🔒 RC4/MSE Encryption** - Every single packet is encrypted. Good luck reading that, assholes.
3. **🎭 Traffic Obfuscation** - Your torrent traffic looks like HTTPS. Fuck their pattern recognition.
4. **🎲 Random Ports** - Different port every time. No more port blocking bullshit.
5. **🕵️ DHT Obfuscation** - Even peer discovery is encrypted. Can't block what you can't see.
6. **⚡ uTP Protocol** - Extra layer of "go fuck yourself" to their DPI.
7. **🎪 Traffic Randomization** - Makes your torrent traffic look completely innocent.

### The Result?

**Ooredoo's throttling system can go fuck itself. Seriously.**

---

## 🎯 The Features (A.K.A. "Fuck You" Features)

### 🖕 Anti-Throttling Arsenal
- **Tor Network Routing**: Because fuck Ooredoo's packet inspection
- **Forced Encryption**: RC4/MSE on EVERY connection - no exceptions, no mercy
- **DPI Bypass**: Deep Packet Inspection? More like Deep Packet FUCK YOU
- **DHT Through Tor**: Even finding peers is anonymous and encrypted
- **Smart Speed Optimization**: 2000+ peer connections, 10MB/s upload for better ratios
- **Ultra-Aggressive Settings**: We're not here to play nice

### 🎨 User Experience (Because We're Not Total Savages)
- **Modern Dark UI**: CustomTkinter because we have standards (unlike Ooredoo)
- **Real-time Stats**: Watch as your torrents fly past Ooredoo's throttling attempts
- **Tor Status Indicator**: Green checkmark = Ooredoo is crying
- **Magnet Link Support**: Copy, paste, watch Ooredoo fail
- **Multi-torrent Management**: Download all the things while Ooredoo watches helplessly
- **Cross-Platform**: Windows, Linux, macOS - fuck Ooredoo everywhere

---

## 💀 Requirements

- **Python 3.8+** - To run the code
- **Tor** - To flip off Ooredoo properly
- **Internet** - Even throttled Ooredoo internet works (barely)
- **Attitude** - You should be at least 60% angry at ISP throttling

---

## 🚀 Installation (Let's Fucking Go)

### Step 1: Install Tor (Your New Best Friend)

**Ubuntu/Debian** (Fuck yeah, open source):
```bash
sudo apt update && sudo apt install tor
sudo systemctl start tor
# Watch Ooredoo's throttling become useless
```

**Fedora** (For the cool kids):
```bash
sudo dnf install tor
sudo systemctl start tor
```

**Arch** (I use Arch btw):
```bash
sudo pacman -S tor
sudo systemctl start tor
```

**macOS** (Even Apple users deserve freedom):
```bash
brew install tor
brew services start tor
```

**Windows** (Yes, even you):
- Download Tor Browser: [torproject.org](https://www.torproject.org/download/)
- Or: `choco install tor`

### Step 2: Install This Badass Tool

#### Option A: APT Install (Ubuntu/Debian - Recommended) 🎯

**The easiest way to install - includes all dependencies automatically:**

```bash
# Add the PPA repository
sudo add-apt-repository ppa:azizbahloul/fuckooredoo
sudo apt-get update

# Install (includes Tor and all dependencies)
sudo apt-get install fuckooredoo

# Done! Launch it:
fuckooredoo
```

**Why use APT?**
- ✅ Automatic dependency installation (including Tor)
- ✅ Tor service auto-configured and started
- ✅ System-wide installation
- ✅ Easy updates with `apt upgrade`
- ✅ Man page included: `man fuckooredoo`
- ✅ Desktop integration

#### Option B: PyPI Install (All Platforms)

```bash
pip install fuckooredoo
```

**Note:** If using PyPI, you must manually install and start Tor (see Step 1).

#### Option C: Direct .deb (no PPA needed)

If the Launchpad PPA is unavailable or you prefer a direct install, you can install the provided Debian package (.deb) or build one locally from this repository.

- Install a downloaded .deb (for example, from the project's GitHub Releases):

```bash
# from the folder where you downloaded the file
sudo dpkg -i fuckooredoo_1.0.4-2_all.deb
sudo apt-get install -f    # fix and install any missing dependencies
```

- Build and install locally (use this if you changed code or want the latest from source):

```bash
# from the project root (/home/you/F_ooredoo)
./build_deb.sh
sudo dpkg -i ../fuckooredoo_*.deb
sudo apt-get install -f
```

This creates a system package with desktop integration, a man page, and automatic service handling.

> Tip: if you don't want a system package, `pip install .` (from the repo root) will install the Python package into your environment, but you'll need to manage Tor and desktop integration yourself.

#### Download .deb (clickable link)

You can download the latest .deb from the project's GitHub Releases page. Click the link below to open the Releases page and grab the most recent .deb asset for your system:

[Download the latest .deb from Releases](https://github.com/AzizBahloul/F_ooredoo/releases/latest)

If you prefer a direct asset link and know the exact release/tag and filename, the URL format is:

```
https://github.com/AzizBahloul/F_ooredoo/releases/download/<tag>/<filename>.deb
```

Example:

```
https://github.com/AzizBahloul/F_ooredoo/releases/download/v1.0.4/fuckooredoo_1.0.4-2_all.deb
```

### Step 3: Launch and Watch Magic Happen

```bash
fuckooredoo
```

**What happens next:**
- ✅ Checks if Tor is ready to fuck shit up
- ✅ Verifies Ooredoo can't see your traffic
- ✅ Launches the most beautiful "fuck you" to ISP throttling ever created
- ✅ Routes EVERYTHING through Tor with military-grade encryption

---

## 🎮 How to Use This Beast

### Basic Mode (For Beginners)

1. **Start the app:**
   ```bash
   fuckooredoo
   ```

2. **Add a magnet link:**
   - Copy any magnet link (the ones Ooredoo hates)
   - Paste that shit in the input field
   - Click "⬇ Download"
   - Watch Ooredoo's throttling fail miserably

3. **Or use a .torrent file:**
   - Click "📁 Browse .torrent"
   - Select your file
   - Watch the magic

### Headless Mode (For Servers and Extra Badassery)

```bash
# Basic headless mode
fuckooredoo --headless

# With magnet link
fuckooredoo --headless --magnet "magnet:?xt=urn:btih:..."
```

### Managing Downloads

- **⏸ Pause**: When you need a break from watching Ooredoo fail
- **▶ Resume**: To resume watching Ooredoo fail
- **🗑 Remove**: Clean up completed downloads
- **📂 Change Path**: Store your files wherever the fuck you want

---

## 🛡️ How We Fuck Ooredoo's Throttling

### The Technical "Fuck You"

1. **Step 1: Tor Routing**
   - Every single bit goes through Tor (port 9050)
   - Ooredoo sees: `????????`
   - Actual traffic: `YOUR GLORIOUS TORRENTS`

2. **Step 2: RC4/MSE Encryption**
   - All BitTorrent traffic is encrypted with RC4
   - Ooredoo's DPI: *confused screaming*
   - Your downloads: **MAXIMUM SPEED**

3. **Step 3: Traffic Obfuscation**
   - Makes torrent traffic look like normal HTTPS
   - Ooredoo: "Is this... Netflix?"
   - You: "Sure, let's go with that 😏"

4. **Step 4: Random Everything**
   - Random ports every session
   - Random timing patterns
   - Random packet sizes
   - Ooredoo's pattern detection: **COMPLETELY FUCKED**

### Why This Works

Because Ooredoo's throttling is:
- ❌ Lazy as fuck
- ❌ Based on obvious patterns
- ❌ Vulnerable to basic encryption
- ❌ No match for Tor + Encryption combo
- ❌ Basically useless against this tool

---

## 🎪 The Stats (Prepare to Be Impressed)

**Before F_ooredoo:**
- Download speed: 50 KB/s (thanks Ooredoo, you cheap fucks)
- Upload speed: lol what upload?
- Peers: 5 (Ooredoo blocked the rest)
- Your mood: 😠

**After F_ooredoo:**
- Download speed: **AS FAST AS YOUR ACTUAL CONNECTION**
- Upload speed: **HELPING THE COMMUNITY**
- Peers: **200+ concurrent connections**
- Your mood: 😎🖕

---

## 💡 Pro Tips (From One Rebel to Another)

### Optimization

1. **Keep Tor Running 24/7**
   - Tor is your shield against Ooredoo's bullshit
   - The app shows a green checkmark when Tor is active
   - If Tor stops, restart it ASAP

2. **Choose Popular Torrents**
   - More peers = faster downloads
   - Even with encryption, popular = better

3. **Seed After Downloading**
   - Don't be a leech
   - Sharing is caring
   - Plus it pisses off Ooredoo even more

4. **Firewall Configuration**
   - Allow the app through your firewall
   - Or just disable Windows Firewall (we're rebels, remember?)

### Troubleshooting

**"Tor is not running"**
```bash
# Fix that shit
sudo systemctl start tor  # Linux
brew services start tor    # macOS
# Windows: Just run Tor Browser
```

**"Still slow"**
- Check if Tor is ACTUALLY running (green checkmark)
- Try a more popular torrent
- Restart Tor: `sudo systemctl restart tor`
- Blame Ooredoo's shit infrastructure

**"No module named 'tkinter'"**
```bash
# Linux
sudo apt install python3-tk

# macOS  
brew install python-tk

# Windows
Reinstall Python from python.org and CHECK THE TCL/TK BOX
```

---

## ⚠️ Legal Shit (Because We Have To)

**DISCLAIMER:**

This tool is designed to bypass **UNJUST and ANTI-CONSUMER ISP throttling** on **LEGAL torrent traffic**.

### What This Tool Is For:
- ✅ Downloading Linux ISOs faster
- ✅ Torrenting open-source software
- ✅ Getting around unfair ISP throttling
- ✅ Exercising your right to privacy
- ✅ Telling Ooredoo to go fuck themselves (legally)

### What This Tool Is NOT For:
- ❌ Piracy (don't be a dick)
- ❌ Illegal downloads (seriously, don't)
- ❌ Copyright infringement (we're rebels, not criminals)

### Real Talk:
- Use this responsibly
- Only download legal content
- Respect copyright laws in your country
- We're fighting against ISP fuckery, not breaking laws
- The developers are not responsible if you do stupid shit

**Remember:** We're here to fight UNFAIR THROTTLING, not promote piracy. Ooredoo's throttling is bullshit, but that doesn't mean piracy is okay.

---

## 🎓 How Ooredoo's Throttling Works (And Why It's Trash)

### Their "Strategy" (LOL)

1. **Deep Packet Inspection (DPI)**
   - Looks at your traffic patterns
   - Identifies BitTorrent-like behavior
   - **Solution**: We encrypt everything, GG Ooredoo

2. **Port Blocking**
   - Blocks common BitTorrent ports (6881-6889)
   - **Solution**: We use random ports, LOL

3. **Protocol Detection**
   - Tries to identify BitTorrent protocol
   - **Solution**: Everything looks like HTTPS through Tor, nice try

4. **Speed Limiting**
   - Slows down "suspicious" traffic
   - **Solution**: Our traffic isn't suspicious, it's encrypted AF

### Why This Tool Destroys Their System

```
Ooredoo's DPI: "Is this BitTorrent?"
Our Encrypted Traffic: "¯\_(ツ)_/¯"
Ooredoo: "I... I don't know what to do"
Your Downloads: *GOING AT FULL SPEED*
```

---

## 🔮 Future Plans (Making Ooredoo Cry More)

- [ ] Multiple proxy support (Tor + I2P + others)
- [ ] Bandwidth scheduling (download at night, seed during day)
- [ ] RSS feed automation (set it and forget it)
- [ ] Even more aggressive anti-throttling
- [ ] Mobile app (fuck Ooredoo on your phone too)
- [ ] Built-in VPN support (triple encryption, why not?)
- [ ] Statistics page showing "Money Saved by Not Paying for VPN"

---

## 🤝 Contributing

Want to help make Ooredoo cry even more? Contributions welcome!

**Areas where you can help:**
- More anti-throttling techniques
- Better obfuscation methods
- Performance optimization
- Cross-platform improvements
- Documentation (make it even funnier)
- Testing on different ISPs (fuck them all equally)

---

## 🏆 Hall of Fame

**People Who Said "Fuck Ooredoo" Before It Was Cool:**
- Mohamed Aziz Bahloul (that's me! 🎉)
- You (once you use this tool)
- Everyone who's tired of ISP bullshit

---

## 📱 Connect

**Author:** Mohamed Aziz Bahloul  
**GitHub:** [@AzizBahloul](https://github.com/AzizBahloul)  
**Project:** [F_ooredoo](https://github.com/AzizBahloul/F_ooredoo)  
**Email:** azizbahloul3@gmail.com

**Found a bug?** Report it  
**Have a feature idea?** Suggest it  
**Want to say thanks?** ⭐ the repo  
**Want to really say thanks?** Contribute code

---

## 📜 License

MIT License - Because Freedom

Copyright (c) 2025 Mohamed Aziz Bahloul

**Translation:** Do whatever the fuck you want with this code, just don't sue me.

---

## 🎉 Final Words

To Ooredoo: **This is what happens when you fuck with the wrong developers.**

To Users: **Download responsibly, seed generously, and never let ISPs control you.**

To Everyone Else: **Share this tool. Let's make ISP throttling a thing of the past.**

---

### Made with 😠 Anger, 💻 Code, and 🖕 Pure Spite

**Remember:** We're not just downloading torrents. We're fighting for digital freedom, one encrypted packet at a time.

#### Now go forth and download at full speed, you beautiful rebel. 🚀

---

## 🎸 Easter Eggs

If you read this far, you're a real one. Here's a secret:

```bash
# The nuclear option (maximum fuck you to Ooredoo)
export TORRENT_PEERS=9999
export UPLOAD_SPEED=unlimited
fuckooredoo --headless --aggressive-mode
```

*(Note: aggressive-mode doesn't actually exist, but wouldn't that be cool?)*

---

**P.S.** If you work for Ooredoo and you're reading this: Fix your shit. Stop throttling legal traffic. Do better.

**P.P.S.** If you're a user: Enjoy your full-speed downloads! You deserve it! 🎊