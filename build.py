# build.py
import os
import sys
import subprocess

def build_executable():
    """Build standalone executable using PyInstaller"""
    print("Building Sorting Algorithm Simulator executable...")
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=SortingAlgorithmSimulator',
        '--windowed',  # No console window
        '--onefile',   # Single executable file
        '--add-data=gui;gui',           # Include gui folder
        '--add-data=sorting;sorting',   # Include sorting folder  
        '--add-data=utils;utils',       # Include utils folder
        '--icon=icon.ico',              # Optional: add your own icon
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        print(f"Executable location: {os.path.abspath('dist/SortingAlgorithmSimulator.exe')}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install it with: pip install pyinstaller")

if __name__ == "__main__":
    build_executable()