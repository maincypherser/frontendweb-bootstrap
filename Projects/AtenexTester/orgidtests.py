import requests

# Superuser login details
SUPERUSER_EMAIL = "supercharm@email.com"
SUPERUSER_PASSWORD = "8$JF46^5GoNgCJ1!WjRj"

# Platform Admin login details
PLATFORM_ADMIN_EMAIL = "newspl45atformadmin@example.com"
PLATFORM_ADMIN_PASSWORD = "SecurePasswordForPlatformAdmin!"

# New Org Admin login details
ORG_ADMIN_EMAIL = "newsorgadmin@example.com"
ORG_ADMIN_PASSWORD = "SecurePasswordForOrgAdmin123!"

# New Regular User login details
REGULAR_USER_EMAIL = "newsregularuser@example.com"
REGULAR_USER_PASSWORD = "SecurePasswordForRegularUser!"

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

# Helper function to send authenticated requests (GET, POST, PUT, DELETE)
def auth_request(method, endpoint, token, data=None):
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Sending {method} request to {endpoint}...")  # Verbose output

    if method == "GET":
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    elif method == "POST":
        response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
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
        "name": "New Organization for Testing",
        "address": "456 Test Ave",
        "contact_email": "contact@testorganization.com",
        "contact_phone": "9876543210"
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
        "organization": org_id  # Include Org ID directly, assuming the backend handles it correctly
    }
    response = auth_request("POST", "users/", platform_admin_token, org_admin_data)
    if response.status_code == 201:
        print("Org Admin created successfully with Org ID.")
    else:
        print(f"Failed to create Org Admin. Status: {response.status_code} - {response.text}")

# Function to create Regular User
def create_regular_user(org_admin_token):
    """Function to create a new Regular User."""
    print("\n=== Creating Regular User ===")
    regular_user_data = {
        "email": REGULAR_USER_EMAIL,
        "first_name": "Regular",
        "last_name": "User",
        "password": REGULAR_USER_PASSWORD,
        "role": "regular_user",
        "is_active": True
        # The organization ID should not be needed here if auto-association is implemented
    }
    response = auth_request("POST", "users/", org_admin_token, regular_user_data)
    if response.status_code == 201:
        print("Regular User created successfully.")
    else:
        print(f"Failed to create Regular User. Status: {response.status_code} - {response.text}")

# Main Execution Block
if __name__ == "__main__":
    # Log in as Superuser
    # superuser_token = login(SUPERUSER_EMAIL, SUPERUSER_PASSWORD)

    # 1. Create Platform Admin
    # Uncomment to run this section
    # if superuser_token:
    #     create_platform_admin(superuser_token)

    # 2. Create Organization
    # Uncomment to run this section after creating the Platform Admin
    platform_admin_token = login(PLATFORM_ADMIN_EMAIL, PLATFORM_ADMIN_PASSWORD)
    if platform_admin_token:
        org_id = create_organization(platform_admin_token)

    # 3. Create Org Admin
    # Uncomment to run this section after creating the organization
    # if org_id:
    #     create_org_admin(platform_admin_token, org_id)

    # 4. Create Regular User
    # Uncomment to run this section after creating the Org Admin
    # org_admin_token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)
    # if org_admin_token:
    #     create_regular_user(org_admin_token)
