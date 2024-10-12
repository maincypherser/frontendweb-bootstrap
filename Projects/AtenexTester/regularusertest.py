import requests

# Regular User login details
REGULAR_USER_EMAIL = "newregularuser@example.com"  # Update with the actual email
REGULAR_USER_PASSWORD = "SecurePasswordForRegularUser!"  # Update with the actual password

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


# Helper function to view OrgUser details
def view_org_user(token):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}orgusers/", headers=headers)  # Endpoint for OrgUser
    print("Attempting to view OrgUser details...")
    print(f"HTTP Response: {response.status_code} - {response.json()}")  # Show HTTP response


# Main Execution Block
if __name__ == "__main__":
    # Log in as Regular User
    regular_user_token = login(REGULAR_USER_EMAIL, REGULAR_USER_PASSWORD)

    if regular_user_token:
        # Step: View OrgUser Details
        view_org_user(regular_user_token)
