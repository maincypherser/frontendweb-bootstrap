import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from myEMS.core.models import HistoricalDiamondPrice


# List of diamond shapes to scrape
diamond_shapes = [
    'round', 'princess-cut', 'cushion-cut', 'emerald-cut',
    'oval-cut', 'asscher-cut', 'marquise-cut', 'heart-shaped',
    'pear-shaped'
]

# Base URL (without shape, which will be added dynamically)
base_url = 'https://www.bluenile.com/diamond-search?CaratFrom=0.05&Color=K,J,I,H,G,F,E,D&Clarity=SI2,SI1,VS2,VS1,VVS2,VVS1,IF,FL&Cut=Good,Very+Good,Ideal,AstorIdeal'


def extract_diamond_details(title_text):
    """Extracts carat, color, clarity, cut, and shape from the title string."""
    try:
        parts = title_text.split()

        # Extracting diamond details from the title string
        carat = float(parts[0])  # Example: "0.30" -> Carat
        color = parts[1].split('-')[0]  # Example: "J-SI1" -> Color: J
        clarity = parts[1].split('-')[1]  # Example: "J-SI1" -> Clarity: SI1
        cut = parts[3]  # Example: "Excellent" -> Cut
        shape = parts[-1]  # Shape can be derived from the last word

        return carat, color, clarity, cut, shape
    except Exception as e:
        print(f"Error extracting diamond details: {e}")
        return None, None, None, None, None


def scrape_bluenile():
    """Scrapes Blue Nile diamonds for multiple shapes and stores data in the database."""

    # Iterate through each diamond shape
    for shape in diamond_shapes:
        print(f"\nStarting scrape for {shape} diamonds...")

        # Build the URL for the current shape
        url = f"{base_url}&Shape={shape}"

        try:
            # Send request to fetch the HTML content
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text
            print(f"HTML content fetched successfully for {shape} diamonds.")

        except requests.RequestException as e:
            print(f"Error fetching data for {shape} diamonds: {e}")
            continue  # Skip to the next shape if an error occurs

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"HTML content parsed for {shape} diamonds.")

        # Extract the base domain
        base_domain = urlparse(url).netloc

        # Find all diamond items
        gallery_items = soup.find_all('div', class_='bn_comp_itemData_a82a6e')

        for item in gallery_items:
            try:
                # Extract price (e.g., "€244")
                price_tag = item.find('div', class_='price--GUo2yxzV2va4P7Bqe00G')
                price = float(price_tag.get_text(strip=True).replace('€', '').replace(',', '')) if price_tag else 'N/A'

                # Extract diamond details from the title
                title_tag = item.find('h3', class_='bn_comp_itemTitle_a82a6e')
                if title_tag:
                    carat, color, clarity, cut, _ = extract_diamond_details(title_tag.get_text(strip=True))
                else:
                    carat, color, clarity, cut = None, None, None, None

                # These fields are not available in the HTML sample provided:
                polish = 'N/A'  # Marked as missing
                symmetry = 'N/A'  # Marked as missing
                certificate = 'N/A'  # Marked as missing

                # Print the extracted data for verification
                print(f"\nExtracted Data for {shape} diamond:")
                print(f"  - Carat: {carat}")
                print(f"  - Color: {color}")
                print(f"  - Clarity: {clarity}")
                print(f"  - Cut: {cut}")
                print(f"  - Price: {price}€")
                print(f"  - Shape: {shape}")

                # Save the diamond data to the Django model
                new_entry = HistoricalDiamondPrice.objects.create(
                    source="BlueNile",
                    shape=shape,
                    carat=carat,
                    price=price,
                    clarity=clarity,
                    color=color,  # Added color field
                    cut=cut,
                    polish=polish,
                    symmetry=symmetry,
                    certificate=certificate
                )

                # Verify that data was added to the database
                if new_entry.id:  # Assuming Django automatically generates an ID
                    print(f"✅ Successfully added to the database: {new_entry}")

            except Exception as e:
                print(f"Error processing item for {shape} diamonds: {e}")

    print("\nScraping completed.")


if __name__ == "__main__":
    # Run the scraper function
    print("Running BlueNile Scraper...\n")
    scrape_bluenile()
    print("\nFinished running BlueNile scraper.")
