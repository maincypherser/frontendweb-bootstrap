import paramiko
import requests
import socket
import ssl
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed certs
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Target host and ports
TARGET_IP = "3.253.253.227"
PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3000: "Custom Service"
}

# Output report list
report = []


# Function to log messages
def log_message(message):
    print(message)
    report.append(message)


# Add section titles to report for better formatting
def add_section_title(title):
    report.append("\n")
    report.append("=" * len(title))
    report.append(title)
    report.append("=" * len(title))
    report.append("\n")


# Function to test SSH vulnerabilities
def test_ssh(target_ip):
    add_section_title("Testing SSH Service (Port 22)")
    log_message(f"Description: Testing for SSH vulnerabilities including weak credentials and connection issues.")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Testing with commonly used weak credentials for SSH
        client.connect(target_ip, port=22, username='root', password='weakpassword', timeout=5)
        log_message("[-] Vulnerability Found: Weak SSH credentials (username: root, password: weakpassword)")
    except paramiko.AuthenticationException:
        log_message("[+] SSH is secure: No weak credentials allowed.")
    except Exception as e:
        log_message(f"[!] Error during SSH test: {str(e)}")
    finally:
        client.close()


# Function to test HTTP and HTTPS for common vulnerabilities
def test_http_https(target_ip, port):
    service_name = PORTS[port]
    add_section_title(f"Testing {service_name} (Port {port})")
    log_message(
        f"Description: Testing for common web server vulnerabilities, status checks, and information disclosure.")

    url = f"http://{target_ip}" if port == 80 else f"https://{target_ip}"

    try:
        # Handle HTTP vs HTTPS requests
        if port == 443:
            response = requests.get(url, timeout=5, verify=False)  # Disable SSL verification for HTTPS
        else:
            response = requests.get(url, timeout=5)

        if response.status_code == 200:
            log_message(f"[+] {service_name} is reachable and returned status code 200 (OK).")
            # Basic vulnerability checks
            if "X-Powered-By" in response.headers:
                log_message(
                    f"[-] Vulnerability Found: Possible information disclosure: X-Powered-By header ({response.headers['X-Powered-By']}).")
            if "Server" in response.headers:
                log_message(f"[-] Vulnerability Found: Server information disclosed: {response.headers['Server']}.")
            # Adding a basic directory check for 404 or server configuration issues
            dir_test = requests.get(f"{url}/nonexistent", timeout=5)
            if dir_test.status_code == 404:
                log_message(f"[+] Directory Check Passed: Custom 404 page returned for nonexistent directory.")
            else:
                log_message(
                    f"[-] Directory Check Failed: Unexpected response code for nonexistent directory: {dir_test.status_code}")
        else:
            log_message(f"[-] {service_name} returned status code {response.status_code}. Check the server response.")

    except requests.exceptions.SSLError as ssl_error:
        log_message(f"[!] SSL Error: {ssl_error}. This could indicate an invalid or self-signed certificate.")
    except requests.exceptions.ConnectionError as conn_error:
        log_message(f"[!] Connection Error: {conn_error}. The service might be down or a firewall is blocking access.")
    except Exception as e:
        log_message(f"[!] Error testing {service_name}: {str(e)}")


# Function to test custom port 3000
def test_port_3000(target_ip):
    add_section_title("Testing Custom Service (Port 3000)")
    log_message(f"Description: Testing for services running on port 3000 (commonly Node.js/Express).")
    try:
        response = requests.get(f"http://{target_ip}:3000", timeout=5)
        if response.status_code == 200:
            log_message("[+] Custom service on port 3000 is reachable and returned status code 200 (OK).")
            # Example check: identify common frameworks like Node.js
            if "X-Powered-By" in response.headers and "Express" in response.headers["X-Powered-By"]:
                log_message(
                    "[-] Vulnerability Found: Node.js Express framework detected (Potential for Express-specific vulnerabilities).")
        else:
            log_message(f"[-] Custom service on port 3000 returned status code {response.status_code}.")
    except requests.exceptions.ConnectionError:
        log_message(
            f"[!] Connection Error: Could not establish a connection to the custom service on port 3000. The service might be down or blocked.")
    except Exception as e:
        log_message(f"[!] Error testing custom service on port 3000: {str(e)}")


# Function to save the report to a file
def save_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"security_report_{timestamp}.txt"

    with open(report_filename, "w") as report_file:
        report_file.write("\n".join(report))

    print(f"[*] Detailed report saved to {report_filename}")


# Main function to run tests
def run_tests():
    add_section_title("Penetration Testing Report")
    log_message(f"Target IP: {TARGET_IP}")
    log_message(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_message("\n")

    # Test SSH (port 22)
    test_ssh(TARGET_IP)

    # Test HTTP (port 80) and HTTPS (port 443)
    test_http_https(TARGET_IP, 80)
    test_http_https(TARGET_IP, 443)

    # Test custom service (port 3000)
    test_port_3000(TARGET_IP)

    # Save the report to a file
    save_report()


# Run the tests
if __name__ == "__main__":
    run_tests()
