import os
import requests
from bs4 import BeautifulSoup

# Remove all flags that are not official countries
# URL of the webpage to scrape
url = "https://www.worldometers.info/geography/alphabetical-list-of-countries/"

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object with the response text
soup = BeautifulSoup(response.text, "html.parser")

# Find all <td> elements with the specified style
td_elements = soup.find_all("td", style="font-weight: bold; font-size:15px")

# Extract the text content from the <td> elements and store in a list
country_list = [td.get_text(strip=True) for td in td_elements]

# Append "Kosovo" and "Palestine" to the country list
country_list.append("Kosovo")
country_list.append("Palestine")

# Append additional countries to the country list
additional_countries = [
    "Cape Verde",
    "Côte d’ Ivoire",
    "East Timor",
    "Myanmar",
    "Swaziland",
    "São Tomé and Príncipe",
    "Taiwan",
    "Vatican City"
]
country_list.extend(additional_countries)

# Remove files from the "flags" directory
flags_directory = "flags"

for filename in os.listdir(flags_directory):
    if "," in filename:
        continue

    if filename.startswith("flag_of_Flag of"):
        # Extract country name from the filename
        country_name = filename.replace("flag_of_Flag of", "").replace(".png", "").strip()

        # Skip iterations for country names containing "North" or "South"
        if "North" in country_name or "South" in country_name:
            continue

        # Check if the country name exists in the country list
        if country_name not in country_list:
            file_path = os.path.join(flags_directory, filename)
            os.remove(file_path)
            print(f"Removed file: {filename}")
