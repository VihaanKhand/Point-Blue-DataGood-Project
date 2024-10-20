import os
import requests

base_url = 'https://deju-penguinscience.s3-us-east-2.amazonaws.com/UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'

download_dir = os.path.expanduser("~/Desktop/UAVCensusImages")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {image_url}")
    except requests.exceptions.HTTPError as err:
        print(f"Failed to download {image_url}: {err}")

def download_all_images(start_index, end_index):
    print("Starting the download process...")
    
    for i in range(start_index, end_index + 1):
        image_filename = f'croz_spsk_2023-12-19_lcc169_99_{i}.jpg'
        image_url = os.path.join(base_url, image_filename)
        save_path = os.path.join(download_dir, image_filename)
        
        response = requests.head(image_url)
        if response.status_code == 200:
            download_image(image_url, save_path)
        else:
            print(f"Image not found: {image_url}")

if __name__ == "__main__":
    start_index = 533  
    end_index = 1000   
    download_all_images(start_index, end_index)
