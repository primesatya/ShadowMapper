import requests
import json

def fetch_subdomains(domain):
    print(f"[*] Searching subdomains for {domain} via crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    
    try:
        # Timeout added to prevent hanging if server is slow
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            # Parse JSON to extract unique names
            data = response.json()
            subdomains = set()  # Using set to automatically avoid duplicates
            for entry in data:
                name = entry['name_value']
                # Remove wildcards and newlines
                for sub in name.split('\n'):
                    if not sub.startswith('*.'):
                        subdomains.add(sub)
            return sorted(list(subdomains))
    except Exception as e:
        print(f"[!] Error fetching from crt.sh: {e}")
        return []