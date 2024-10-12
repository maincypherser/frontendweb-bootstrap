import requests
import json
import csv
from datetime import datetime

# Define the URL and payload
url = "https://www.77diamonds.com/api/shop/diamond-list"
payload = {
    "itemId": -1,
    "categoryId": 7,
    "currentPage": 1,
    "resultsPerPage": 20,
    "stoneType": "1",
    "diamondType": "-1",
    "minCarat": "0.76",
    "maxCarat": 30,
    "isGroupedShapes": False,
    "showPairs": False,
    "minPrice": 118.0178,
    "maxPrice": 40000,
    "minRatio": 1,
    "maxRatio": 5,
    "withMedia": False,
    "minDepth": 0,
    "maxDepth": 0,
    "minTable": 0,
    "maxTable": 0,
    "quickShipping": False,
    "searchBlocked": False,
    "language": 1,
    "country": 724,
    "currency": 2,
    "shapes": ["10"],
    "colors": [16, 20, 21, 22, 19, 15, 17],
    "intensities": [],
    "clarities": [42, 41, 40, 44, 39],
    "certificates": [],
    "cuts": [58, 57],
    "polishes": [],
    "symmetries": [],
    "fluorescences": [],
    "gemClarity": [],
    "gemIntensity": [],
    "gemTreatment": [],
    "gemClarityTreatment": [],
    "discount-code": None,
    "diamondsInBag": [],
    "expressItemsInBag": [],
    "engravingsInBag": 0,
    "url": "https://www.77diamonds.com/radiant-cut-diamonds?item=-1"
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# CSV file name
csv_filename = "diamonds_data.csv"

try:
    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Check for HTTP errors
    data = response.json()

    # Extract relevant data
    diamonds = data.get("Diamonds", [])  # Extract diamonds list

    # Write to CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["DateTime", "BaseDomain", "Shape", "Carat", "Cut", "Clarity", "Price", "Shipping Date"])

        # Get current datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_domain = "www.77diamonds.com"

        # Write diamond data
        for diamond in diamonds:
            shape = diamond.get("ShapeName", "N/A")
            carat = diamond.get("CaratWeight", "N/A")
            cut = diamond.get("Cut", "N/A")
            clarity = diamond.get("Clarity", "N/A")
            price = diamond.get("Price", "N/A").replace("€ ", "€")
            shipping_date = diamond.get("DeliveryDate", "N/A")

            writer.writerow([current_time, base_domain, shape, carat, cut, clarity, price, shipping_date])

    print(f"Data saved to {csv_filename}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
