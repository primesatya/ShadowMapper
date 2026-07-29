from core.crt_sh import fetch_subdomains
from core.wayback import fetch_wayback_urls, grep_sensitive_urls
from colorama import Fore, Style, init
from datetime import datetime
from pathlib import Path

# Initiating colorama for colored output in terminal
init(autoreset=True)


def build_report(target, subs, urls, sensitive_urls):
    lines = [
        "ShadowMapper Report",
        "===================",
        f"Target: {target}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Discovered subdomains: {len(subs)}",
    ]

    if subs:
        lines.append("")
        lines.append("Subdomains:")
        lines.extend(f"  - {sub}" for sub in subs)

    lines.append("")
    lines.append(f"Historical URLs found: {len(urls)}")
    if urls:
        lines.append("")
        lines.append("Wayback URLs:")
        lines.extend(f"  - {u}" for u in urls)

    lines.append("")
    lines.append(f"Sensitive URLs detected: {len(sensitive_urls)}")
    if sensitive_urls:
        lines.append("")
        lines.append("Sensitive URLs:")
        lines.extend(f"  - {u}" for u in sensitive_urls)

    return "\n".join(lines)


def save_report(target, subs, urls, sensitive_urls):
    project_root = Path(__file__).resolve().parent
    report_dir = project_root / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    safe_target = "".join(c if c.isalnum() or c in "-._" else "_" for c in target)
    default_name = f"shadowmapper_report_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = report_dir / default_name

    report_text = build_report(target, subs, urls, sensitive_urls)
    output_path.write_text(report_text, encoding="utf-8")
    return output_path


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

    if input("\nSave report to file? [y/N]: ").strip().lower().startswith("y"):
        output_path = save_report(target, subs, urls, sensitive_urls)
        print(f"{Fore.GREEN}[+] Report saved to {output_path.resolve()}")
        print(f"{Fore.GREEN}[+] Report folder: {output_path.parent}")

if __name__ == "__main__":
    main()