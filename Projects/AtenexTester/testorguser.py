import requests

# Org Admin login details
ORG_ADMIN_EMAIL = "neworgadmin@example.com"  # Update with the actual email
ORG_ADMIN_PASSWORD = "SecurePasswordForOrgAdmin!"  # Update with the actual password

# New Regular User details
REGULAR_USER_EMAIL = "newregularuser@example.com"  # Change this to the email you want for the regular user
REGULAR_USER_PASSWORD = "SecurePasswordForRegularUser!"
REGULAR_USER_FIRST_NAME = "New"
REGULAR_USER_LAST_NAME = "RegularUser"

# New Organization details
NEW_ORG_NAME = "Updated Organization Name"  # New name for the organization

# Base API URL
BASE_URL = "http://127.0.0.1:8000/api/"  # Update if your API URL is different


# Helper function to log in and get the JWT token
def login(email, password):
    response = requests.post(f"{BASE_URL}token/", json={"email": email, "password": password})
    print(f"Logging in {email}...")  # Verbose output
    print(f"HTTP Response: {response.status_code} - {response.text}")  # Show HTTP response

    if response.status_code == 200:
        print(f"Login successful for {email}.")
        return response.json().get('access')  # Return the access token
    else:
        print(f"Login failed for {email}. Status code: {response.status_code}")
        return None


# Helper function to create a regular user
def create_regular_user(token):
    headers = {"Authorization": f"Bearer {token}"}
    user_data = {
        "email": REGULAR_USER_EMAIL,
        "first_name": REGULAR_USER_FIRST_NAME,
        "last_name": REGULAR_USER_LAST_NAME,
        "password": REGULAR_USER_PASSWORD,
        "role": "regular_user",
        "is_active": True,
        # Optionally, you can specify the organization ID here if needed
    }

    response = requests.post(f"{BASE_URL}users/", headers=headers, json=user_data)
    print("Creating Regular User...")
    print(f"HTTP Response: {response.status_code} - {response.text}")  # Show HTTP response

    if response.status_code == 201:
        print("Regular User created successfully.")
    else:
        print("Failed to create Regular User.")


# Helper function to edit organization name
def edit_organization(token):
    headers = {"Authorization": f"Bearer {token}"}
    organization_id = "3e7fdbf6-af30-4b73-ae6b-c0eb20a81df9"  # Use the ID of the organization you want to edit

    org_data = {
        "name": NEW_ORG_NAME,
        # Add other fields to update if necessary
    }

    response = requests.patch(f"{BASE_URL}organizations/{organization_id}/", headers=headers, json=org_data)
    print("Editing Organization Name...")
    print(f"HTTP Response: {response.status_code} - {response.text}")  # Show HTTP response

    if response.status_code == 200:
        print("Organization name updated successfully.")
    else:
        print("Failed to update organization name.")


# Main Execution Block
if __name__ == "__main__":
    # Log in as Org Admin
    org_admin_token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)

    if org_admin_token:
        # Create Regular User
        create_regular_user(org_admin_token)

        # Edit Organization Name
        edit_organization(org_admin_token)
