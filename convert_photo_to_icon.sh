#!/bin/bash
# Convert your photo to application icon

set -e

echo "🎨 Converting your photo to application icon..."

# The photo should be provided as first argument
PHOTO="$1"

if [ -z "$PHOTO" ]; then
    echo "Usage: $0 <photo_file>"
    echo "Example: $0 my_photo.jpg"
    exit 1
fi

if [ ! -f "$PHOTO" ]; then
    echo "Error: Photo file '$PHOTO' not found!"
    exit 1
fi

echo "📷 Source photo: $PHOTO"
echo ""

# Generate circular/rounded icon with border
echo "Generating icon variants..."

# Create SVG icon with your photo
cat > fuckooredoo.svg << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="128" height="128" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="circleClip">
      <circle cx="64" cy="64" r="58"/>
    </clipPath>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b0000;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#ff4444;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8b0000;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Outer border ring -->
  <circle cx="64" cy="64" r="62" fill="url(#borderGrad)"/>
  
  <!-- Profile photo (will be replaced with actual photo) -->
  <image href="PHOTO_PLACEHOLDER" x="6" y="6" width="116" height="116" clip-path="url(#circleClip)" preserveAspectRatio="xMidYMid slice"/>
  
  <!-- Inner border -->
  <circle cx="64" cy="64" r="58" fill="none" stroke="#000000" stroke-width="1" opacity="0.3"/>
  
  <!-- Small badge indicator (Tor/secure) -->
  <g transform="translate(100, 100)">
    <circle cx="0" cy="0" r="16" fill="#8b0000" stroke="white" stroke-width="2"/>
    <text x="0" y="6" font-family="Arial" font-size="20" font-weight="bold" fill="white" text-anchor="middle">🖕</text>
  </g>
</svg>
EOF

# Convert photo to base64 and embed in SVG
if command -v base64 >/dev/null 2>&1; then
    echo "Embedding photo in SVG..."
    PHOTO_BASE64=$(base64 -w 0 "$PHOTO")
    PHOTO_TYPE=$(file -b --mime-type "$PHOTO")
    PHOTO_DATA="data:${PHOTO_TYPE};base64,${PHOTO_BASE64}"
    sed -i "s|PHOTO_PLACEHOLDER|${PHOTO_DATA}|g" fuckooredoo.svg
    echo "✓ SVG icon created"
fi

# Generate PNG versions in multiple sizes
SIZES=(16 22 24 32 48 64 128 256)

echo "Generating PNG icons..."
for size in "${SIZES[@]}"; do
    if command -v convert >/dev/null 2>&1; then
        # Create rounded icon with border
        convert "$PHOTO" \
            -resize ${size}x${size}^ \
            -gravity center \
            -extent ${size}x${size} \
            \( +clone -threshold -1 -negate -fill white -draw "circle $((size/2)),$((size/2)) $((size/2)),2" \) \
            -alpha off -compose copy_opacity -composite \
            -bordercolor '#8b0000' -border 2 \
            "fuckooredoo-${size}.png"
        echo "  ✓ Created ${size}x${size} icon"
    fi
done

echo ""
echo "✅ Icon conversion complete!"
echo ""
echo "Generated files:"
ls -lh fuckooredoo.svg fuckooredoo-*.png 2>/dev/null

echo ""
echo "🎯 Your photo is now the application icon!"
