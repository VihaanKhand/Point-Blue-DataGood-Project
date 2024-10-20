import boto3
from botocore import UNSIGNED
from botocore.client import Config
import os

# Create an S3 client without authentication (anonymous access)
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Define your bucket and folder prefix
bucket_name = 'deju-penguinscience'
prefix = 'UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'


# Initialize variables for pagination
continuation_token = None
all_objects = []

# Loop to paginate through all objects
while True:
    if continuation_token:
        # Fetch the next set of objects
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
    else:
        # Fetch the first set of objects
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Add current batch of objects to the list
    if 'Contents' in response:
        all_objects.extend(response['Contents'])
        print(f"Retrieved {len(response['Contents'])} objects (total: {len(all_objects)})")
    
    # Check if more objects need to be fetched
    if response.get('IsTruncated'):
        continuation_token = response['NextContinuationToken']
    else:
        # No more objects to fetch
        break

# Now all_objects contains all of the listed objects
print(f"Total objects retrieved: {len(all_objects)}")

download_folder = '/Users/sushrut.g12/Desktop/PointBlue/Point-Blue-DataGood-Project/SkuaDroneImages'
# Example: Download the images
for obj in all_objects:
    file_name = obj['Key'].split('/')[-1]  # Extract the file name
    print(f"Downloading {file_name}...")
    download_path = os.path.join(download_folder, file_name)
    s3.download_file(bucket_name, obj['Key'], download_path)
