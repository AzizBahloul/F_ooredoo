#!/bin/bash
# Upload package to PPA: ppa:siaziz/fuckooredoo

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     🚀 Upload to PPA: ppa:siaziz/fuckooredoo 🚀          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Your GPG key ID (last 8 chars of fingerprint)
GPG_KEY_ID="$(cat /tmp/gpg_key_id.txt 2>/dev/null || echo 'C29E265F')"
PPA_URL="ppa:siaziz/fuckooredoo"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "debian" ]; then
    echo -e "${RED}❌ Error: Run this script from the project root directory!${NC}"
    exit 1
fi

# Check GPG key
echo "🔑 Checking GPG key..."
if ! gpg --list-secret-keys | grep -q "$GPG_KEY_ID"; then
    echo -e "${RED}❌ GPG key $GPG_KEY_ID not found in keyring!${NC}"
    echo ""
    echo "Available keys:"
    gpg --list-secret-keys --keyid-format=long
    exit 1
fi
echo -e "${GREEN}✓ GPG key found${NC}"
echo ""

# Check dput configuration
echo "📋 Checking dput configuration..."
if [ ! -f ~/.dput.cf ]; then
    echo -e "${YELLOW}⚠️  ~/.dput.cf not found. Creating it...${NC}"
    cat > ~/.dput.cf << 'EOFCONFIG'
[siaziz-fuckooredoo]
fqdn = ppa.launchpad.net
method = ftp
incoming = ~siaziz/ubuntu/fuckooredoo/
login = anonymous
allow_unsigned_uploads = 0

[ppa]
fqdn = ppa.launchpad.net
method = ftp
incoming = ~siaziz/ubuntu/
login = anonymous
allow_unsigned_uploads = 0
EOFCONFIG
    echo -e "${GREEN}✓ dput configuration created${NC}"
else
    echo -e "${GREEN}✓ dput configuration exists${NC}"
fi
echo ""

# Clean previous build artifacts
echo "🧹 Cleaning previous build artifacts..."
rm -f ../*.upload
rm -f ../*.changes
rm -f ../*.dsc
rm -f ../*.tar.*
rm -f ../*.buildinfo
echo -e "${GREEN}✓ Cleaned${NC}"
echo ""

# Build source package
echo "🔨 Building signed source package..."
echo -e "${BLUE}   (This will prompt for your GPG passphrase)${NC}"
echo ""

debuild -S -sa -k"$GPG_KEY_ID"

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Build failed!${NC}"
    echo ""
    echo "Common issues:"
    echo "  - GPG passphrase incorrect"
    echo "  - Missing build dependencies (run: sudo apt install build-essential devscripts)"
    echo "  - Syntax errors in debian/ files"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Source package built successfully!${NC}"
echo ""

# Check with lintian
echo "🔍 Running quality checks..."
CHANGES_FILE=$(ls -t ../*_source.changes 2>/dev/null | head -n1)

if [ -n "$CHANGES_FILE" ]; then
    lintian "$CHANGES_FILE" || true
    echo ""
else
    echo -e "${RED}❌ No .changes file found!${NC}"
    exit 1
fi

# Show what will be uploaded
echo "📦 Package to be uploaded:"
echo "   $(basename "$CHANGES_FILE")"
echo ""
echo "📄 Contents:"
cat "$CHANGES_FILE"
echo ""

# Ask for confirmation
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Ready to upload to: $PPA_URL${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
read -p "Continue with upload? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Upload cancelled."
    exit 0
fi

# Upload to PPA
echo ""
echo "📤 Uploading to PPA..."
echo ""

dput "$PPA_URL" "$CHANGES_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              ✅ Upload Successful! ✅                     ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "📧 Next steps:"
    echo "   1. Check your email (azizbahloul3@gmail.com) for acceptance/rejection"
    echo "   2. Wait for builds to complete (~15-30 minutes)"
    echo "   3. Monitor progress at:"
    echo "      https://launchpad.net/~siaziz/+archive/ubuntu/fuckooredoo"
    echo ""
    echo "📊 Build status timeline:"
    echo "   • Upload accepted: ~5 minutes"
    echo "   • Build starts: ~10 minutes"
    echo "   • Build completes: ~30 minutes"
    echo "   • Package published: ~60 minutes"
    echo ""
    echo "🎉 Once published, users can install with:"
    echo "   sudo add-apt-repository ppa:siaziz/fuckooredoo"
    echo "   sudo apt-get update"
    echo "   sudo apt-get install fuckooredoo"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Upload failed!${NC}"
    echo ""
    echo "Common issues:"
    echo "  - GPG key not validated on Launchpad (check your email)"
    echo "  - Package already uploaded (increment version with: dch -i)"
    echo "  - Network issues (try again)"
    echo ""
    exit 1
fi
