from core.crt_sh import fetch_subdomains
from core.wayback import fetch_wayback_urls, grep_sensitive_urls
from colorama import Fore, Style, init

# Initiating colorama for colored output in terminal
init(autoreset=True)

def main():
    print(f"{Fore.YELLOW}=== ShadowMapper: Passive Recon Suite ===\n")
    target = input("Input target domain (eg: target.com): ")
    
    # Subdomain Discovery
    subs = fetch_subdomains(target)
    print(f"{Fore.GREEN}[+] Found {len(subs)} unique subdomains.")
    for s in subs[:10]: # Display only the first 10 to avoid clutter
        print(f"  - {s}")

    print("-" * 30)

    # Wayback URLs Discovery
    urls = fetch_wayback_urls(target)
    print(f"{Fore.CYAN}[+] Found {len(urls)} historical URLs.")
    for u in urls[:10]:
        print(f"  - {u}")

    # Sensitive URL Filtering
    sensitive_urls = grep_sensitive_urls(urls)
    if sensitive_urls:
        print(f"\n{Fore.RED}[!] Found {len(sensitive_urls)} potentially sensitive URLs:")
        # Display a maximum of 20 sensitive findings to avoid cluttering the screen
        for sensitive_url in sensitive_urls[:20]:
            print(f"  {Fore.RED}[SENSITIVE]{Style.RESET_ALL} -> {sensitive_url}")
        
        if len(sensitive_urls) > 20:
            print(f"  ... and {len(sensitive_urls) - 20} other findings.")
    else:
        print(f"{Fore.GREEN}[+] No common sensitive file patterns found.")
        
if __name__ == "__main__":
    main()