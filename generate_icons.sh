#!/bin/bash
# Generate PNG icons in multiple sizes from SVG

set -e

SVG_FILE="fuckooredoo.svg"

if [ ! -f "$SVG_FILE" ]; then
    echo "Error: $SVG_FILE not found!"
    exit 1
fi

echo "Generating PNG icons from SVG..."

# Check for required tools
if command -v rsvg-convert >/dev/null 2>&1; then
    CONVERTER="rsvg-convert"
    echo "Using rsvg-convert..."
elif command -v convert >/dev/null 2>&1; then
    CONVERTER="imagemagick"
    echo "Using ImageMagick convert..."
else
    echo "Warning: Neither rsvg-convert nor ImageMagick found."
    echo "SVG icon will be used directly (works on most modern systems)"
    exit 0
fi

# Create PNG icons in standard sizes
SIZES=(16 22 24 32 48 64 128 256)

for size in "${SIZES[@]}"; do
    output="fuckooredoo-${size}.png"
    
    if [ "$CONVERTER" = "rsvg-convert" ]; then
        rsvg-convert -w $size -h $size "$SVG_FILE" -o "$output"
    else
        convert -background none -resize ${size}x${size} "$SVG_FILE" "$output"
    fi
    
    echo "  Created: $output (${size}x${size})"
done

echo ""
echo "✅ Icon generation complete!"
echo ""
echo "Generated files:"
ls -lh fuckooredoo*.png 2>/dev/null || echo "  (SVG only - no PNG files)"
