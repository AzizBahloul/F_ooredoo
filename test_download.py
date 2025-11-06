#!/usr/bin/env python3
"""
OOREDOO ISP BYPASS VERSION
Your ISP is blocking UDP - this uses HTTP trackers and TCP-only
"""

import libtorrent as lt
import time
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="ISP-bypass torrent downloader")
    parser.add_argument("--magnet", help="Magnet link")
    parser.add_argument("--path", default="./downloads", help="Download path")
    parser.add_argument("--use-proxy", action="store_true", help="Use SOCKS5 proxy (Tor recommended)")
    parser.add_argument("--proxy-host", default="127.0.0.1", help="Proxy host (default: 127.0.0.1)")
    parser.add_argument("--proxy-port", type=int, default=9050, help="Proxy port (default: 9050 for Tor)")
    return parser.parse_args()


TEST_MAGNETS = {
    "bigbuck": "magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c&dn=Big+Buck+Bunny",
    "ubuntu": "magnet:?xt=urn:btih:9f9165d9a281a9b8e782cd5176bbcc8256fd1871&dn=Ubuntu"
}

args = parse_args()

print("=" * 80)
print("🚨 TOR-BASED ANTI-THROTTLING MODE")
print("=" * 80)
print()

if not args.use_proxy:
    print("⚠️  WARNING: Using Tor proxy for maximum ISP bypass!")
    print("⚠️  Make sure Tor is running: tor")
    print()
    print("Quick fix:")
    print("  1. Install Tor: sudo apt install tor")
    print("  2. Start Tor: tor")
    print("  3. Then run: python test_download.py --use-proxy")
    print()
    print("Forcing Tor proxy mode...")
    args.use_proxy = True
    print()

# Select magnet
if args.magnet:
    magnet = TEST_MAGNETS.get(args.magnet, args.magnet)
else:
    magnet = TEST_MAGNETS["bigbuck"]
    print("📝 Using Big Buck Bunny test torrent")

print(f"   Hash: {magnet[20:60]}...")
print()

# Create session
ses = lt.session()

print("⚡ Configuring ANTI-OOREDOO settings...")

# OOREDOO-SPECIFIC SETTINGS
settings = {
    # DISABLE UDP - Ooredoo blocks it!
    'enable_outgoing_utp': False,  # ❌ UDP blocked by ISP
    'enable_incoming_utp': False,  # ❌ UDP blocked by ISP
    
    # FORCE TCP ONLY
    'enable_outgoing_tcp': True,   # ✅ TCP works
    'enable_incoming_tcp': True,   # ✅ TCP works
    'mixed_mode_algorithm': lt.bandwidth_mixed_algo_t.prefer_tcp,
    
    # ENCRYPTION - Try to hide from DPI
    'out_enc_policy': lt.enc_policy.enabled,  # Prefer encrypted
    'in_enc_policy': lt.enc_policy.enabled,
    'allowed_enc_level': lt.enc_level.both,   # Allow both for more peers
    'prefer_rc4': True,
    
    # DHT - Keep enabled (uses UDP but worth trying)
    'enable_dht': True,
    'enable_lsd': True,
    'enable_upnp': True,
    'enable_natpmp': True,
    
    # TRACKERS - Announce aggressively
    'announce_to_all_trackers': True,
    'announce_to_all_tiers': True,
    'tracker_completion_timeout': 60,
    'tracker_receive_timeout': 30,
    'auto_manage_interval': 15,
    
    # CONNECTIONS
    'connections_limit': 200,  # Lower since we're limited
    'max_peerlist_size': 1000,
    'unchoke_slots_limit': 50,
    
    # SPEEDS - Unlimited
    'download_rate_limit': 0,
    'upload_rate_limit': 0,  # Upload helps get peers
    
    # AGGRESSIVE PEER DISCOVERY
    'peer_connect_timeout': 15,
    'request_timeout': 45,
    'peer_timeout': 180,
    
    # CACHE
    'cache_size': 512,
    'max_queued_disk_bytes': 3 * 1024 * 1024,
}

ses.apply_settings(settings)

# PROXY - TOR-BASED BYPASS
if args.use_proxy:
    print(f"✅ Using TOR SOCKS5 proxy: {args.proxy_host}:{args.proxy_port}")
    print("   This will bypass ISP throttling through Tor network!")
    ses.apply_settings({
        'proxy_type': lt.proxy_type_t.socks5,
        'proxy_hostname': args.proxy_host,
        'proxy_port': args.proxy_port,
        'proxy_hostnames': True,
        'proxy_peer_connections': True,
        'proxy_tracker_connections': True,
        'force_proxy': True,
    })
else:
    print("❌ ERROR: Tor proxy is required!")
    exit(1)

# DHT bootstrap (try even though UDP blocked)
for node in [("router.bittorrent.com", 6881), ("dht.transmissionbt.com", 6881)]:
    ses.add_dht_node(node)

# Alerts
ses.set_alert_mask(lt.alert.category_t.all_categories)

# Port
import random
port = random.randint(50000, 60000)
ses.apply_settings({'listen_interfaces': f'0.0.0.0:{port}'})
print(f"🔌 Port: {port}")
print()

# Parse magnet
print("🧲 Parsing magnet...")
atp = lt.parse_magnet_uri(magnet)
atp.save_path = args.path

