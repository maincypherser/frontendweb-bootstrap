import json

import requests

# Set your RapNet API credentials
CLIENT_ID = 'IIKbgarRvnvpQocrf2dpTSN46kKuF6Sn'  # Replace with your actual Client ID
CLIENT_SECRET = '55DHjEj36WWVp-fm3ZT-x5FR-HVOlFFeLcCZ_AqVXOv_A1P6S8sewnpMPrPgsBqX'  # Replace with your actual Client Secret


# Function to get the Bearer token
def get_bearer_token(client_id, client_secret):
    url = "https://authztoken.api.rapaport.com/api/get"
    headers = {"Content-Type": "application/json"}
    data = {"client_id": client_id, "client_secret": client_secret}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")


# Function to fetch inventory data and save the raw response to a text file
def fetch_inventory_data(bearer_token):
    url = "https://technet.rapnetapis.com/instant-inventory/api/Diamonds"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    # Exact request body from the documentation
    data = {
        "request": {
            "body": {
                "search_type": "White",  # For white diamonds
                "shapes": [
                    "Round", "Pear", "Princess", "Marquise", "Oval", "Radiant",
                    "Emerald", "Heart", "Cushion", "Asscher"
                ],
                "labs": ["GIA", "IGI", "AGS", "HRD", "NONE"],  # Expanded labs
                "fluorescence_intensities": ["Faint", "Medium", "Strong", "None"],  # Expanded intensities
                "fluorescence_colors": ["Blue", "Yellow", "Green", "Red", "Orange", "White"],
                "size_from": "0.2",  # Set a broader range for size (carat weight)
                "size_to": "10.0",
                "color_from": "D",  # Broad range for color
                "color_to": "M",
                "clarity_from": "IF",  # Broad range for clarity
                "clarity_to": "I3",
                "price_total_from": "100",  # Minimum price
                "price_total_to": "1000000",  # Maximum price
                "sort_by": "Price",  # Sort by price
                "sort_direction": "Asc",  # Ascending order
                "page_number": "1",  # Start with page 1
                "page_size": "50"  # Increase page size to get more data at once
            }
        }
    }# Function to fetch inventory data by shape only
def fetch_inventory_data_by_shape(bearer_token, shape):
    url = "https://technet.rapnetapis.com/instant-inventory/api/Diamonds"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    # Simplified request body to filter only by shape
    data = {
        "request": {
            "body": {
                "search_type": "White",  # For white diamonds
                "shapes": [shape],       # Filter by shape only
                "page_number": "1",       # Start with page 1
                "page_size": "20"         # Page size of 20
            }
        }
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)

    # Print and save the raw response for debugging
    print(f"Status Code: {response.status_code}")
    print("Response Headers:", response.headers)
    print("Raw Response Text:", response.text)  # Print the raw response

    # Save the raw response to a text file
    with open("rapnet_inventory_response_by_shape.txt", "w") as file:
        file.write(response.text)

    # If the request was successful, process the response
    if response.status_code == 200:
        try:
            response_json = response.json()
            diamonds_data = response_json.get('response', {}).get('body', {}).get('diamonds', [])
            total_items = len(diamonds_data)

            # Print total items retrieved and sample fields
            print(f"\nTotal diamonds retrieved: {total_items}")
            if total_items > 0:
                print("\nFields for each diamond:")
                for field in diamonds_data[0].keys():
                    print(f"- {field}")

                # Display sample data for the first few diamonds
                print("\nSample diamonds data:")
                for i, diamond in enumerate(diamonds_data[:5]):  # Print first 5 items as a sample
                    print(f"\nDiamond {i+1}:")
                    for key, value in diamond.items():
                        print(f"  {key}: {value}")
            else:
                print("No diamonds were retrieved. Check your request parameters or response.")
        except json.JSONDecodeError:
            print("Failed to decode JSON. Check the response format.")
    else:
        print(f"Failed to fetch inventory data: {response.status_code} {response.text}")

# Main function to integrate everything
if __name__ == "__main__":
    try:
        # Get the Bearer token
        token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
        print("Bearer token obtained successfully.")

        # Fetch and process the inventory data by shape only
        fetch_inventory_data_by_shape(token, "Round")  # Filter by "Round" shape

    except Exception as e:
        print(f"Error: {e}")