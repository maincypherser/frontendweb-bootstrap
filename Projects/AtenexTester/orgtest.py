import requests

# Superuser login details
SUPERUSER_EMAIL = "supercharm@email.com"
SUPERUSER_PASSWORD = "8$JF46^5GoNgCJ1!WjRj"

# New Platform Admin login details
PLATFORM_ADMIN_EMAIL = "newsplatformadmin@example.com"
PLATFORM_ADMIN_PASSWORD = "SecurePasswordForPlatformAdmin!"

# New Organization details
ORG_NAME = "T3333333"
ORG_ADDRESS = "123 Testing Lane"
ORG_CONTACT_EMAIL = "contact@neworganization.com"
ORG_CONTACT_PHONE = "1234567890"

# New Org Admin login details
ORG_ADMIN_EMAIL = "new3333333n@example.com"
ORG_ADMIN_PASSWORD = "SecurePasswordForOrgAdmin!"

# Base API URL
BASE_URL = "http://127.0.0.1:8000/api/"

# Helper function to log in and get the JWT token
def login(email, password):
    response = requests.post(f"{BASE_URL}token/", json={"email": email, "password": password})
    print(f"Logging in {email}...")  # Verbose output
    print(f"HTTP Response: {response.status_code} - {response.text}")  # Show HTTP response

    if response.status_code == 200:
        print(f"Login successful for {email}.")
        return response.json().get('access')
    else:
        print(f"Login failed for {email}. Status code: {response.status_code}")
        return None

# Helper function to send authenticated requests (GET, POST)
def auth_request(method, endpoint, token, data=None):
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Sending {method} request to {endpoint}...")  # Verbose output

    if method == "GET":
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    elif method == "POST":
        response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    else:
        return None

    print(f"HTTP Response: {response.status_code} - {response.text}")  # Show HTTP response
    return response

# Function to create a new Platform Admin
def create_platform_admin(superuser_token):
    """Function to create a new Platform Admin."""
    print("\n=== Creating Platform Admin ===")
    platform_admin_data = {
        "email": PLATFORM_ADMIN_EMAIL,
        "first_name": "New",
        "last_name": "PlatformAdmin",
        "password": PLATFORM_ADMIN_PASSWORD,
        "role": "platform_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", superuser_token, platform_admin_data)
    if response.status_code == 201:
        print("Platform Admin created successfully.")
    else:
        print(f"Failed to create Platform Admin. Status: {response.status_code}")
        print(response.json())  # Print error details for debugging

# Function to create an organization
def create_organization(platform_admin_token):
    """Function to create a new organization."""
    print("\n=== Creating Organization ===")
    org_data = {
        "name": ORG_NAME,
        "address": ORG_ADDRESS,
        "contact_email": ORG_CONTACT_EMAIL,
        "contact_phone": ORG_CONTACT_PHONE
    }
    response = auth_request("POST", "organizations/", platform_admin_token, org_data)
    if response.status_code == 201:
        print("Organization created successfully.")
        org_id = response.json().get('id')  # Extract the Org ID
        print(f"New Organization Org ID: {org_id}")
        return org_id
    else:
        print(f"Failed to create organization. Status: {response.status_code}")
        return None

# Function to create Org Admin
def create_org_admin(platform_admin_token, org_id):
    """Function to create a new Org Admin."""
    print("\n=== Creating Org Admin ===")
    org_admin_data = {
        "email": ORG_ADMIN_EMAIL,
        "first_name": "Test",
        "last_name": "OrgAdmin",
        "password": ORG_ADMIN_PASSWORD,
        "role": "org_admin",
        "is_active": True,
        "organization_id": org_id  # Include Org ID
    }
    response = auth_request("POST", "users/", platform_admin_token, org_admin_data)
    if response.status_code == 201:
        print("Org Admin created successfully with Org ID.")
    else:
        print(f"Failed to create Org Admin. Status: {response.status_code} - {response.text}")

# Main Execution Block
if __name__ == "__main__":
    # Log in as Superuser
    superuser_token = login(SUPERUSER_EMAIL, SUPERUSER_PASSWORD)

    if superuser_token:
        # Create Platform Admin
        create_platform_admin(superuser_token)

        # Log in as the newly created Platform Admin
        platform_admin_token = login(PLATFORM_ADMIN_EMAIL, PLATFORM_ADMIN_PASSWORD)

        if platform_admin_token:
            # Create Organization and retrieve Org ID
            org_id = create_organization(platform_admin_token)

            if org_id:
                # Create Org Admin
                create_org_admin(platform_admin_token, org_id)
