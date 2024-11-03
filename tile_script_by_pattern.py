import os
import requests

base_url = 'https://deju-penguinscience.s3-us-east-2.amazonaws.com/UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'

download_dir = os.path.expanduser("~/Desktop/UAVCensusImages")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

log_file_path = os.path.join(download_dir, "download_log.txt")

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {image_url}")
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Downloaded: {image_url}\n")
    except requests.exceptions.HTTPError as err:
        print(f"Failed to download {image_url}: {err}")
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Image not found: {image_url}\n")

def download_images():
    print("Starting the download process...")
    # LIST OF PATTERNS---this script will only grab images that lead with the 99, 9, 98 formats. Change the patterns accordingly.
    filename_patterns = [
        'croz_spsk_2023-12-19_lcc169_13_{}.jpg',
        'croz_spsk_2023-12-19_lcc169_139_{}.jpg',
        'croz_spsk_2023-12-19_lcc169_169_{}.jpg'
    ]
    
    for i in range(1, 1000):  
        for pattern in filename_patterns:
            filename = pattern.format(i)
            image_url = os.path.join(base_url, filename)
            save_path = os.path.join(download_dir, filename)

            # Check if the URL exists before downloading
            response = requests.head(image_url)
            if response.status_code == 200:
                download_image(image_url, save_path)
                break  # Break the loop after a successful download
            else:
                print(f"Image not found: {image_url}")
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"Image not found: {image_url}\n")

if __name__ == "__main__":
    download_images()
