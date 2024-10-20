import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = 'https://deju-penguinscience.s3.us-east-2.amazonaws.com/UAVCensusMultiSpecies/index.html?prefix=UAVCensusMultiSpecies/croz_spsk_2023-12-19/tiles/'

# Send a request to get the page content
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the 'a' tags that contain the file links
    links = soup.find("/html/body/div[2]/pre")
    
    

    # Extract the href attribute for each link (file name)
    image_urls = [url + link['href'] for link in links if link['href'].endswith('.jpg')]
    print(soup)
    # Print all the image URLs
    for image_url in image_urls:
        print(image_url)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
