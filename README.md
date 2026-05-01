# ShadowMapper - Passive Recon Suite

A Python-based passive reconnaissance tool for security researchers and penetration testers. Discover subdomains and historical URLs from public sources without active scanning.

## Features

- **Subdomain Discovery**: Find subdomains using Certificate Transparency logs (crt.sh)
- **Historical URL Mapping**: Retrieve archived URLs from Wayback Machine with robust retry logic
- **Sensitive Data Detection**: Identify potentially sensitive files and endpoints (configs, backups, API keys, etc.)
- **Colorized Output**: Enhanced terminal UI with color-coded results

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd ShadowMapper

# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On Windows:
myenv\Scripts\activate
# On Linux/Mac:
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Then input the target domain when prompted:
```
Input target domain (eg: target.com): example.com
```

### Output Example

```
=== ShadowMapper: Passive Recon Suite ===

Input target domain (eg: target.com): example.com
[+] Found 42 unique subdomains.
  - api.example.com
  - mail.example.com
  - admin.example.com
  ... (showing first 10)

------------------------------
[+] Found 156 historical URLs.
  - https://example.com/api/v1/users
  - https://example.com/admin/config
  ... (showing first 10)

[!] Found 8 potentially sensitive URLs:
  [SENSITIVE] -> https://example.com/.env
  [SENSITIVE] -> https://example.com/config.php
  [SENSITIVE] -> https://example.com/backup.sql
  ... and 5 other findings.
```

## Tools Used

### Data Sources

- **crt.sh**: Certificate Transparency logs for subdomain enumeration
- **Wayback Machine**: Historical URL archive from web.archive.org

### Key Libraries

- `requests`: HTTP client with robust retry mechanism
- `colorama`: Cross-platform colored terminal output
- `urllib3`: HTTP client with retry strategy support

## How It Works

### 1. Subdomain Discovery (crt_sh.py)
- Queries Certificate Transparency logs via crt.sh API
- Extracts unique subdomain names from SSL certificate data
- Removes wildcards and duplicates automatically

### 2. Historical URL Fetching (wayback.py)
- Connects to Wayback Machine CDX API
- Implements retry logic with exponential backoff
- Handles timeouts gracefully (60s timeout, 3 retries)
- Uses proper User-Agent headers to avoid blocking

### 3. Sensitive URL Filtering
- Scans URLs for common sensitive patterns:
  - Configuration files (`.env`, `config.php`, `web.config`, etc.)
  - Backup files (`.bak`, `.old`, `.sql`, `.db`)
  - API credentials and tokens
  - Hidden directories (`.git`, `.svn`)
  - Compressed archives (`.zip`)

## Project Structure

```
ShadowMapper/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── core/
    ├── __init__.py        # Package initializer
    ├── crt_sh.py          # Subdomain enumeration module
    └── wayback.py         # Historical URL + filtering module
```

## Requirements

See `requirements.txt` for full list:
- `requests` - HTTP library
- `colorama` - Terminal colors
- `python-dotenv` - Environment variable management
- `tqdm` - Progress bars
- `urllib3` - URL parsing and retry utilities

## Error Handling

The tool includes comprehensive error handling:

- **Timeout Errors**: Graceful timeout with retry mechanism
- **Connection Errors**: Clear messages with troubleshooting tips
- **Rate Limiting**: Exponential backoff strategy
- **Invalid JSON**: Handles malformed API responses

## Disclaimer

**Legal Notice**: This tool is designed for authorized security testing and reconnaissance only. Users are responsible for ensuring they have proper authorization before using this tool on any target. Unauthorized access to computer systems is illegal.

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

MIT License - See LICENSE file for details

## Author

**~prime**
- GitHub: [@primesatya](https://github.com/primesatya)

## Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## Changelog

### Version 1.0 (Initial Release)
- Subdomain discovery via Certificate Transparency
- Historical URL mapping from Wayback Machine
- Sensitive URL detection
- Robust error handling with retry logic