# HTTP/HTTPS TRACKERS ONLY (UDP is blocked by Ooredoo!)
print("📡 Adding HTTP/HTTPS trackers (UDP blocked by ISP)...")
HTTP_TRACKERS = [
    # HTTP trackers that work without UDP
    "http://tracker.opentrackr.org:1337/announce",
    "https://tracker.tamersunion.org:443/announce",
    "http://tracker.gbitt.info/announce",
    "http://tracker1.itzmx.com:8080/announce",
    "http://tracker.files.fm:6969/announce",
    "http://retracker.local.msn-net.ru/announce",
    "http://tracker2.itzmx.com:6961/announce",
    "http://open.acgnxtracker.com:80/announce",
    "https://tracker.nanoha.org:443/announce",
    "https://tracker.lelux.fi:443/announce",
    "http://tracker.mywaifu.best:6969/announce",
    "https://tracker.cloudit.top:443/announce",
    "http://tracker.ipv6tracker.ru:80/announce",
    "http://t.nyaatracker.com:80/announce",
    "http://share.camoe.cn:8080/announce",
]

# ALSO try some UDP (in case proxy works)
if args.use_proxy:
    UDP_TRACKERS = [
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://open.stealth.si:80/announce",
        "udp://exodus.desync.com:6969/announce",
        "udp://tracker.torrent.eu.org:451/announce",
        "udp://explodie.org:6969/announce",
    ]
    HTTP_TRACKERS.extend(UDP_TRACKERS)
    print("   (Also trying UDP through proxy)")

# Set trackers
atp.trackers = HTTP_TRACKERS
for i in range(len(HTTP_TRACKERS)):
    atp.tracker_tiers.append(i % 3)

print(f"   ✅ Added {len(HTTP_TRACKERS)} trackers")

# Storage
atp.storage_mode = lt.storage_mode_t.storage_mode_sparse
atp.flags |= lt.torrent_flags.auto_managed

# Add
print()
print("➕ Adding to session...")
h = ses.add_torrent(atp)

print("=" * 80)
print("⏳ CONNECTING (may take 30-60s on Ooredoo ISP)...")
print("=" * 80)
print()

start = time.time()
got_metadata = False
got_peers = False
working_trackers = []

try:
    while True:
        elapsed = int(time.time() - start)
        
        if elapsed > 120:
            print("\n\n⏰ 2 minutes - no good connection")
            print("\n🔍 DIAGNOSIS:")
            s = h.status()
            print(f"   Peers: {s.num_peers}")
            print(f"   Seeds: {s.num_seeds}")
            print(f"   Speed: {s.download_rate / 1024:.1f} KB/s")
            print(f"   Working trackers: {len(working_trackers)}")
            print()
            
            if len(working_trackers) == 0:
                print("❌ NO TRACKERS WORKING!")
                print()
                print("Your ISP (Ooredoo) is blocking torrent traffic.")
                print()
                print("SOLUTIONS:")
                print("  1. Get a VPN (ProtonVPN free tier works)")
                print("  2. Use mobile hotspot (4G/5G not throttled)")
                print("  3. SSH tunnel: ssh -D 1080 user@vps.com")
                print("     Then: python test_download.py --use-proxy")
                print("  4. Try Tor: brew install tor; tor")
                print("     Then: python test_download.py --use-proxy --proxy-port 9050")
            else:
                print(f"✅ {len(working_trackers)} trackers working")
                print("   But still no peers - torrent might be dead")
                print("   Try: python test_download.py --magnet bigbuck")
            
            break
        
        s = h.status()
        
        # Metadata
        if not got_metadata and s.has_metadata:
            got_metadata = True
            print(f"\n✅ Metadata: {h.torrent_file().name()}")
            print(f"   Size: {s.total_wanted / (1024**3):.2f} GB\n")
        
        # Peers
        if not got_peers and s.num_peers > 0:
            got_peers = True
            print(f"\n🎉 {s.num_peers} peers connected!\n")
        
        # Progress
        prog = s.progress * 100
        bar = '█' * int(prog / 2) + '░' * (50 - int(prog / 2))
        
        dl = s.download_rate / (1024 * 1024)
        ul = s.upload_rate / (1024 * 1024)
        
        print(f"\r{bar} {prog:.1f}% | ⬇ {dl:.2f} MB/s | ⬆ {ul:.2f} MB/s | ", end='')
        print(f"👥 {s.num_peers} ({s.num_seeds} seeds) | ", end='')
        
        if s.total_wanted > 0:
            done = s.total_wanted_done / (1024**3)
            total = s.total_wanted / (1024**3)
            print(f"📦 {done:.2f}/{total:.2f} GB", end='')
        
        print("  " * 5, end='')
        sys.stdout.flush()
        
        # Alerts
        alerts = ses.pop_alerts()
        for a in alerts:
            name = type(a).__name__
            
            if 'tracker_reply' in name:
                if a.url not in working_trackers:
                    working_trackers.append(a.url)
                    tracker_type = "HTTP" if a.url.startswith("http") else "UDP"
                    print(f"\n✅ {tracker_type} tracker OK: {a.url[:60]}")
            
            elif 'tracker_error' in name or 'tracker_warning' in name:
                # Only show UDP failures if no proxy
                if not args.use_proxy or not a.url.startswith("udp"):
                    pass  # Silent - we know UDP is blocked
            
            elif 'dht_bootstrap' in name:
                print(f"\n✅ DHT bootstrapped (may help find peers)")
        
        # Done?
        if s.is_seeding:
            print("\n\n✅ COMPLETE!")
            break
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\n\n⏸️  Stopped")

print("\n")
ses.pause()