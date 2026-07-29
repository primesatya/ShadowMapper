# 🗺️ ShadowMapper - Passive Recon Suite

[![Security Gate](https://github.com/primesatya/ShadowMapper/actions/workflows/security-gate.yml/badge.svg)](https://github.com/primesatya/ShadowMapper/actions/workflows/security-gate.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Advanced passive reconnaissance suite for security researchers and penetration testers.** Discover subdomains and historical URLs from public sources without active scanning.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [💻 Usage](#-usage)
- [🔍 How It Works](#-how-it-works)
- [🏗️ Project Structure](#️-project-structure)
- [🛡️ Security & Quality](#️-security--quality)
- [⚠️ Requirements](#️-requirements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- **🔎 Subdomain Discovery**  
  Find subdomains using Certificate Transparency logs (crt.sh) with automatic deduplication

- **📜 Historical URL Mapping**  
  Retrieve archived URLs from Wayback Machine with intelligent retry logic and exponential backoff

- **🚨 Sensitive Data Detection**  
  Identify potentially sensitive files and endpoints (configs, backups, API keys, etc.)

- **🎨 Colorized Output**  
  Enhanced terminal UI with color-coded results for better readability

- **⚡ Robust Error Handling**  
  Comprehensive exception handling with graceful fallbacks and informative error messages

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/primesatya/ShadowMapper.git
cd ShadowMapper

# Create and activate virtual environment
python -m venv myenv

# Windows
myenv\Scripts\activate
# Linux/Mac
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the tool
python main.py
```

---

## 📦 Installation


### 📋 Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **git** (for cloning repository)

### 🔧 Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/primesatya/ShadowMapper.git
cd ShadowMapper

# 2. Create virtual environment
python -m venv myenv

# 3. Activate virtual environment
# On Windows:
myenv\Scripts\activate
# On Linux/Mac:
source myenv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage


### 🎯 Basic Command

```bash
python main.py
```

### 📥 Input

Simply provide the target domain when prompted:

```
Input target domain (eg: target.com): example.com
```

### 📤 Sample Output

```
=== ShadowMapper: Passive Recon Suite ===

Input target domain (eg: target.com): example.com

[*] Fetching subdomains from Certificate Transparency...
[+] Found 42 unique subdomains.
    • api.example.com
    • mail.example.com
    • admin.example.com
    ... (showing first 10)

[*] Fetching historical URLs from Wayback Machine...
[+] Found 156 historical URLs.
    • https://example.com/api/v1/users
    • https://example.com/admin/config
    • https://example.com/api/v2/accounts
    ... (showing first 10)

[!] Found 8 potentially sensitive URLs:
    [SENSITIVE] → https://example.com/.env
    [SENSITIVE] → https://example.com/config.php
    [SENSITIVE] → https://example.com/backup.sql
    [SENSITIVE] → https://example.com/.git/config
    ... and 4 other findings.

[✓] Scan completed in 2.45 seconds
```

---

## 🔍 How It Works

### 1️⃣ Subdomain Discovery (crt_sh.py)

- Queries **Certificate Transparency logs** via crt.sh API
- Extracts unique subdomain names from SSL certificate data
- Automatically removes wildcards and duplicates
- Returns comprehensive list of discovered subdomains

### 2️⃣ Historical URL Fetching (wayback.py)

- Connects to **Wayback Machine CDX API**
- Implements retry logic with exponential backoff (2s, 4s, 8s)
- Handles timeouts gracefully (60-second timeout, max 3 retries)
- Uses proper User-Agent headers to avoid blocking
- Session pooling for efficient HTTP connections

### 3️⃣ Sensitive Data Detection

- Scans URLs for common sensitive patterns:
  - Configuration files: `.env`, `config.php`, `web.config`, etc.
  - Backup files: `.bak`, `.old`, `.sql`, `.db`, `.sqlite`
  - Version control: `.git`, `.svn`, `.hg`
  - API & credentials: files containing `api_key`, `token`, `password`
  - Compressed archives: `.zip`, `.tar.gz`, `.rar`

---

## 🏗️ Project Structure


```
ShadowMapper/
├── main.py                          # 🎯 Entry point
├── requirements.txt                 # 📦 Python dependencies
├── README.md                        # 📖 Documentation (this file)
├── LICENSE                          # ⚖️ MIT License
├── .gitignore                       # 🚫 Git ignore rules
├── .github/
│   └── workflows/
│       └── security-gate.yml        # 🛡️ Security scanning pipeline
└── core/
    ├── __init__.py                  # Package initializer
    ├── crt_sh.py                    # 🔎 Subdomain enumeration module
    └── wayback.py                   # 📜 Historical URL + filtering module
```

---

## ⚙️ Requirements

The project requires the following Python packages:

| Package | Purpose |
|---------|---------|
| `requests` | HTTP library with session management |
| `colorama` | Cross-platform terminal color output |
| `python-dotenv` | Environment variable management |
| `tqdm` | Progress bars for user feedback |
| `urllib3` | URL parsing and retry utilities |

All dependencies are listed in `requirements.txt` and can be installed via:

```bash
pip install -r requirements.txt
```

---

## 🛡️ Security & Quality

This project includes comprehensive security measures:

### 🔐 Automated Security Scanning

The repository is protected by **Security Gate** GitHub Actions workflow that runs on every push and pull request:

- **🔴 TruffleHog**: Detects high-entropy secrets (API keys, tokens, credentials)
- **🟢 GitGuardian**: Verifies against known secret signatures database
- **🟡 Semgrep**: Static Application Security Testing (SAST) for code vulnerabilities
- **🟣 Detect-Secrets**: Custom baseline for tracking allowed secrets
- **🔵 Custom Patterns**: Regex-based detection for common secrets

### ✅ Security Practices

- ✓ No secrets hardcoded in repository
- ✓ All sensitive files properly added to `.gitignore`
- ✓ Environment variables via `.env` (never committed)
- ✓ Code scanning on every commit
- ✓ Permission-based GitHub Actions

### 📊 Workflow Status

See the [Security Gate workflow](https://github.com/primesatya/ShadowMapper/actions/workflows/security-gate.yml) for detailed scan results.

---

## ⚠️ Error Handling


The tool includes robust error handling for common scenarios:

| Error | Handling |
|-------|----------|
| **Timeout Errors** | Automatic retry with exponential backoff (max 3 attempts) |
| **Connection Errors** | Clear error messages with troubleshooting tips |
| **Rate Limiting (429)** | Graceful handling with retry-after header support |
| **Invalid JSON** | Malformed API responses are handled gracefully |
| **Network Issues** | Fallback mechanisms and user-friendly error messages |

---

## 🚨 Disclaimer & Legal Notice

⚠️ **Important**: This tool is designed for **authorized security testing and reconnaissance only**.

- Users are **responsible** for ensuring they have proper authorization before using this tool
- Unauthorized access to computer systems is **illegal**
- Use of this tool is subject to all applicable laws and regulations
- The author assumes no liability for misuse or damage caused by this tool

**Always obtain written permission before conducting security assessments.**

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 📝 How to Contribute

1. **Report Bugs**: Open a GitHub issue with detailed description
2. **Suggest Features**: Discuss new ideas in GitHub discussions
3. **Submit PRs**: Fork the repository and create a pull request

### 📋 Contribution Guidelines

- Follow the existing code style (PEP 8)
- Add tests for new features
- Update documentation as needed
- Ensure all security checks pass (Security Gate workflow)

### 🔀 Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 ShadowMapper Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👤 Author

**~prime** (primesatya)

- 🐙 GitHub: [@primesatya](https://github.com/primesatya)
- 💼 LinkedIn: Available upon request
- 📧 Contact: Available in GitHub profile

---

## 📞 Support & Issues

Have questions or encountered an issue?

### 📍 Getting Help

1. **Check Existing Issues**: [GitHub Issues](https://github.com/primesatya/ShadowMapper/issues)
2. **Create New Issue**: Include:
   - Error message / logs
   - Steps to reproduce
   - Python version
   - Operating system
3. **Provide Details**: More info = faster solution

---

## 📈 Changelog

### Version 1.0 (Initial Release)

**Features:**
- ✨ Subdomain discovery via Certificate Transparency
- ✨ Historical URL mapping from Wayback Machine
- ✨ Sensitive data detection
- ✨ Colorized terminal output

**Improvements:**
- ⚡ Robust error handling with retry logic
- 🛡️ Security scanning pipeline (Security Gate)
- 📖 Comprehensive documentation

---

## 🎓 Learning Resources

### Related Tools & Services

- [crt.sh](https://crt.sh/) - Certificate Transparency Search
- [Wayback Machine](https://web.archive.org/) - Internet Archive
- [OWASP](https://owasp.org/) - Web Application Security

### Security Testing Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne](https://www.hackerone.com/) - Bug Bounty Platform
- [SANS](https://www.sans.org/) - Security Training

---

## ⭐ Show Your Support

If you found this project helpful, please consider:

- ⭐ Starring this repository
- 🔗 Sharing with others
- 🐛 Reporting issues
- 🚀 Contributing improvements

---

<div align="center">

**Made by primesatya**

[⬆ Back to Top](#-shadowmapper---passive-recon-suite)

</div>
