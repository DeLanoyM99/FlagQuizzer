import os
import requests
from bs4 import BeautifulSoup

# Make a GET request to the website
response = requests.get('https://www.countryflags.com/')

# Create a BeautifulSoup object
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <img> tags with the class "flag-img" and width="120"
flag_images = soup.find_all('img')

# Create a directory to save the images
os.makedirs('flags', exist_ok=True)

# Download and save each image
for img in flag_images:
    # Get the image URL
    img_url = img['src']

    # Get the country name from the alt attribute
    country_name = img['alt'].replace('flag of ', '')  # Remove "flag of" prefix

    # Generate the filename for the image
    filename = f'flag_of_{country_name}.png'

    # Download the image
    image_data = requests.get(img_url).content

    # Save the image to the "flags" directory
    with open(f'flags/{filename}', 'wb') as f:
        f.write(image_data)

    print(f'Saved {filename}')

print('All flags downloaded and saved.')
