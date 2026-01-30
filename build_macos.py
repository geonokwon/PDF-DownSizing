"""
Build script for macOS executable
"""
import os
import sys
import subprocess
import shutil


def build_macos_executable():
    """Build macOS executable using PyInstaller"""
    
    print("Building macOS executable...")
                                                                                                                                                  
    # PyInstaller command for macOS (using onedir for .app bundle)
    cmd = [
        "pyinstaller",
        "--onedir",
        "--windowed",
        "--name=PDF-DownSizing-Tool",
        "--icon=icon.icns" if os.path.exists("icon.icns") else "",
        "--add-data=README.md:.",
        "--clean",
        "main.py"
    ]
    
    # Remove empty icon parameter if icon doesn't exist
    cmd = [arg for arg in cmd if arg]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created in: dist/PDF-DownSizing-Tool")
        
        # Create distribution folder
        if not os.path.exists("dist"):
            os.makedirs("dist")
        
        # Copy additional files to dist folder
        if os.path.exists("README.md"):
            shutil.copy2("README.md", "dist/")
        
        # Make executable
        executable_path = "dist/PDF-DownSizing-Tool"
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
        
        print("\nFiles in distribution:")
        for file in os.listdir("dist"):
            print(f"  - {file}")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Please install it first:")
        print("pip install pyinstaller")
        return False
    
    return True


def create_dmg():
    """Create DMG file for macOS distribution (optional)"""
    try:
        import dmgbuild
        print("Creating DMG file...")
        
        settings = {
            'files': ['dist/PDF-DownSizing-Tool'],
            'symlinks': {'Applications': '/Applications'},
            'icon_locations': {
                'PDF-DownSizing-Tool': (200, 200)
            },
            'background': 'builtin-arrow',
            'window_rect': ((100, 100), (800, 400)),
            'default_view': 'icon-view',
            'show_status_bar': False,
            'show_tab_view': False,
            'show_toolbar': False,
            'show_pathbar': False,
            'show_sidebar': False,
            'sidebar_width': 180,
        }
        
        dmgbuild.build_dmg(
            "dist/PDF-DownSizing-Tool.dmg",
            "PDF DownSizing Tool",
            settings
        )
        print("DMG created successfully!")
        
    except ImportError:
        print("dmgbuild not installed. Skipping DMG creation.")
        print("To create DMG files, install: pip install dmgbuild")


def clean_build_files():
    """Clean up build files"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")
    
    import glob
    for pattern in files_to_clean:
        for file in glob.glob(pattern):
            os.remove(file)
            print(f"Cleaned {file}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        clean_build_files()
    elif len(sys.argv) > 1 and sys.argv[1] == "--dmg":
        success = build_macos_executable()
        if success:
            create_dmg()
    else:
        success = build_macos_executable()
        if success:
            print("\n✅ macOS build completed successfully!")
            print("You can find the executable in the 'dist' folder.")
            print("To create a DMG file, run: python build_macos.py --dmg")
        else:
            print("\n❌ Build failed!")
            sys.exit(1)
