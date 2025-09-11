# Mist Network Troubleshooter

A Python script for automated troubleshooting of Mist network connectivity issues.

## Features

- Authentication and authorization issue detection
- DHCP/DNS problem analysis
- Client health metrics monitoring
- AP uptime checking
- Detailed recommendations based on findings
- Multiple organization support
- Automated organization selection

## Prerequisites

- Python 3.6+
- Mist API token
- Organization ID (optional - can be auto-detected)
- Client IP address
- Client MAC address

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/mist-network-troubleshooter.git
cd mist-network-troubleshooter
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python mist_troubleshoot.py \
  --token "your_mist_api_token" \
  --client-ip "192.168.1.100" \
  --client-mac "aa:bb:cc:dd:ee:ff"
```

### With Specific Organization ID
```bash
python mist_troubleshoot.py \
  --token "your_mist_api_token" \
  --org-id "your_org_id" \
  --client-ip "192.168.1.100" \
  --client-mac "aa:bb:cc:dd:ee:ff"
```

### List Available Organizations
```bash
python mist_troubleshoot.py --token "your_mist_api_token" --list-orgs
```

## Output Examples

The script provides detailed analysis output including:
- Authentication/Authorization issues
- DHCP/DNS problems
- Client health metrics
- AP status and recommendations
- Detailed troubleshooting steps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Security Note

Never commit your Mist API token to version control. Always provide it as a command-line argument or environment variable.
