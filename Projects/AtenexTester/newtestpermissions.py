import requests

# Superuser login details
SUPERUSER_EMAIL = "supercharm@email.com"
SUPERUSER_PASSWORD = "8$JF46^5GoNgCJ1!WjRj"

# Platform Admin login details
PLATFORM_ADMIN_EMAIL = "newadmin2@example.com"
PLATFORM_ADMIN_PASSWORD = "NewSecurePassword123!"

# New Org Admin login details
ORG_ADMIN_EMAIL = "neworddddgadmin@example.com"
ORG_ADMIN_PASSWORD = "newoddddrgadmin_password"

# Base API URL
BASE_URL = "http://127.0.0.1:8000/api/"

# Helper function to log in and get the JWT token
def login(email, password):
    """
    Log in a user using their email and password.
    Returns a JWT access token if successful, or None if login fails.
    """
    response = requests.post(f"{BASE_URL}token/", json={"email": email, "password": password})
    if response.status_code == 200:
        print(f"Login successful for {email}.")
        return response.json().get('access')
    else:
        print(f"Login failed for {email}. Status code: {response.status_code}")
        print(response.text)  # Print error details for debugging
        return None

# Helper function to send authenticated requests (GET, POST, PUT, DELETE)
def auth_request(method, endpoint, token, data=None):
    """
    Sends authenticated HTTP requests (GET, POST, PUT, DELETE) using the provided JWT token.
    """
    headers = {"Authorization": f"Bearer {token}"}
    if method == "GET":
        return requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    elif method == "POST":
        return requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    elif method == "PUT":
        return requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    elif method == "DELETE":
        return requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
    return None

# Function to create Org Admin
def create_org_admin(platform_admin_token):
    """Function to create a new Org Admin."""
    print("\n=== Creating Org Admin ===")
    org_admin_data = {
        "email": ORG_ADMIN_EMAIL,
        "first_name": "New",
        "last_name": "OrgAdmin",
        "password": ORG_ADMIN_PASSWORD,
        "role": "org_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", platform_admin_token, org_admin_data)
    if response.status_code == 201:
        print("Org Admin created successfully.")
    else:
        print(f"Failed to create Org Admin. Status: {response.status_code}")
        print(response.json())  # Print error details for debugging

# Function to test Org Admin's permissions
def test_org_admin_permissions(org_admin_token):
    """
    Tests Org Admin's ability to manage their own organization and regular users.
    Org Admin should not be able to create Platform Admins or access other organizations.
    """
    print("\n=== Testing Org Admin Permissions ===")

    # Test 1: Attempt to view Platform Admin (Org Admin should not have access)
    response = auth_request("GET", "users/", org_admin_token)  # Attempt to get all users
    if response.status_code == 403:
        print("Org Admin is correctly restricted from viewing all users.")
    else:
        print(f"Org Admin unexpectedly viewed users. Status: {response.status_code}")

    # Test 2: Attempt to edit Platform Admin (Org Admin should not have access)
    # Assuming the Platform Admin ID is known (you can change it accordingly)
    platform_admin_id = 1  # Change this to a valid Platform Admin ID
    edit_data = {
        "first_name": "Updated Name",
        "last_name": "Updated Last Name",
        "is_active": False
    }
    response = auth_request("PUT", f"users/{platform_admin_id}/", org_admin_token, edit_data)
    if response.status_code == 403:
        print("Org Admin is correctly restricted from editing Platform Admin.")
    else:
        print(f"Org Admin unexpectedly edited Platform Admin. Status: {response.status_code}")

# Main Execution Block
if __name__ == "__main__":
    # Log in as Superuser
    superuser_token = login(SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    if superuser_token:
        # Create Org Admin using Platform Admin Token
        platform_admin_token = login(PLATFORM_ADMIN_EMAIL, PLATFORM_ADMIN_PASSWORD)
        if platform_admin_token:
            create_org_admin(platform_admin_token)

            # Log in as the newly created Org Admin
            org_admin_token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)
            if org_admin_token:
                # Test Org Admin permissions
                test_org_admin_permissions(org_admin_token)
