import boto3
from botocore import UNSIGNED
from botocore.client import Config


s3 = boto3.client('s3',  config=Config(signature_version=UNSIGNED))

bucket_name = 'deju-penguinscience'
prefix = 'UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'

# List objects in the folder
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

if 'Contents' in response:
    print(f"Found {len(response['Contents'])} objects in the folder:")
    for obj in response['Contents']:
        print(obj['Key'])  # This prints the full path of each object (image) in the folder
        
        # Example: Download each object (image)
        file_name = obj['Key'].split('/')[-1]  # Get the file name
        s3.download_file(bucket_name, obj['Key'], file_name)
        print(f"Downloaded {file_name}")
else:
    print("No objects found in the specified folder.")
