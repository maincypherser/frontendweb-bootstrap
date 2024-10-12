import requests
from datetime import datetime
import random

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/"
ORG_ADMIN_EMAIL = "neworgadmin_1727959093@example.com"
ORG_ADMIN_PASSWORD = "SecurePasswordForOrgAdmin!"  # Use the actual password for the Org Admin


# Function to log in and get a JWT token
def login(email, password):
    response = requests.post(f"{BASE_URL}token/", json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json().get('access')
    else:
        print(f"Failed to log in: {response.status_code}, {response.text}")
        return None


# Function to create a regular user
def create_regular_user(token):
    # Prepare user data with a unique email
    unique_suffix = random.randint(1000000000, 9999999999)
    user_data = {
        "email": f"newregularuser_{unique_suffix}@example.com",
        "first_name": "New",
        "last_name": "RegularUser",
        "password": "SecurePasswordForNewUser!",
        "role": "regular_user"  # Role set as regular_user
    }

    # Create the regular user
    response = requests.post(f"{BASE_URL}users/", headers={"Authorization": f"Bearer {token}"}, json=user_data)

    if response.status_code == 201:
        print(f"Regular user created successfully: {response.json()}")
    else:
        print(f"Failed to create regular user: {response.status_code}, {response.text}")


# Main function to run the tests
def main():
    # Step 1: Log in as Org Admin
    token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)
    if not token:
        return

    print(f"Logged in as Org Admin '{ORG_ADMIN_EMAIL}' successfully!")

    # Step 2: Create a Regular User
    create_regular_user(token)


# Run the main function
if __name__ == "__main__":
    main()
