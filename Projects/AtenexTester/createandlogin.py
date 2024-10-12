import requests

# Superuser login details (Replace with your actual superuser credentials)
SUPERUSER_EMAIL = "supercharm@email.com"
SUPERUSER_PASSWORD = "8$JF46^5GoNgCJ1!WjRj"

# Base API URL (Update if necessary)
BASE_URL = "http://127.0.0.1:8000/api/"

# Helper function to log in and get the JWT token
def login(email, password):
    """
    Log in a user using their email and password.
    Returns a JWT access token if successful, or None if login fails.
    """
    response = requests.post(f"{BASE_URL}token/", json={
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        data = response.json()
        print(f"Login successful for {email}.")
        return data.get('access')
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

# Function to attempt Superuser creation via API (this should fail)
def create_superuser_api():
    print("\n=== Attempt to Create Superuser via API ===")
    superuser_data = {
        "email": "superadmin@example.com",
        "first_name": "Super",
        "last_name": "Admin",
        "password": "super_password",
        "role": "superuser",  # Attempt to set role to superuser
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}users/", json=superuser_data)
    if response.status_code == 403:
        print("Superuser creation via API is forbidden (expected behavior).")
    else:
        print(f"Unexpected behavior: Superuser created via API. Status: {response.status_code}")
        print(response.json())

# Function to log in as Superuser
def login_superuser():
    print("\n=== Login with Superuser ===")
    superuser_token = login(SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    if not superuser_token:
        print("Superuser login failed. Exiting.")
        return None
    print("Superuser login successful.")
    return superuser_token

# Function to create Platform Admin (Superuser must be logged in)
def create_platform_admin(superuser_token):
    print("\n=== Create Platform Admin ===")
    platform_admin_data = {
        "email": "newadmin2@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "newpass12322",
        "role": "platform_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", superuser_token, platform_admin_data)
    if response.status_code == 201:
        print("Platform Admin created successfully.")
        return response.json()  # Return Platform Admin data
    else:
        print(f"Failed to create Platform Admin. Status: {response.status_code}")
        print(response.json())
        return None

# Function to log in as Platform Admin
def login_platform_admin():
    print("\n=== Login with Platform Admin ===")
    platform_admin_token = login("newadmin2@example.com", "NewSecurePassword123!")
    if not platform_admin_token:
        print("Platform Admin login failed. Exiting.")
        return None
    print("Platform Admin login successful.")
    return platform_admin_token

# Function to create an Organization (Platform Admin must be logged in)
def create_organization(platform_admin_token):
    print("\n=== Create Organization ===")
    organization_data = {
        "name": "Test Organization",
        "address": "123 Test St",
        "contact_email": "contact@test.com",
        "contact_phone": "123-456-7890"
    }
    response = auth_request("POST", "organizations/", platform_admin_token, organization_data)
    if response.status_code == 201:
        print("Organization created successfully.")
        return response.json()  # Return Organization data
    else:
        print(f"Failed to create Organization. Status: {response.status_code}")
        print(response.json())
        return None

# Function to create Org Admin (Platform Admin must be logged in)
def create_org_admin(platform_admin_token):
    print("\n=== Create Org Admin ===")
    org_admin_data = {
        "email": "orgadmin@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "orgadmin_password",
        "role": "org_admin",
        "is_active": True
    }
    response = auth_request("POST", "users/", platform_admin_token, org_admin_data)
    if response.status_code == 201:
        print("Org Admin created successfully.")
        return response.json()  # Return Org Admin data
    else:
        print(f"Failed to create Org Admin. Status: {response.status_code}")
        print(response.json())
        return None

# Function to log in as Org Admin
def login_org_admin():
    print("\n=== Login with Org Admin ===")
    org_admin_token = login("orgadmin@example.com", "orgadmin_password")
    if not org_admin_token:
        print("Org Admin login failed. Exiting.")
        return None
    print("Org Admin login successful.")
    return org_admin_token

# Function to create Regular User (Org Admin must be logged in)
def create_regular_user(org_admin_token):
    print("\n=== Create Regular User ===")
    regular_user_data = {
        "email": "regularuser@example.com",
        "first_name": "Regular",
        "last_name": "User",
        "password": "regular_password",
        "role": "regular_user",
        "is_active": True
    }
    response = auth_request("POST", "users/", org_admin_token, regular_user_data)
    if response.status_code == 201:
        print("Regular User created successfully.")
        return response.json()  # Return Regular User data
    else:
        print(f"Failed to create Regular User. Status: {response.status_code}")
        print(response.json())
        return None

# Function to log in as Regular User
def login_regular_user():
    print("\n=== Login with Regular User ===")
    regular_user_token = login("regularuser@example.com", "regular_password")
    if not regular_user_token:
        print("Regular User login failed. Exiting.")
        return None
    print("Regular User login successful.")
    return regular_user_token

if __name__ == "__main__":
    # Run individual tests by commenting or uncommenting the calls below

    # Test 1: Attempt to create Superuser via API (should fail)
    #create_superuser_api()

    # Test 2: Log in as Superuser
    # superuser_token = login_superuser()
    #
    # # # Test 3: Create Platform Admin (after Superuser login)
    # if superuser_token:
    #     create_platform_admin(superuser_token)
    # #
    # # # Test 4: Log in as Platform Admin
    # platform_admin_token = login_platform_admin()
    # #
    # # # Test 5: Create Organization (after Platform Admin login)
    # if platform_admin_token:
    #  create_organization(platform_admin_token)
    # #
    # # # Test 6: Create Org Admin (after Platform Admin login)
    # if platform_admin_token:
    #    create_org_admin(platform_admin_token)
    #
    # # Test 7: Log in as Org Admin
    # org_admin_token = login_org_admin()
    #
    # # Test 8: Create Regular User (after Org Admin login)
    # if org_admin_token:
    #   create_regular_user(org_admin_token)
    #
    # # Test 9: Log in as Regular User
     login_regular_user()
