import os
import glob

# Set the base directory
base_dir = 'Labelled Images'
images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')

# Get list of all images and labels
image_files = set(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(images_dir, '*.*')))
label_files = set(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(labels_dir, '*.txt')))
# image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]
# label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
print(len(image_files))
print(len(label_files))
# Find mismatches
images_without_labels = image_files - label_files
labels_without_images = label_files - image_files

# Remove images without labels
for img in images_without_labels:
    img_path = glob.glob(os.path.join(images_dir, f'{img}.*'))[0]
    os.remove(img_path)
    print(f"Removed image without label: {img_path}")

# Remove labels without images
for lbl in labels_without_images:
    lbl_path = os.path.join(labels_dir, f'{lbl}.txt')
    os.remove(lbl_path)
    print(f"Removed label without image: {lbl_path}")

# Final check
image_files = set(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(images_dir, '*.*')))
label_files = set(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(labels_dir, '*.txt')))

print(f"\nFinal count: {len(image_files)} images and {len(label_files)} labels")
if image_files == label_files:
    print("All images and labels are now matched!")
else:
    print("There are still mismatches. Please check manually.")
