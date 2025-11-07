#!/bin/bash
# Use your photo as the app icon
# Place your photo in this directory and run this script

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🎨 Convert Your Photo to App Icon 🎨            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Look for photo files (excluding generated icons)
PHOTO_FILES=($(ls *.jpg *.jpeg *.png 2>/dev/null | grep -v "fuckooredoo-" | head -1))

if [ ${#PHOTO_FILES[@]} -eq 0 ]; then
    echo "❌ No photo found in current directory!"
    echo ""
    echo "📋 Instructions:"
    echo "   1. Save your photo to this directory as: my_photo.jpg"
    echo "   2. Run this script again: ./use_my_photo_as_icon.sh"
    echo ""
    echo "Or specify the photo path:"
    echo "   ./convert_photo_to_icon.sh /path/to/your/photo.jpg"
    exit 1
fi

PHOTO="${PHOTO_FILES[0]}"
echo "📷 Found photo: $PHOTO"
echo ""

# Ask for confirmation
read -p "Use this photo as the app icon? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "🎨 Converting photo to icon..."
./convert_photo_to_icon.sh "$PHOTO"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              ✅ Icon Created Successfully! ✅             ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Your photo is now the application icon!"
    echo ""
    echo "📦 Next steps:"
    echo "   1. Rebuild the package: ./build_deb.sh"
    echo "   2. Install and see your icon: sudo dpkg -i ../*.deb"
    echo ""
    echo "🚀 Or upload to PPA: ./upload_to_ppa.sh"
    echo ""
else
    echo "❌ Icon conversion failed!"
    exit 1
fi
