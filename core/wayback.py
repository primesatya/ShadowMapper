import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def fetch_wayback_urls(domain):
    print(f"[*] Fetching historical URLs from Wayback Machine for: {domain}")
    
    # Setup session with retry logic and connection pooling
    session = requests.Session()
    
    # Configure retry strategy with exponential backoff
    retry_strategy = Retry(
        total=3,  # Total retry attempts
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP status codes
        allowed_methods=["GET"],  # Only retry on GET requests
        backoff_factor=2  # Exponential backoff: 2, 4, 8 seconds
    )
    
    # Attach retry strategy to adapter
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Setup headers to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Wayback Machine CDX API endpoint (using HTTPS)
    url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey"
    
    try:
        print(f"[*] Sending request to Wayback Machine (timeout: 60s, retries: 3x)...")
        response = session.get(url, timeout=60, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        # Skip header (first row) and return unique URLs
        if len(data) > 1:
            urls = [entry[0] for entry in data[1:]]
            print(f"[+] Successfully fetched {len(urls)} URLs from Wayback Machine")
            return urls
        return []
        
    except requests.exceptions.Timeout:
        print(f"[!] Timeout: Request to Wayback Machine took too long (> 60s)")
        print(f"    Possible cause: Wayback Machine server is busy")
        print(f"    Solution: try again in a few moments")
        return []
        
    except requests.exceptions.ConnectionError as e:
        print(f"[!] Connection Error: Unable to connect to Wayback Machine")
        print(f"    Error: {e}")
        print(f"    Check your internet connection")
        return []
        
    except requests.exceptions.HTTPError as e:
        print(f"[!] HTTP Error: {e.response.status_code}")
        if e.response.status_code == 429:
            print(f"    Rate limited! Try again in a few minutes")
        elif e.response.status_code in [500, 502, 503, 504]:
            print(f"    Wayback Machine server is experiencing issues, try again later")
        return []
        
    except json.JSONDecodeError:
        print(f"[!] Response is not valid JSON. Domain may not have historical data")
        return []
        
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return []
    
    finally:
        session.close()

def grep_sensitive_urls(urls):
    """Filter URLs containing sensitive files or patterns.
    
    Args:
        urls: List of URLs to filter
        
    Returns:
        List of URLs matching sensitive patterns
    """
    # Patterns that often store confidential information
    sensitive_patterns = [
        '.env', '.git', '.svn', '.htaccess', 'config.php', 'config.js',
        'wp-config', 'settings.py', 'web.config', '.bak', '.old',
        '.sql', '.db', '.sqlite', 'backup', 'password', 'credentials',
        '.json', '.xml', 'api_key', 'token', '.zip', '.phpinfo'
    ]
    
    found_leaks = []
    
    for url in urls:
        # Make it case-insensitive to be more accurate.
        if any(pattern.lower() in url.lower() for pattern in sensitive_patterns):
            found_leaks.append(url)
            
    return found_leaks