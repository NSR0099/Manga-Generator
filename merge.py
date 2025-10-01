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

# Example usage - change this path to your folder:
merge_subfolders(r'C:\Users\Nain Singh Rathore\Documents\manga')
