import requests
import json

from catalyst_center_utils import *

# Disable SSL warnings (only use this in testing environments)
requests.packages.urllib3.disable_warnings()

# API details
BASE_URL = "https://sandboxdnac.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "Cisco123!"

def main():
    # Get authentication token
    token = get_auth_token(BASE_URL, USERNAME, PASSWORD)
    total_sites = get_site_count(BASE_URL, token)
    all_sites = []  # List to store all devices from all pages

    for counter in range(1, -(-total_sites // 50) + 1):
        devices_url = f"{BASE_URL}/dna/intent/api/v1/site-health?limit=50&offset=" + str(counter)
        headers = {
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        }
        try:
            response = requests.get(
                devices_url,
                headers=headers,
                verify=False  # Disable SSL verification (only for testing)
            )
            response.raise_for_status()
            page_devices = response.json()
            
            # Append the devices from this page to our list of all devices
            if 'response' in page_devices:
                all_sites.extend(page_devices['response'])
            else:
                print(f"Unexpected response structure on page {counter}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching devices on page {counter}: {e}")
            # Continue to the next iteration instead of exiting
            continue

    return json.dumps(all_sites, indent=4)

if __name__ == "__main__":
    main()