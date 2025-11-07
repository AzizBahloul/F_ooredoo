#!/bin/bash
# Build Debian package for fuckooredoo

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     🖕 F**k Ooredoo - Debian Package Builder 🖕          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check for required tools
echo "📦 Checking build dependencies..."
MISSING_DEPS=()

if ! command -v dpkg-buildpackage &> /dev/null; then
    MISSING_DEPS+=("dpkg-dev")
fi

if ! command -v dh &> /dev/null; then
    MISSING_DEPS+=("debhelper")
fi

if ! command -v dh_python3 &> /dev/null; then
    MISSING_DEPS+=("dh-python")
fi

if ! command -v lintian &> /dev/null; then
    MISSING_DEPS+=("lintian")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Missing dependencies: ${MISSING_DEPS[*]}${NC}"
    echo "Installing required packages..."
    sudo apt-get update
    sudo apt-get install -y build-essential devscripts debhelper dh-python python3-all python3-setuptools lintian
fi

echo -e "${GREEN}✓ All build dependencies are installed${NC}"
echo ""

# Clean previous build artifacts
echo "🧹 Cleaning previous build artifacts..."
rm -rf debian/fuckooredoo
rm -rf debian/.debhelper
rm -f debian/debhelper-build-stamp
rm -f debian/files
rm -f debian/*.log
rm -f debian/*.substvars
rm -rf debian/tmp
rm -f ../*.deb
rm -f ../*.changes
rm -f ../*.buildinfo
rm -f ../*.dsc
rm -f ../*.tar.*

echo -e "${GREEN}✓ Clean complete${NC}"
echo ""

# Make maintainer scripts executable
echo "🔧 Setting up maintainer scripts..."
chmod +x debian/rules
chmod +x debian/postinst
chmod +x debian/prerm
chmod +x debian/postrm

echo -e "${GREEN}✓ Maintainer scripts configured${NC}"
echo ""

# Build the package
echo "🔨 Building Debian package..."
echo ""

dpkg-buildpackage -us -uc -b

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║           ✅ Package Built Successfully! ✅               ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Package files created:"
    ls -lh ../*.deb 2>/dev/null || echo "  (no .deb files found)"
    echo ""
    
    # Run lintian to check the package
    echo "🔍 Running package quality checks with lintian..."
    echo ""
    
    DEB_FILE=$(ls -t ../*.deb 2>/dev/null | head -n1)
    if [ -n "$DEB_FILE" ]; then
        lintian "$DEB_FILE" || true
        echo ""
        echo "📋 Package contents:"
        dpkg -c "$DEB_FILE" | head -n 20
        if [ $(dpkg -c "$DEB_FILE" | wc -l) -gt 20 ]; then
            echo "  ... (more files)"
        fi
        echo ""
        echo "ℹ️  To install the package locally:"
        echo "   sudo dpkg -i $DEB_FILE"
        echo "   sudo apt-get install -f  # Fix any dependency issues"
        echo ""
    fi
    
    echo "✅ Build complete! Package is ready for distribution."
    echo ""
    echo "📖 Next steps:"
    echo "   1. Test the package locally (see command above)"
    echo "   2. Sign the package for PPA upload (see PPA_SETUP.md)"
    echo "   3. Upload to Launchpad PPA (see PPA_SETUP.md)"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Build failed! Check the output above for errors.${NC}"
    echo ""
    exit 1
fi
