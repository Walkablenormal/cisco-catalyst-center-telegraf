import json
import requests

from catalyst_center_utils import get_auth_token, get_site_count
from config import BASE_URL, USERNAME, PASSWORD, SSL_VERIFY

def main():
    """
    Returns site health information from Catalyst Center.
    """
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
                verify=SSL_VERIFY,
                timeout=60
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

    print(json.dumps(all_sites, indent=4))

if __name__ == "__main__":
    main()
