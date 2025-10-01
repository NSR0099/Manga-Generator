import subprocess
from pathlib import Path
import sys
import os
import shutil

def merge_subfolders(main_folder):
    # Walk through directory tree from bottom to top (deepest subfolders first)
    for root, dirs, files in os.walk(main_folder, topdown=False):
        if root == main_folder:
            # Skip main folder itself
            continue
        
        for filename in files:
            file_path = os.path.join(root, filename)
            # Create a relative path for the file from main folder
            relative_path = os.path.relpath(file_path, main_folder)
            # Replace folder separators with underscores to avoid collisions
            safe_filename = relative_path.replace(os.sep, '_')
            new_file_path = os.path.join(main_folder, safe_filename)
            
            # Move and rename the file
            shutil.move(file_path, new_file_path)
        
        # Remove the empty folder after files are moved
        try:
            os.rmdir(root)
        except OSError as e:
            print(f"Warning: Could not remove directory {root}: {e}")

    print("All subfolders merged. Only files remain in the main folder.")

def add_to_calibre(file_path: Path, calibre_library_path: Path = None):
    """Add file to Calibre library using calibredb."""
    command = ["calibredb", "add", str(file_path)]
    if calibre_library_path:
        command.extend(["--with-library", str(calibre_library_path)])
    
    try:
        print("\n📚 Adding file to Calibre library:")
        print("   ", " ".join(command))
        subprocess.run(command, check=True)
        print("✅ Added to Calibre library successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to add to Calibre library: {e}")

def convert_manga_with_kcc(
    images_folder,
    output_dir,
    title="Manga Title",
    author="Unknown",
    profile="KPW",
    calibre_library_path=None
):
    images_folder = Path(images_folder).resolve()
    output_dir = Path(output_dir).resolve()
    kcc_script = Path(r"C:\Users\Nain Singh Rathore\Downloads\KCC_c2e_9.0.0.exe")  


    if not images_folder.exists():
        print(f"❌ Input folder not found: {images_folder}")
        return
    if not kcc_script.exists():
        print(f"❌ kcc-c2e.py not found at: {kcc_script}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
    str(kcc_script),
    "-p", profile,
    "-m",
    "--cropping", "0",
    "--preservemargin", "0",
    "-f", "EPUB",
    "-t", title,
    "-a", author,
    "-o", str(output_dir),
    str(images_folder)
]

    try:
        print("\n🚀 Running Kindle Comic Converter:")
        print("   ", " ".join(command))
        subprocess.run(command, check=True)
        print(f"\n✅ Conversion complete! Checking for output...")

        output_files = list(output_dir.glob("*.epub"))
        if output_files:
            output_file = output_files[0]
            print(f"📄 Found output file: {output_file.name}")
            add_to_calibre(output_file, calibre_library_path)
        else:
            print("❌ No output EPUB file found in output directory.")

    except subprocess.CalledProcessError as e:
        print(f"❌ KCC failed: {e}")
        sys.exit(1)

if __name__ == "__main__":

    merge_subfolders(r'C:\Users\Nain Singh Rathore\Documents\manga')
    convert_manga_with_kcc(
        images_folder=r"C:\Users\Nain Singh Rathore\Documents\manga",
        output_dir=r"C:\Users\Nain Singh Rathore\Documents\MangaPirate",
        title=input("Enter Title: "),
        author=input("Enter Author: "),
        profile="KPW",
        calibre_library_path=None
    )
