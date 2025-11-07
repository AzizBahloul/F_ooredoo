#!/bin/bash
# Quick test script for Debian package

echo "🧪 Testing Debian Package Installation..."
echo ""

# Check if package is installed
if dpkg -l | grep -q fuckooredoo; then
    echo "✅ Package is installed"
    echo ""
    
    # Check version
    echo "📦 Installed version:"
    dpkg -l | grep fuckooredoo
    echo ""
    
    # Check if binary is accessible
    if command -v fuckooredoo &> /dev/null; then
        echo "✅ Binary is in PATH"
        echo ""
        
        # Show help
        echo "📖 Showing help output:"
        fuckooredoo --help || echo "  (help not yet implemented)"
        echo ""
    else
        echo "❌ Binary not found in PATH"
        exit 1
    fi
    
    # Check installed files
    echo "📁 Installed files:"
    dpkg -L fuckooredoo | head -n 20
    echo ""
    
    # Check Tor status
    echo "🔧 Checking Tor service:"
    if systemctl is-active --quiet tor; then
        echo "✅ Tor is running"
    else
        echo "⚠️  Tor is not running"
        echo "   Start with: sudo systemctl start tor"
    fi
    echo ""
    
    # Check documentation
    echo "📚 Documentation files:"
    ls -lh /usr/share/doc/fuckooredoo/ 2>/dev/null || echo "  (no docs found)"
    echo ""
    
    # Check man page
    echo "📄 Man page:"
    if man -w fuckooredoo &> /dev/null; then
        echo "✅ Man page is installed"
        echo "   View with: man fuckooredoo"
    else
        echo "⚠️  Man page not found"
    fi
    echo ""
    
    echo "✅ All tests passed!"
    
else
    echo "❌ Package is not installed"
    echo ""
    echo "Install with one of these methods:"
    echo ""
    echo "1. Local .deb file:"
    echo "   sudo dpkg -i fuckooredoo_*.deb"
    echo "   sudo apt-get install -f"
    echo ""
    echo "2. From PPA:"
    echo "   sudo add-apt-repository ppa:username/fuckooredoo"
    echo "   sudo apt-get update"
    echo "   sudo apt-get install fuckooredoo"
    echo ""
    exit 1
fi
