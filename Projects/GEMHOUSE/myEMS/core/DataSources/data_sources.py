import requests
from bs4 import BeautifulSoup
from datetime import datetime
from myEMS.core.models import HistoricalDiamondPrice  #

def scrape_bluenile():
    url = 'https://www.bluenile.com/diamond-search?resultsView=List&...'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching BlueNile data: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    gallery_items = soup.find_all('div', class_='gallery-list-item-wrapper')

    for item in gallery_items:
        try:
            # Extract the attributes (example: adjust based on actual HTML structure)
            shape = item.find('div', {'data-wrapper': 'shape'}).get_text(strip=True)
            carat = float(item.find('div', {'data-wrapper': 'carat'}).get_text(strip=True))
            cut = item.find('div', {'data-wrapper': 'cut'}).get_text(strip=True)
            clarity = item.find('div', {'data-wrapper': 'clarity'}).get_text(strip=True)
            price = float(item.find('div', {'data-wrapper': 'price'}).get_text(strip=True).replace('€', ''))

            # Save the extracted data to the model
            HistoricalDiamondPrice.objects.create(
                source="BlueNile",
                shape=shape,
                carat=carat,
                cut=cut,
                clarity=clarity,
                price=price,
            )
            print(f"BlueNile diamond saved: {shape}, {carat} carat, {price}€")

        except Exception as e:
            print(f"Error processing BlueNile item: {e}")


def scrape_77diamonds():
    url = "https://www.77diamonds.com/api/shop/diamond-list"
    payload = {...}  # Keep the payload as in your previous example

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching 77Diamonds data: {e}")
        return

    diamonds = data.get("Diamonds", [])

    for diamond in diamonds:
        try:
            shape = diamond.get("ShapeName", "N/A")
            carat = float(diamond.get("CaratWeight", 0))
            cut = diamond.get("Cut", "N/A")
            clarity = diamond.get("Clarity", "N/A")
            price = float(diamond.get("Price", "0").replace("€ ", ""))
            certificate = diamond.get("Lab", "N/A")

            # Save the data to the database
            HistoricalDiamondPrice.objects.create(
                source="77Diamonds",
                shape=shape,
                carat=carat,
                cut=cut,
                clarity=clarity,
                price=price,
                certificate=certificate,
            )
            print(f"77Diamonds diamond saved: {shape}, {carat} carat, {price}€")

        except Exception as e:
            print(f"Error processing 77Diamonds item: {e}")


def get_bearer_token(client_id, client_secret):
    url = "https://authztoken.api.rapaport.com/api/get"
    headers = {"Content-Type": "application/json"}
    data = {"client_id": client_id, "client_secret": client_secret}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")


def scrape_rapnet():
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    token = get_bearer_token(client_id, client_secret)

    url = "https://technet.rapaport.com/HTTP/JSON/RetailFeed/GetDiamonds.aspx"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "GetDiamondsRequest": {
            "PageNumber": 1,
            "PageSize": 50,
            "SortBy": "Price",
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        diamonds = response.json().get("Diamonds", [])
    except requests.RequestException as e:
        print(f"Error fetching RapNet data: {e}")
        return

    for diamond in diamonds:
        try:
            shape = diamond.get("Shape", "N/A")
            carat = float(diamond.get("CaratWeight", 0))
            color = diamond.get("Color", "N/A")
            clarity = diamond.get("Clarity", "N/A")
            price = float(diamond.get("Price", 0))
            certificate = diamond.get("Certificate", "N/A")

            # Save the data to the database
            HistoricalDiamondPrice.objects.create(
                source="RapNet",
                shape=shape,
                carat=carat,
                color=color,
                clarity=clarity,
                price=price,
                certificate=certificate,
            )
            print(f"RapNet diamond saved: {shape}, {carat} carat, {price}€")

        except Exception as e:
            print(f"Error processing RapNet item: {e}")


if __name__ == "__main__":
    import sys

    # Check if an argument is passed from the terminal (which function to run)
    if len(sys.argv) > 1:
        function_name = sys.argv[1]

        if function_name == "scrape_bluenile":
            print("Running BlueNile Scraper...")
            scrape_bluenile()
        elif function_name == "scrape_77diamonds":
            print("Running 77Diamonds Scraper...")
            scrape_77diamonds()
        elif function_name == "scrape_rapnet":
            print("Running RapNet Scraper...")
            scrape_rapnet()
        else:
            print(f"Unknown function: {function_name}")
    else:
        print("Please provide a function name to run: 'scrape_bluenile', 'scrape_77diamonds', or 'scrape_rapnet'")
