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

- Python 3.6 or higher
- Mist API token (obtain from Mist Dashboard → Organization → API Tokens)
- Organization ID (optional - can be auto-detected)
- Client IP address or Client MAC address (at least one required)
- Network access to Mist API endpoints

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rockban31/mist-network-troubleshooter.git
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

### Using Environment Variables (Recommended)
```bash
export MIST_API_TOKEN="your_mist_api_token"
python mist_troubleshoot.py \
  --client-ip "192.168.1.100" \
  --client-mac "aa:bb:cc:dd:ee:ff"
```

### List Available Organizations
```bash
python mist_troubleshoot.py --token "your_mist_api_token" --list-orgs
```

### Help
```bash
python mist_troubleshoot.py --help
```

## Output Examples

The script provides detailed analysis output including:

- **Authentication/Authorization issues**: Token validation and permission checks
- **DHCP/DNS problems**: IP assignment and name resolution analysis
- **Client health metrics**: Signal strength, throughput, and connection stability
- **AP status and recommendations**: Access point health and optimization suggestions
- **Detailed troubleshooting steps**: Step-by-step remediation guidance

### Sample Output
```
=== Mist Network Troubleshooter ===
Organization: Example Corp (org-id: 12345678-1234-5678-9012-123456789012)
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff

✓ Authentication successful
✓ Client found in network
⚠ DHCP lease time expiring soon (2 hours remaining)
✗ DNS resolution issues detected

Recommendations:
1. Renew DHCP lease
2. Check DNS server configuration
3. Verify AP signal strength (-65 dBm detected)
```

## Configuration

### Environment Variables
- `MIST_API_TOKEN`: Your Mist API token
- `MIST_ORG_ID`: Default organization ID (optional)

### Command Line Arguments
- `--token`: Mist API token (required if not set via environment)
- `--org-id`: Organization ID (optional, auto-detected if not provided)
- `--client-ip`: Client IP address
- `--client-mac`: Client MAC address
- `--list-orgs`: List available organizations
- `--verbose`: Enable verbose output
- `--output`: Output format (json, text) - default: text

## Troubleshooting

### Common Issues

**Invalid API Token**
```
Error: Authentication failed. Please check your API token.
```
Solution: Verify your token in Mist Dashboard → Organization → API Tokens

**Rate Limiting**
```
Error: API rate limit exceeded. Please wait before retrying.
```
Solution: Wait 60 seconds before running the script again

**Client Not Found**
```
Warning: Client not found in the specified organization.
```
Solution: Verify the client IP/MAC and ensure the client is connected

**Network Connectivity**
```
Error: Unable to connect to Mist API endpoints.
```
Solution: Check internet connectivity and firewall settings

## Requirements

Create a `requirements.txt` file with:
```
requests>=2.25.1
argparse>=1.4.0
json-logging>=1.3.0
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 mist_troubleshoot.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Notes

- **Never commit your Mist API token to version control**
- Use environment variables or secure credential management systems
- Rotate API tokens regularly
- Ensure minimum required API permissions are granted
- Use HTTPS for all API communications (enabled by default)

## Changelog

### v1.0.0
- Initial release with basic troubleshooting features
- Support for authentication and DHCP analysis
- Multi-organization support

## Support

For support and questions:
- Create an issue in this repository
- Check the [Mist API Documentation](https://api.mist.com/api/v1/docs/)
- Review common troubleshooting steps above

## Acknowledgments

- Mist Systems for providing the API
- Contributors and community feedback