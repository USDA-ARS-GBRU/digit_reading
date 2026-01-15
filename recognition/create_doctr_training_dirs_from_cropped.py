'''create_doctr_training_dirs_from_cropped.py 
'''
import os
import shutil
import json
import random
import re

# Define paths
source_dir = 'cropped_images2_inverted'
train_path = 'train_path'
val_path = 'val_path'
val_size = 1000

def setup_directories(path):
    """Creates the images subdirectory within the given path."""
    img_dir = os.path.join(path, 'images')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    return img_dir

def extract_label(filename):
    """Extracts the 4 digits following 'digits' in the filename."""
    match = re.search(r'digits(\d{4})', filename)
    return match.group(1) if match else None

def process_dataset():
    # 1. Get and shuffle all jpg files
    all_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg')]
    random.shuffle(all_files)

    # 2. Split into validation and training sets
    val_files = all_files[:val_size]
    train_files = all_files[val_size:]

    # 3. Setup directory structures
    train_img_dir = setup_directories(train_path)
    val_img_dir = setup_directories(val_path)

    # 4. Move files and build label dictionaries
    datasets = [
        (train_files, train_img_dir, train_path),
        (val_files, val_img_dir, val_path)
    ]

    for files, img_dest, root_dest in datasets:
        labels_dict = {}
        
        print(f"Processing {len(files)} files for {root_dest}...")
        
        for filename in files:
            label = extract_label(filename)
            if label:
                # Move the file
                shutil.copy(os.path.join(source_dir, filename), os.path.join(img_dest, filename))
                # Add to label dictionary
                labels_dict[filename] = label
            else:
                print(f"Warning: Could not parse label for {filename}")

        # Save labels.json in the respective root directory
        with open(os.path.join(root_dest, 'labels.json'), 'w') as f:
            json.dump(labels_dict, f, indent=4)

    print("Task completed successfully.")

if __name__ == "__main__":
    process_dataset()