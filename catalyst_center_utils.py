import sys
import requests
from config import SSL_VERIFY

def get_auth_token(base_url, username, password):
    """
    Authenticate with Cisco Catalyst Center and get a token.
    """
    auth_url = f"{base_url}/dna/system/api/v1/auth/token"

    try:
        response = requests.post(
            auth_url,
            auth=(username, password),
            verify=SSL_VERIFY,
            timeout=60
        )
        response.raise_for_status()
        return response.json()["Token"]
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining auth token: {e}")
        sys.exit(1)

def get_network_device_count(base_url, token):
    """
    Returns integer with total amount of network devices.
    """
    url = f"{base_url}/dna/intent/api/v1/network-device/count"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            verify=SSL_VERIFY,
            timeout=60
        )
        response.raise_for_status()
        return response.json()['response']

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

def get_site_count(base_url, token):
    """
    Returns integer with total amount of sites.
    """
    url = f"{base_url}/dna/intent/api/v1/site/count"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            verify=SSL_VERIFY,
            timeout=60
        )
        response.raise_for_status()
        return response.json()['response']

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)
