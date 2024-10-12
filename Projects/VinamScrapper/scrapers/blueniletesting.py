import requests
from bs4 import BeautifulSoup

# Example Blue Nile URL for diamond search (adjust as needed)
url = 'https://www.bluenile.com/diamond-search?CaratFrom=0.05&Color=K,J,I,H,G,F,E,D&Clarity=SI2,SI1,VS2,VS1,VVS2,VVS1,IF,FL&Cut=Good,Very+Good,Ideal,AstorIdeal&Shape=princess-cut'

def inspect_html():
    """Fetches and prints the HTML structure of diamond items from Blue Nile."""

    try:
        # Send request to fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
        html_content = response.text
        print("HTML content fetched successfully.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        print("HTML content parsed.")

        # Find all diamond items on the page
        gallery_items = soup.find_all('div', class_='bn_comp_itemData_a82a6e')

        # Print the raw structure of the first diamond item for inspection
        if gallery_items:
            print("HTML structure of the first diamond item:\n")
            print(gallery_items[0].prettify())  # Prettify the HTML for better readability
        else:
            print("No diamond items found on the page.")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    inspect_html()
