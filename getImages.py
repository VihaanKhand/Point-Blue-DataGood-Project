import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Create an S3 client without authentication (anonymous access)
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Define your bucket and folder prefix
bucket_name = 'deju-penguinscience'
prefix = 'UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'

# Define the paths for the labels and images directories
MAIN_DIR = '/Users/sushrut.g12/Desktop/PointBlue/Point-Blue-DataGood-Project/Labelled Images'
LABELS_DIR = os.path.join(MAIN_DIR, 'labels')
IMAGES_DIR = os.path.join(MAIN_DIR, 'images')

# Iterate through each .txt file in the labels directory
for txt_file in os.listdir(LABELS_DIR):
    if txt_file.endswith('.txt'):
        # Get the image filename by changing the extension to .jpg (or correct image extension)
        image_name = txt_file.replace('.txt', '.jpg')  # Adjust if images use a different extension

        # Define the S3 key by appending the image name to the prefix
        s3_key = f'{prefix}{image_name}'

        # Download the image
        try:
            local_image_path = os.path.join(IMAGES_DIR, image_name)
            s3.download_file(bucket_name, s3_key, local_image_path)
            print(f"Downloaded {image_name} to {local_image_path}")
        except Exception as e:
            print(f"Failed to download {image_name}: {e}")

print("All images downloaded.")
