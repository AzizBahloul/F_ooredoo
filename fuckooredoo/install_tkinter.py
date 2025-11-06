#fuckooredoo/install_tkinter.py
"""
Post-installation helper to attempt automatic tkinter installation
This runs after pip install to help users get tkinter automatically
"""

import sys
import subprocess
import platform
import os


def install_tkinter():
    """Attempt to install tkinter automatically based on OS"""
    
    # Check if tkinter is already available
    try:
        import tkinter
        print("✅ tkinter is already installed!")
        return True
    except ImportError:
        pass
    
    print("\n⚠️  tkinter not found. Attempting automatic installation...")
    
    system = platform.system().lower()
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    # Determine the right package and command based on OS
    if system == "linux":
        # Try to detect package manager and distribution
        cmd = None
        package = None
        distro_name = "Linux"
        
        try:
            # Read OS release info
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
            
            # Detect distribution family
            if 'debian' in os_info or 'ubuntu' in os_info or 'mint' in os_info or 'pop' in os_info or 'zorin' in os_info:
                distro_name = "Debian/Ubuntu"
                package = f"python{python_version}-tk"
                # Check if apt is available
                if subprocess.run(["which", "apt"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "apt", "install", "-y", package]
                elif subprocess.run(["which", "apt-get"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "apt-get", "install", "-y", package]
                
            elif 'fedora' in os_info or 'rhel' in os_info or 'centos' in os_info or 'rocky' in os_info or 'alma' in os_info:
                distro_name = "Fedora/RHEL"
                package = f"python{python_version}-tkinter"
                # Check if dnf or yum is available
                if subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "dnf", "install", "-y", package]
                elif subprocess.run(["which", "yum"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "yum", "install", "-y", package]
                
            elif 'arch' in os_info or 'manjaro' in os_info or 'endeavour' in os_info:
                distro_name = "Arch Linux"
                package = "tk"
                if subprocess.run(["which", "pacman"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "pacman", "-S", "--noconfirm", package]
                
            elif 'opensuse' in os_info or 'suse' in os_info or 'sles' in os_info:
                distro_name = "openSUSE"
                package = f"python{python_version.replace('.', '')}-tk"
                if subprocess.run(["which", "zypper"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "zypper", "install", "-y", package]
                
            elif 'gentoo' in os_info:
                distro_name = "Gentoo"
                package = f"dev-lang/python:{python_version}[tk]"
                if subprocess.run(["which", "emerge"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "emerge", "--ask=n", "dev-lang/python"]
                    print(f"\n⚠️  Note: On Gentoo, you need to enable the 'tk' USE flag for Python.")
                
            elif 'alpine' in os_info:
                distro_name = "Alpine Linux"
                package = f"python{python_version.replace('.', '')}-tkinter"
                if subprocess.run(["which", "apk"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "apk", "add", package]
                    
            elif 'void' in os_info:
                distro_name = "Void Linux"
                package = f"python{python_version}-tkinter"
                if subprocess.run(["which", "xbps-install"], capture_output=True).returncode == 0:
                    cmd = ["sudo", "xbps-install", "-y", package]
            
            # If no specific distro detected, try to detect package manager directly
            if cmd is None:
                if subprocess.run(["which", "apt"], capture_output=True).returncode == 0:
                    distro_name = "APT-based"
                    package = f"python{python_version}-tk"
                    cmd = ["sudo", "apt", "install", "-y", package]
                elif subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
                    distro_name = "DNF-based"
                    package = f"python{python_version}-tkinter"
                    cmd = ["sudo", "dnf", "install", "-y", package]
                elif subprocess.run(["which", "yum"], capture_output=True).returncode == 0:
                    distro_name = "YUM-based"
                    package = f"python{python_version}-tkinter"
                    cmd = ["sudo", "yum", "install", "-y", package]
                elif subprocess.run(["which", "pacman"], capture_output=True).returncode == 0:
                    distro_name = "Pacman-based"
                    package = "tk"
                    cmd = ["sudo", "pacman", "-S", "--noconfirm", package]
                elif subprocess.run(["which", "zypper"], capture_output=True).returncode == 0:
                    distro_name = "Zypper-based"
                    package = f"python{python_version.replace('.', '')}-tk"
                    cmd = ["sudo", "zypper", "install", "-y", package]
            
            if cmd is None:
                print(f"\n❌ Could not detect package manager on this {distro_name} system.")
                print("\nPlease install tkinter manually:")
                print(f"   Debian/Ubuntu/Mint:  sudo apt install python{python_version}-tk")
                print(f"   Fedora/RHEL/CentOS:  sudo dnf install python{python_version}-tkinter")
                print(f"   Arch/Manjaro:        sudo pacman -S tk")
                print(f"   openSUSE:            sudo zypper install python{python_version.replace('.', '')}-tk")
                print(f"   Alpine:              sudo apk add python{python_version.replace('.', '')}-tkinter")
                print(f"   Void:                sudo xbps-install python{python_version}-tkinter")
                return False
            
            print(f"\n🔧 Detected {distro_name}. Installing {package}...")
            print(f"Running: {' '.join(cmd)}")
            print("\n⚠️  You may need to enter your password:\n")
            
            # Try to run the installation
            try:
                result = subprocess.run(cmd, check=False)
                if result.returncode == 0:
                    print("\n✅ tkinter installation completed!")
                    # Verify
                    try:
                        import tkinter
                        print("✅ tkinter verified and working!")
                        return True
                    except ImportError:
                        print("⚠️  Installation succeeded but tkinter still not found.")
                        print("   You may need to restart your terminal or Python.")
                        return False
                else:
                    print(f"\n❌ Installation failed with exit code {result.returncode}")
                    return False
            except Exception as e:
                print(f"\n❌ Could not run installation: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error detecting Linux distribution: {e}")
            return False
    
    elif system == "darwin":
        print("\n🍎 macOS detected.")
        print("Please install tkinter using Homebrew:")
        print("   brew install python-tk")
        print("\nOr ensure your Python was installed with Tcl/Tk support:")
        print("   brew reinstall python@3.11 --with-tcl-tk")
        return False
    
    elif system == "windows":
        print("\n🪟 Windows detected.")
        print("Please reinstall Python from python.org and ensure")
        print("'tcl/tk and IDLE' option is selected in the installer.")
        return False
    
    else:
        print(f"\n❌ Unknown operating system: {system}")
        return False


if __name__ == "__main__":
    install_tkinter()
