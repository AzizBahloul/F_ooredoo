#check_package.py
"""
Quick test script to verify package structure before building
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if Path(filepath).exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} MISSING: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status"""
    if Path(dirpath).is_dir():
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description} MISSING: {dirpath}")
        return False

def main():
    print("=" * 70)
    print("F_ooredoo Package Structure Verification")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # Check root files
    print("📄 Checking root files...")
    all_ok &= check_file_exists("setup.py", "Setup script")
    all_ok &= check_file_exists("pyproject.toml", "Project config")
    all_ok &= check_file_exists("README.md", "README")
    all_ok &= check_file_exists("LICENSE", "License")
    all_ok &= check_file_exists("requirements.txt", "Requirements")
    all_ok &= check_file_exists("MANIFEST.in", "Manifest")
    print()
    
    # Check package directory
    print("📦 Checking package directory...")
    all_ok &= check_directory_exists("fuckooredoo", "Package directory")
    all_ok &= check_file_exists("fuckooredoo/__init__.py", "Package init")
    all_ok &= check_file_exists("fuckooredoo/__main__.py", "CLI entry point")
    all_ok &= check_file_exists("fuckooredoo/torrent_client.py", "Torrent client")
    all_ok &= check_file_exists("fuckooredoo/gui.py", "GUI module")
    all_ok &= check_file_exists("fuckooredoo/main.py", "Main module")
    print()
    
    # Check version consistency
    print("🔢 Checking version consistency...")
    try:
        # Read version from __init__.py
        with open("fuckooredoo/__init__.py", "r") as f:
            init_content = f.read()
            if '__version__ = "1.0.0"' in init_content:
                print("✓ Version in __init__.py: 1.0.0")
            else:
                print("✗ Version mismatch in __init__.py")
                all_ok = False
        
        # Read version from setup.py
        with open("setup.py", "r") as f:
            setup_content = f.read()
            if 'version="1.0.0"' in setup_content:
                print("✓ Version in setup.py: 1.0.0")
            else:
                print("✗ Version mismatch in setup.py")
                all_ok = False
        
        # Read version from pyproject.toml
        with open("pyproject.toml", "r") as f:
            toml_content = f.read()
            if 'version = "1.0.0"' in toml_content:
                print("✓ Version in pyproject.toml: 1.0.0")
            else:
                print("✗ Version mismatch in pyproject.toml")
                all_ok = False
    except Exception as e:
        print(f"✗ Error checking versions: {e}")
        all_ok = False
    print()
    
    # Check imports
    print("🔍 Checking package imports...")
    try:
        with open("fuckooredoo/gui.py", "r") as f:
            gui_content = f.read()
            if "from .torrent_client import" in gui_content:
                print("✓ Relative imports in gui.py")
            else:
                print("⚠ Warning: gui.py might not use relative imports")
        
        with open("fuckooredoo/main.py", "r") as f:
            main_content = f.read()
            if "from .torrent_client import" in main_content and "from .gui import" in main_content:
                print("✓ Relative imports in main.py")
            else:
                print("⚠ Warning: main.py might not use relative imports")
    except Exception as e:
        print(f"✗ Error checking imports: {e}")
        all_ok = False
    print()
    
    # Final result
    print("=" * 70)
    if all_ok:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Ready to build! Run:")
        print("  ./build.sh")
        print()
        print("Or manually:")
        print("  python -m build")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print()
        print("Please fix the issues above before building.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
