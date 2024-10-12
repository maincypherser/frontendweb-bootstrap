import requests

# Superuser login details
SUPERUSER_EMAIL = "supercharm@email.com"
SUPERUSER_PASSWORD = "8$JF46^5GoNgCJ1!WjRj"

# Platform Admin login details
PLATFORM_ADMIN_EMAIL = "newadmin2@example.com"
PLATFORM_ADMIN_PASSWORD = "NewSecurePassword123!"

# Org Admin login details
ORG_ADMIN_EMAIL = "neworgadmin@example.com"  # Updated if necessary
ORG_ADMIN_PASSWORD = "orgadmin_password2"  # Update if the password changed

# Regular User login details
REGULAR_USER_EMAIL = "regularuser@example.com"
REGULAR_USER_PASSWORD = "regular_password"

# Base API URL (adjust as needed)
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

# Function to test Superuser's permissions
def test_superuser_permissions(superuser_token):
    """
    Tests Superuser's ability to view, create, update, and delete users, organizations, and agents.
    Superuser should have full access.
    """
    print("\n=== Testing Superuser Permissions ===")

    # Test 1: View all users
    response = auth_request("GET", "users/", superuser_token)
    if response.status_code == 200:
        print("Superuser can view all users.")
    else:
        print(f"Superuser failed to view all users. Status: {response.status_code}")

    # Test 2: Create a new Platform Admin
    platform_admin_data = {
        "email": "newplatformadmin@example.com",
        "first_name": "Platform",
        "last_name": "Admin",
        "password": "platform_password",
        "role": "platform_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", superuser_token, platform_admin_data)
    if response.status_code == 201:
        print("Superuser created a new Platform Admin successfully.")
    else:
        print(f"Superuser failed to create a Platform Admin. Status: {response.status_code}")

    # Test 3: Attempt to delete a Platform Admin (replace ID with actual admin ID)
    # Assume ID 5 is the new Platform Admin's ID for testing
    response = auth_request("DELETE", "users/5/", superuser_token)
    if response.status_code == 204:
        print("Superuser deleted Platform Admin successfully.")
    else:
        print(f"Superuser failed to delete Platform Admin. Status: {response.status_code}")

# Function to test Platform Admin's permissions
def test_platform_admin_permissions(platform_admin_token):
    """
    Tests Platform Admin's ability to manage organizations and users.
    Platform Admin should not have access to create/delete superusers.
    """
    print("\n=== Testing Platform Admin Permissions ===")

    # Test 1: View all organizations
    response = auth_request("GET", "organizations/", platform_admin_token)
    if response.status_code == 200:
        print("Platform Admin can view all organizations.")
    else:
        print(f"Platform Admin failed to view organizations. Status: {response.status_code}")

    # Test 2: Create a new Org Admin
    org_admin_data = {
        "email": "neworgadmin@example.com",
        "first_name": "Org",
        "last_name": "Admin",
        "password": "orgadmin_password2",
        "role": "org_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", platform_admin_token, org_admin_data)
    if response.status_code == 201:
        print("Platform Admin created a new Org Admin successfully.")
    else:
        print(f"Platform Admin failed to create Org Admin. Status: {response.status_code}")

    # Test 3: Attempt to create Superuser
    superuser_data = {
        "email": "fake_superuser@example.com",
        "first_name": "Fake",
        "last_name": "Superuser",
        "password": "fake_super_password",
        "role": "superuser",
        "is_active": True
    }
    response = auth_request("POST", "users/", platform_admin_token, superuser_data)
    if response.status_code == 403:
        print("Platform Admin is correctly restricted from creating Superuser.")
    else:
        print(f"Platform Admin unexpectedly created a Superuser. Status: {response.status_code}")

# Function to test Org Admin's permissions
def test_org_admin_permissions(org_admin_token):
    """
    Tests Org Admin's ability to manage their own organization and regular users.
    Org Admin should not be able to create Platform Admins or access other organizations.
    """
    print("\n=== Testing Org Admin Permissions ===")

    # Test 1: View own organization
    response = auth_request("GET", "organizations/", org_admin_token)
    if response.status_code == 200:
        print("Org Admin can view their organization.")
    else:
        print(f"Org Admin failed to view organization. Status: {response.status_code}")

    # Test 2: Attempt to create Platform Admin
    platform_admin_data = {
        "email": "illegaladmin@example.com",
        "first_name": "Illegal",
        "last_name": "Admin",
        "password": "illegal_password",
        "role": "platform_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", org_admin_token, platform_admin_data)
    if response.status_code == 403:
        print("Org Admin is correctly restricted from creating Platform Admin.")
    else:
        print(f"Org Admin unexpectedly created a Platform Admin. Status: {response.status_code}")

# Function to test Regular User's permissions
def test_regular_user_permissions(regular_user_token):
    """
    Tests Regular User's ability to access their own data.
    Regular User should not be able to create or manage other users or organizations.
    """
    print("\n=== Testing Regular User Permissions ===")

    # Test 1: View own profile
    response = auth_request("GET", "users/me/", regular_user_token)  # Fetching own profile
    if response.status_code == 200:
        print("Regular User can view their own profile.")
    else:
        print(f"Regular User failed to view their profile. Status: {response.status_code}")

    # Test 2: Attempt to create another user
    regular_user_data = {
        "email": "newregularuser@example.com",
        "first_name": "New",
        "last_name": "Regular",
        "password": "newregular_password",
        "role": "regular_user",
        "is_active": True
    }
    response = auth_request("POST", "users/", regular_user_token, regular_user_data)
    if response.status_code == 403:
        print("Regular User is correctly restricted from creating other users.")
    else:
        print(f"Regular User unexpectedly created another user. Status: {response.status_code}")

if __name__ == "__main__":
    # Superuser tests
    superuser_token = login(SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    if superuser_token:
        test_superuser_permissions(superuser_token)

    # Platform Admin tests
    platform_admin_token = login(PLATFORM_ADMIN_EMAIL, PLATFORM_ADMIN_PASSWORD)
    if platform_admin_token:
        test_platform_admin_permissions(platform_admin_token)

    # Org Admin tests
    org_admin_token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)
    if org_admin_token:
        test_org_admin_permissions(org_admin_token)

    # Regular User tests
    regular_user_token = login(REGULAR_USER_EMAIL, REGULAR_USER_PASSWORD)
    if regular_user_token:
        test_regular_user_permissions(regular_user_token)
