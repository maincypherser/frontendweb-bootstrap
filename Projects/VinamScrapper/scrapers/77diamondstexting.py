import requests
import json
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
    "shapes": ["10"],  # Example for round shape
    "colors": [16, 20, 21, 22, 19, 15, 17],
    "clarities": [42, 41, 40, 44, 39],
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
    "url": "https://www.77diamonds.com/round-cut-diamonds?item=-1"
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

try:
    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Check for HTTP errors

    # Print the raw JSON data from the response
    data = response.json()
    print("Raw JSON Response:")
    print(json.dumps(data, indent=4))  # Pretty-print JSON data

    # Extract relevant data if you want to go further
    diamonds = data.get("Diamonds", [])
    print("\nExtracted Diamond Data (First 5 Diamonds):")
    for diamond in diamonds[:5]:  # Display only first 5 diamonds for brevity
        print(f"Shape: {diamond.get('ShapeName', 'N/A')}, Carat: {diamond.get('CaratWeight', 'N/A')}, "
              f"Clarity: {diamond.get('Clarity', 'N/A')}, Price: {diamond.get('Price', 'N/A')}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
