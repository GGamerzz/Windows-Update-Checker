# Microsoft Update Connectivity Checker
Tools &amp; Scripts to test and verify connection to Windows Update services

A Python script to test DNS resolution and port connectivity (80, 443) for Microsoft Update domains. Useful for diagnosing network connectivity issues in corporate environments where Windows Update may be blocked or restricted.

## Features
- Tests DNS resolution for Microsoft Update domains
- Checks HTTP (80) and HTTPS (443) port connectivity
- Clear visual indicators for connection status
- Support for custom domains
- Multiple output modes (normal, verbose, quiet)
- Proper exit codes for automation
- No external dependencies (uses only Python standard library)

## Requirements
- Python 3.6 or higher
- No additional packages required

## Installation
```bash
git clone https://github.com/GGamerzz/connectivity-checker.git
cd connectivity-checker
```

## Usage

### Basic Usage

```bash
python connectivity_checker.py
```

### Command Line Options

```bash
python connectivity_checker.py [options]
```

| Option | Description |
|--------|-------------|
| `-d, --domains DOMAIN` | Add custom domain to test (can be used multiple times) |
| `-t, --timeout SECONDS` | Connection timeout in seconds (default: 3) |
| `-v, --verbose` | Show detailed connection attempts |
| `-q, --quiet` | Show only failed connections |
| `-h, --help` | Show help message |

### Examples

Test default Microsoft Update domains:
```bash
python connectivity_checker.py
```

Add custom domains:
```bash
python connectivity_checker.py -d google.com -d github.com
```

Verbose output with longer timeout:
```bash
python connectivity_checker.py -v -t 10
```

Quiet mode (show only failures):
```bash
python connectivity_checker.py -q
```

## Output Format

The script uses clear visual indicators:

- `[✓]` - All ports accessible
- `[!]` - Some ports blocked/unreachable  
- `[✗]` - DNS resolution failed

Example output:
```
Microsoft Update Connectivity Check
--------------------------------------------------
[✓] windowsupdate.microsoft.com         20.109.209.108:[✓80,✓443]
[!] sls.update.microsoft.com            20.12.23.50:[✗80,✓443]
[✓] download.windowsupdate.com          199.232.26.172:[✓80,✓443]

Summary: 2/3 domains fully accessible
Issues found: 1 domains with connectivity problems
```

## Default Tested Domains
- windowsupdate.microsoft.com
- update.microsoft.com
- dl.delivery.mp.microsoft.com
- sls.update.microsoft.com
- fe2.update.microsoft.com
- download.windowsupdate.com

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | All connections successful |
| 1 | Some connections failed |
| 2 | All connections failed or invalid arguments |

## Use Cases
- **Corporate Networks**: Test if Windows Update is accessible through firewalls
- **Troubleshooting**: Diagnose connectivity issues with Microsoft services
- **Network Monitoring**: Include in scripts to monitor network health
- **Automation**: Use exit codes in bash scripts or monitoring systems

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

