from ultralytics import YOLO
import os
import time
import random
from io import BytesIO
from PIL import Image
from botocore.client import Config
from botocore import UNSIGNED
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

# Initialize your YOLO model
model = YOLO("runs/detect/train12/weights/best.pt")

# S3 Setup
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
bucket_name = 'deju-penguinscience'
prefix = 'UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'

# Fetch object keys from S3
def get_random_sample_from_s3(bucket, prefix, sample_size=20000):
    all_objects = []
    continuation_token = None

    print("Fetching object list from S3...")
    while True:
        if continuation_token:
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

        if 'Contents' in response:
            all_objects.extend([obj['Key'] for obj in response['Contents']])
            print(f"Fetched {len(response['Contents'])} objects (total: {len(all_objects)})")

        if response.get('IsTruncated'):
            continuation_token = response['NextContinuationToken']
        else:
            break

    print(f"Total objects retrieved: {len(all_objects)}")
    
    if len(all_objects) < sample_size:
        raise ValueError(f"Sample size {sample_size} exceeds the number of available objects ({len(all_objects)}).")
    
    # Randomly sample keys
    sampled_keys = random.sample(all_objects, sample_size)
    print(f"Randomly sampled {sample_size} keys from S3.")
    return sampled_keys

# Function to download image from S3
def load_image_from_s3(s3_client, bucket, key):
    try:
        img_data = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
        img = Image.open(BytesIO(img_data))
        return img, key  # Return the image and its original key
    except Exception as e:
        print(f"Error loading image {key}: {e}")
        return None, key

# Load images concurrently
def load_images_concurrently(keys, bucket, s3_client, max_workers=10):
    images = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_key = {executor.submit(load_image_from_s3, s3_client, bucket, key): key for key in keys}
        for i, future in enumerate(as_completed(future_to_key), 1):
            key = future_to_key[future]
            try:
                img, original_key = future.result()
                if img is not None:
                    images.append((img, original_key))  # Append the image and its key
            except Exception as e:
                print(f"Error loading image {key}: {e}")
            
            # Print progress
            if i % 100 == 0 or i == len(keys):
                print(f"Loaded {i}/{len(keys)} images.")

    return images

# Randomly sample 5,000 keys
sampled_keys = get_random_sample_from_s3(bucket_name, prefix, sample_size=5000)

# Load sampled images with progress updates
print("Loading sampled images...")
image_data = load_images_concurrently(sampled_keys, bucket_name, s3, max_workers=20)

print(f"Total images loaded: {len(image_data)}")

# Process images in batches
def process_images_in_batches(image_data, batch_size=100):
    results = []
    for i in range(0, len(image_data), batch_size):
        batch = image_data[i:i + batch_size]
        batch_images, batch_keys = zip(*batch)  # Separate images and their keys
        print(f"Processing batch {i // batch_size + 1} of {len(image_data) // batch_size + 1}")

        # Predict on the batch
        batch_results = model.predict(source=batch_images, save=False, save_txt=True, save_conf=False, iou=0.5, conf=0.6,save_crop=True)

        # Directory where YOLO saves predictions and labels
        default_save_dir = "runs/detect/predict"

        for result, original_key in zip(batch_results, batch_keys):
            # Use the original S3 file name to rename saved outputs
            original_filename = os.path.basename(original_key)

            # Rename saved image
            saved_image_path = os.path.join(default_save_dir, os.path.basename(result.path))
            new_image_path = os.path.join(default_save_dir, original_filename)
            if os.path.exists(saved_image_path):
                os.rename(saved_image_path, new_image_path)
                print(f"Saved processed image: {new_image_path}")
            else:
                print(f"Image file not found: {saved_image_path}")

            # Ensure .txt file has the correct name
            saved_txt_path = os.path.splitext(saved_image_path)[0] + '.txt'
            new_txt_path = os.path.splitext(new_image_path)[0] + '.txt'
            if os.path.exists(saved_txt_path):
                os.rename(saved_txt_path, new_txt_path)
                print(f"Saved label file: {new_txt_path}")
            else:
                print(f"Label file not found: {saved_txt_path}")

        results.extend(batch_results)
        time.sleep(1)  # Optional delay to manage system load

    return results

# Process the images in batches
print("Processing images in batches...")
results = process_images_in_batches(image_data, batch_size=200)

print("Predictions completed!")
