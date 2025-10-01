import os

def rename_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    for item_name in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item_name)

        # Skip items that already start with "Chapter"
        if item_name.startswith("Chapter"):
            print(f"Skipping: {item_name}")
            continue

        # Ensure the name is long enough to remove 3 characters
        if len(item_name) > 3:
            new_name = item_name[3:]
        else:
            print(f"Skipping (name too short to trim 3 chars): {item_name}")
            continue

        new_path = os.path.join(folder_path, new_name)

        # Rename file or folder
        try:
            os.rename(item_path, new_path)
            print(f"Renamed: {item_name} ➜ {new_name}")
        except Exception as e:
            print(f"Error renaming {item_name}: {e}")

# Example usage:
folder = input("Enter the path to the folder: ").strip()
rename_files_in_folder(folder)
