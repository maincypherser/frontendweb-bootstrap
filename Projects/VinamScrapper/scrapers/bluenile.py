import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from urllib.parse import urlparse

# Define the URL of the page to scrape
url = 'https://www.bluenile.com/diamond-search?resultsView=List&CaratFrom=1.37&CaratTo=3.1&Color=F,E,D&PriceFrom=1500&PriceTo=18500&Shape=princess-cut&Clarity=VS1,VVS2,VVS1,IF&Cut=AstorIdeal'

# Capture the current date and time
request_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Extract the base domain
base_domain = urlparse(url).netloc

# Log URL
print(f"Fetching data from URL: {url}")

try:
    # Send a request to fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    html_content = response.text
    print("HTML content fetched successfully.")
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    exit(1)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
print("HTML content parsed.")

# Open a CSV file to write the data
csv_file = '../diamonds.csv'
try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Define the CSV writer
        csvwriter = csv.writer(csvfile)

        # Write the header row to the CSV file
        csvwriter.writerow(['DateTime', 'BaseDomain', 'Shape', 'Carat', 'Cut', 'Clarity', 'Price', 'Shipping Date'])
        print(f"Header row written to {csv_file}.")

        # Find all gallery items
        gallery_items = soup.find_all('div', class_='gallery-list-item-wrapper')
        print(f"Found {len(gallery_items)} gallery items.")

        for item in gallery_items:
            try:
                # Extract data for each gallery item
                shape_tag = item.find('div', {'data-wrapper': 'shape'})
                shape = shape_tag.get_text(strip=True) if shape_tag else 'N/A'

                carat_tag = item.find('div', {'data-wrapper': 'carat'})
                carat = carat_tag.get_text(strip=True) if carat_tag else 'N/A'

                cut_tag = item.find('div', {'data-wrapper': 'cut'})
                cut = cut_tag.get_text(strip=True) if cut_tag else 'N/A'

                clarity_tag = item.find('div', {'data-wrapper': 'clarity'})
                clarity = clarity_tag.get_text(strip=True) if clarity_tag else 'N/A'

                price_tag = item.find('div', {'data-wrapper': 'price'})
                price = price_tag.get_text(strip=True) if price_tag else 'N/A'

                shipping_tag = item.find('div', {'data-wrapper': 'shipsBy'})
                shipping_date = shipping_tag.get_text(strip=True) if shipping_tag else 'N/A'

                # Write the data to the CSV file
                csvwriter.writerow([request_datetime, base_domain, shape, carat, cut, clarity, price, shipping_date])

                # Log successful data write
                print(f"Data written for diamond with shape: {shape}")
            except Exception as e:
                print(f"Error processing item: {e}")

    print(f"Data has been successfully written to {csv_file}")
except IOError as e:
    print(f"Error writing to CSV file: {e}")
