import requests
import random

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/"
ORG_ADMIN_EMAIL = "neworgadmin_1727959093@example.com"
ORG_ADMIN_PASSWORD = "SecurePasswordForOrgAdmin!"


def login(email, password):
    """Log in as Org Admin and return the access token."""
    login_url = f"{BASE_URL}token/"
    response = requests.post(login_url, json={"email": email, "password": password})

    if response.status_code == 200:
        print(f"Logged in as Org Admin '{email}' successfully!")
        return response.json().get('access')
    else:
        print(f"Login failed: {response.status_code}, {response.text}")
        return None


def create_regular_user(token):
    """Create a new regular user linked to the Org Admin's organization."""
    email_suffix = random.randint(1000000000, 9999999999)  # Generate unique suffix
    email = f"newregularuser_{email_suffix}@example.com"  # Unique email

    user_data = {
        "email": email,
        "first_name": "New",
        "last_name": "RegularUser",
        "password": "SecurePasswordForNewUser!",
        "role": "regular_user"
    }

    # Set the headers with the access token
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}users/", headers=headers, json=user_data)

    if response.status_code == 201:
        print(f"Regular user created successfully: {response.json()}")
    else:
        print(f"Failed to create regular user: {response.status_code}, {response.text}")


def main():
    # Step 1: Log in and get token
    token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)

    # Step 2: If login was successful, create a new regular user
    if token:
        create_regular_user(token)


# Run the main function
if __name__ == "__main__":
    main()
