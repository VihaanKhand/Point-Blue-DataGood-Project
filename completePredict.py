import boto3
import os
import time
import random
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
from botocore.client import Config
from botocore import UNSIGNED
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        return img
    except Exception as e:
        print(f"Error loading image {key}: {e}")
        return None

# Load images concurrently
def load_images_concurrently(keys, bucket, s3_client, max_workers=10):
    images = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_key = {executor.submit(load_image_from_s3, s3_client, bucket, key): key for key in keys}
        for i, future in enumerate(as_completed(future_to_key), 1):
            key = future_to_key[future]
            try:
                img = future.result()
                if img is not None:
                    images.append(img)
            except Exception as e:
                print(f"Error loading image {key}: {e}")
            
            # Print progress
            if i % 100 == 0 or i == len(keys):
                print(f"Loaded {i}/{len(keys)} images.")

    return images

# Randomly sample 20,000 keys
sampled_keys = get_random_sample_from_s3(bucket_name, prefix, sample_size=20000)

# Load sampled images with progress updates
print("Loading sampled images...")
image_data = load_images_concurrently(sampled_keys, bucket_name, s3, max_workers=20)

print(f"Total images loaded: {len(image_data)}")

# Process images in batches
def process_images_in_batches(image_data, batch_size=100):
    results = []
    for i in range(0, len(image_data), batch_size):
        batch = image_data[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} of {len(image_data) // batch_size + 1}")
        
        batch_results = model.predict(source=batch, save=False, save_txt=True, save_conf=True, save_crop=True)
        
        # Check for detections
        for result in batch_results:
            if len(result.boxes) > 0:  # If bounding boxes are detected
                result.save()  # Save the image with bounding boxes
                print(f"Saved image: {result.path}")
            else:
                print(f"No bounding boxes for image: {result.path}, skipping save.")
        
        results.extend(batch_results)  # Collect results
        time.sleep(1)  # Optional delay to manage system load
    
    return results

# Process the images in batches
print("Processing images in batches...")
results = process_images_in_batches(image_data, batch_size=100)

print("Predictions completed!")
