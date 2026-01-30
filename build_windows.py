"""
Build script for Windows executable
"""
import os
import sys
import subprocess
import shutil


def build_windows_executable():
    """Build Windows executable using PyInstaller"""
    
    print("Building Windows executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=PDF-DownSizing-Tool",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        "--add-data=README.md:." if os.path.exists("README.md") else "",
        "--hidden-import=tkinter",
        "--hidden-import=PyPDF2",
        "--hidden-import=PIL",
        "main.py"
    ]
    
    # Remove empty icon parameter if icon doesn't exist
    cmd = [arg for arg in cmd if arg]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created in: dist/PDF-DownSizing-Tool.exe")
        
        # Create distribution folder
        if not os.path.exists("dist"):
            os.makedirs("dist")
        
        # Copy additional files to dist folder
        if os.path.exists("README.md"):
            shutil.copy2("README.md", "dist/")
        
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
    else:
        success = build_windows_executable()
        if success:
            print("\n✅ Windows build completed successfully!")
            print("You can find the executable in the 'dist' folder.")
        else:
            print("\n❌ Build failed!")
            sys.exit(1)
