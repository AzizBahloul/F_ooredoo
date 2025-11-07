#!/usr/bin/env python3
"""
Simple icon generator for F**k Ooredoo
Creates a basic SVG icon if no custom icon is provided
"""

import os
import sys

def create_default_icon(output_path):
    """Create a default SVG icon"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="128" height="128" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b0000;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ff4444;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#333333;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background circle -->
  <circle cx="64" cy="64" r="60" fill="url(#grad1)" stroke="#660000" stroke-width="3"/>
  
  <!-- Tor onion symbol -->
  <circle cx="64" cy="64" r="35" fill="none" stroke="white" stroke-width="3" opacity="0.8"/>
  <circle cx="64" cy="64" r="25" fill="none" stroke="white" stroke-width="2.5" opacity="0.6"/>
  <circle cx="64" cy="64" r="15" fill="none" stroke="white" stroke-width="2" opacity="0.4"/>
  
  <!-- Download arrow -->
  <g transform="translate(64, 64)">
    <path d="M -8,0 L -8,-20 L 8,-20 L 8,0 L 18,-10 L 0,8 L -18,-10 Z" 
          fill="white" stroke="#660000" stroke-width="1.5"/>
  </g>
  
  <!-- Prohibition slash (anti-throttling) -->
  <line x1="25" y1="25" x2="103" y2="103" 
        stroke="#ffcc00" stroke-width="6" opacity="0.9"
        stroke-linecap="round"/>
</svg>'''
    
    with open(output_path, 'w') as f:
        f.write(svg_content)
    print(f"Created icon at: {output_path}")

if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else 'fuckooredoo.svg'
    create_default_icon(output)
