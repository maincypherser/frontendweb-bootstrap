import requests

# Set your RapNet API credentials here
client_id = "IIKbgarRvnvpQocrf2dpTSN46kKuF6Sn"      # Replace with your actual Client ID
client_secret = "55DHjEj36WWVp-fm3ZT-x5FR-HVOlFFeLcCZ_AqVXOv_A1P6S8sewnpMPrPgsBqX"  # Replace with your actual Client Secret

def get_bearer_token(client_id, client_secret):
    """
    Function to get a Bearer token from the RapNet API.

    Args:
    - client_id (str): Your Client ID
    - client_secret (str): Your Client Secret

    Returns:
    - str: Bearer token if successful
    """
    url = "https://authztoken.api.rapaport.com/api/get"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")

def fetch_rapnet_data(token, shape="Round"):
    """
    Function to fetch the price list for a specific shape from RapNet.

    Args:
    - token (str): Bearer token for authentication
    - shape (str): Shape of the diamond (e.g., "Round", "Pear")

    Returns:
    - list: JSON response with price data
    """
    url = f"https://technet.rapnetapis.com/pricelist/api/Prices/list?shape={shape}&csvnormalized=true"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data for {shape}: {response.status_code} {response.text}")

if __name__ == "__main__":
    try:
        # Get the Bearer Token
        token = get_bearer_token(client_id, client_secret)
        print("Bearer Token:", token)

        # Fetch data for Round shape
        shape = "Round"
        price_data = fetch_rapnet_data(token, shape)
        print(f"Price Data for {shape}:\n", price_data)

        # Fetch data for Pear shape
        shape = "Pear"
        price_data = fetch_rapnet_data(token, shape)
        print(f"Price Data for {shape}:\n", price_data)

    except Exception as e:
        print("Error:", e)
