import os

# Define the paths to the two folders
folder1 = "runs/detect/predict2/crops/skua"  # Folder containing the .jpg files
folder2 = "runs/detect/predict2/labels"  # Folder containing the .txt files

# List all .jpg files in folder1 (use base names without extensions)
jpg_files = {os.path.splitext(f)[0] for f in os.listdir(folder1) if f.endswith(".jpg")}

# List all .txt files in folder2 (use base names without extensions)
txt_files = [f for f in os.listdir(folder2) if f.endswith(".txt")]

# Iterate over the .txt files and delete those without a corresponding .jpg file
for txt_file in txt_files:
    base_name = os.path.splitext(txt_file)[0]  # Get the base name without extension
    
    if base_name not in jpg_files:
        # If no corresponding .jpg file, delete the .txt file
        txt_file_path = os.path.join(folder2, txt_file)
        try:
            os.remove(txt_file_path)
            print(f"Deleted: {txt_file_path}")
        except Exception as e:
            print(f"Failed to delete {txt_file_path}: {e}")

print("Operation completed.")
