import requests
import random

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/"
ORG_ADMIN_EMAIL = "neworgadmin_1727959093@example.com"
ORG_ADMIN_PASSWORD = "SecurePasswordForOrgAdmin!"  # Use the actual password for the Org Admin
ORG_ID = "7e7eeaa4-3837-4d07-9417-66a625d320f0"  # Organization ID associated with the Org Admin

# Function to log in and get a JWT token
def login(email, password):
    response = requests.post(f"{BASE_URL}token/", json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json().get('access')
    else:
        print(f"Failed to log in: {response.status_code}, {response.text}")
        return None

# Function to create a unique regular user email
def generate_unique_email():
    return f"newregularuser_{random.randint(1000000000, 9999999999)}@example.com"

# Function to run Org Admin tests
def run_org_admin_tests(token):
    results = []

    # Test 1: View own profile
    response = requests.get(f"{BASE_URL}users/me/", headers={"Authorization": f"Bearer {token}"})
    results.append({
        "test": "View own profile",
        "result": "Passed" if response.status_code == 200 else "Failed",
        "details": response.json() if response.status_code == 200 else response.text
    })

    # Test 2: View OrgUser details (Org Admin's own user)
    response = requests.get(f"{BASE_URL}orgusers/?user={ORG_ADMIN_EMAIL}", headers={"Authorization": f"Bearer {token}"})
    results.append({
        "test": "View OrgUser details",
        "result": "Passed" if response.status_code == 200 else "Failed",
        "details": response.json() if response.status_code == 200 else response.text
    })

    # Test 3: Attempt to create a new organization (should fail)
    new_org_data = {
        "name": f"New Organization for Testing {random.randint(1000, 9999)}"
    }
    response = requests.post(f"{BASE_URL}organizations/", headers={"Authorization": f"Bearer {token}"}, json=new_org_data)
    results.append({
        "test": "Attempt to create a new organization",
        "result": "Passed (Expected Failure)" if response.status_code == 403 else "Failed",
        "details": response.json() if response.status_code != 201 else "Unexpected success."
    })

    # Test 4: Attempt to edit the organization (should succeed)
    edit_org_data = {
        "name": f"Updated Organization Name {random.randint(1000, 9999)}"
    }
    response = requests.put(f"{BASE_URL}organizations/{ORG_ID}/", headers={"Authorization": f"Bearer {token}"}, json=edit_org_data)
    results.append({
        "test": "Attempt to edit the organization",
        "result": "Passed" if response.status_code == 200 else "Failed",
        "details": response.json() if response.status_code == 200 else response.text
    })

    # Test 5: Attempt to create a new regular user in their organization (should succeed)
    new_user_data = {
        "email": generate_unique_email(),
        "first_name": "New",
        "last_name": "RegularUser",
        "password": "SecurePasswordForNewUser!",
        "role": "regular_user",
        "organization_id": ORG_ID  # Link to the organization
    }
    response = requests.post(f"{BASE_URL}users/", headers={"Authorization": f"Bearer {token}"}, json=new_user_data)
    results.append({
        "test": "Attempt to create a new regular user in their organization",
        "result": "Passed" if response.status_code == 201 else "Failed",
        "details": response.json() if response.status_code == 201 else response.text
    })

    # Test 6: Attempt to create a user in another organization (should fail)
    new_user_data_diff_org = {
        "email": generate_unique_email(),
        "first_name": "New",
        "last_name": "User",
        "password": "SecurePasswordForNewUser!",
        "role": "regular_user",
        "organization_id": "invalid_org_id"  # Invalid org ID to simulate a different organization
    }
    response = requests.post(f"{BASE_URL}users/", headers={"Authorization": f"Bearer {token}"}, json=new_user_data_diff_org)
    results.append({
        "test": "Attempt to create a user in another organization",
        "result": "Passed (Expected Failure)" if response.status_code == 400 else "Failed",
        "details": response.json() if response.status_code == 400 else response.text
    })

    # Test 7: Attempt to delete another Org Admin (should fail)
    org_admin_id = "another_org_admin_id"  # Replace with a valid Org Admin ID
    response = requests.delete(f"{BASE_URL}users/{org_admin_id}/", headers={"Authorization": f"Bearer {token}"})
    results.append({
        "test": "Attempt to delete another Org Admin",
        "result": "Passed (Expected Failure)" if response.status_code == 403 else "Failed",
        "details": response.json() if response.status_code == 403 else response.text
    })

    # Test 8: Attempt to view details of another Org Admin (should fail)
    org_admin_id = "another_org_admin_id"  # Replace with a valid Org Admin ID
    response = requests.get(f"{BASE_URL}users/{org_admin_id}/", headers={"Authorization": f"Bearer {token}"})
    results.append({
        "test": "Attempt to view details of another Org Admin",
        "result": "Passed (Expected Failure)" if response.status_code == 404 else "Failed",
        "details": response.json() if response.status_code == 404 else response.text
    })

    # Test 9: Attempt to create a superuser (should fail)
    superuser_data = {
        "email": "superuser@example.com",
        "first_name": "Super",
        "last_name": "User",
        "password": "SuperSecurePassword!",
        "role": "superuser"
    }
    response = requests.post(f"{BASE_URL}users/", headers={"Authorization": f"Bearer {token}"}, json=superuser_data)
    results.append({
        "test": "Attempt to create a superuser",
        "result": "Passed (Expected Failure)" if response.status_code == 400 else "Failed",
        "details": response.json() if response.status_code == 400 else response.text
    })

    # Print results
    for result in results:
        print(f"{result['test']}: {result['result']}, Details: {result['details']}")

# Main script execution
if __name__ == "__main__":
    token = login(ORG_ADMIN_EMAIL, ORG_ADMIN_PASSWORD)
    if token:
        run_org_admin_tests(token)
