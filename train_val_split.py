import os
import shutil

# Define the base directory for your labeled images.
base_dir = 'Labelled Images'

# Define paths for the current structure.
current_train_images_dir = os.path.join(base_dir, 'images', 'train')
current_val_images_dir = os.path.join(base_dir, 'images', 'val')
current_train_labels_dir = os.path.join(base_dir, 'labels', 'train')
current_val_labels_dir = os.path.join(base_dir, 'labels', 'val')

# Define new directories for the desired structure.
new_train_images_dir = os.path.join(base_dir, 'train', 'images')
new_train_labels_dir = os.path.join(base_dir, 'train', 'labels')
new_val_images_dir = os.path.join(base_dir, 'val', 'images')
new_val_labels_dir = os.path.join(base_dir, 'val', 'labels')

# Create new directories if they don't exist.
os.makedirs(new_train_images_dir, exist_ok=True)
os.makedirs(new_train_labels_dir, exist_ok=True)
os.makedirs(new_val_images_dir, exist_ok=True)
os.makedirs(new_val_labels_dir, exist_ok=True)

# Function to move files from old structure to new structure.
def move_files(old_images_path, new_images_path):
    if os.path.exists(old_images_path):
        for img_file in os.listdir(old_images_path):
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                shutil.move(os.path.join(old_images_path, img_file), new_images_path)
                print(f"Moved {img_file} to {new_images_path}")
    else:
        print(f"Directory does not exist: {old_images_path}")

def move_labels(old_labels_path, new_labels_path):
    if os.path.exists(old_labels_path):
        for lbl_file in os.listdir(old_labels_path):
            if lbl_file.lower().endswith('.txt'):
                shutil.move(os.path.join(old_labels_path, lbl_file), new_labels_path)
                print(f"Moved {lbl_file} to {new_labels_path}")
    else:
        print(f"Directory does not exist: {old_labels_path}")

# Move training files and labels.
move_files(current_train_images_dir, new_train_images_dir)
move_labels(current_train_labels_dir, new_train_labels_dir)

# Move validation files and labels.
move_files(current_val_images_dir, new_val_images_dir)
move_labels(current_val_labels_dir, new_val_labels_dir)

print("Restructuring complete.")
