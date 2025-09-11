# Mist Troubleshooting Script

A Python script to help troubleshoot Mist network connectivity issues.

## Installation

Clone this repository and ensure you have Python 3.6+ installed.

## Usage

```bash
python mist_troubleshoot.py \
  --token "your_mist_api_token" \
  --org-id "your_org_id" \
  --client-ip "192.168.1.100" \
  --client-mac "aa:bb:cc:dd:ee:ff"
```

## Sample Outputs

### Scenario 1: Authentication/Authorization Issues Detected

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
✅ Client found: John-Laptop on AP 5c:5b:35:aa:bb:cc

[2/5] Analyzing client events and logs...

[3/5] Checking authentication and authorization...

🔴 AUTHENTICATION/AUTHORIZATION ISSUES DETECTED:
   • auth_failed: Invalid credentials (EAP authentication failed)
   • radius_failure: RADIUS server timeout (No response from RADIUS server)
   • 802_1x_failure: Certificate validation failed (Client certificate expired)

📋 RECOMMENDATION:
   Due to detected authentication/authorization failures,
   troubleshoot on ISE (Identity Services Engine).
```

### Scenario 2: DHCP/DNS Issues Detected

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
✅ Client found: Sarah-Phone on AP 5c:5b:35:aa:bb:cc

[2/5] Analyzing client events and logs...

[3/5] Checking authentication and authorization...

[4/5] Checking DHCP and DNS...

🔴 DHCP/DNS ISSUES DETECTED:
   • dhcp_timeout: DHCP request timed out after 30 seconds
   • dns_failure: Unable to resolve domain names (DNS server unreachable)
   • ip_conflict: IP address conflict detected for 192.168.1.100

📋 RECOMMENDATION:
   Due to detected DNS/DHCP lease errors,
   check network infrastructure (LAN, WAN, DHCP, DNS).
```

### Scenario 3: Signal Issues with AP Reboot Recommendation

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
✅ Client found: Conference-Room-TV on AP 5c:5b:35:aa:bb:cc

[2/5] Analyzing client events and logs...

[3/5] Checking authentication and authorization...

[4/5] Checking DHCP and DNS...

[5/5] Analyzing client health metrics...

🟡 CLIENT HEALTH ISSUES DETECTED:
   • RSSI: Poor signal strength: -78 dBm (should be > -67 dBm) [HIGH]
   • SNR: Poor signal quality: 12 dB SNR (should be > 20 dB) [MEDIUM]
   • Retries: High retry rates detected (TX: 25%, RX: 18%) [MEDIUM]

   Checking AP 5c:5b:35:aa:bb:cc uptime...
   AP Uptime: 45.2 days (High uptime - consider scheduled reboot)

📋 RECOMMENDATION:
   Signal-related issues detected with AP uptime concerns.
   Consider rebooting AP 5c:5b:35:aa:bb:cc during maintenance window.
```

### Scenario 4: Client Health Issues (No Reboot Needed)

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
✅ Client found: Employee-Tablet on AP 5c:5b:35:aa:bb:cc

[2/5] Analyzing client events and logs...

[3/5] Checking authentication and authorization...

[4/5] Checking DHCP and DNS...

[5/5] Analyzing client health metrics...

🟡 CLIENT HEALTH ISSUES DETECTED:
   • Latency: High latency detected: 150 ms [MEDIUM]
   • Retries: High retry rates detected (TX: 22%, RX: 15%) [MEDIUM]

📋 RECOMMENDATION:
   Client health metric issues detected;
   refer to manual troubleshooting workflow for detailed analysis.
```

### Scenario 5: All Checks Pass

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
✅ Client found: Manager-Laptop on AP 5c:5b:35:aa:bb:cc

[2/5] Analyzing client events and logs...

[3/5] Checking authentication and authorization...

[4/5] Checking DHCP and DNS...

[5/5] Analyzing client health metrics...

✅ All automated checks completed successfully!

📋 RECOMMENDATION:
   All automated checks look good;
   proceed with manual troubleshooting steps as needed.

============================================================
CLIENT SUMMARY
============================================================
Hostname: Manager-Laptop
AP MAC: 5c:5b:35:aa:bb:cc
SSID: Corporate-WiFi
RSSI: -55 dBm
SNR: 35 dB
Band: 5G
Channel: 36
```

### Scenario 6: Client Not Found

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
❌ ERROR: Client aa:bb:cc:dd:ee:ff not found in Mist database
```

### Scenario 7: API Connection Issues

```plaintext
============================================================
MIST NETWORK TROUBLESHOOTING ANALYSIS
============================================================
Client IP: 192.168.1.100
Client MAC: aa:bb:cc:dd:ee:ff
Analysis Time: 2025-01-15 14:30:22
============================================================

[1/5] Gathering client information...
API request failed: 401 Client Error: Unauthorized for url: https://api.mist.com/api/v1/orgs/xxx/clients/search

❌ ERROR: Please check your API token and organization ID
```

## Output Features

- **Progress Indicators**: Shows [1/5], [2/5] etc. as it works through checks
- **Color-coded Results**: 
  - ✅ Success (green)
  - 🔴 Critical issues (red) 
  - 🟡 Warning issues (yellow)
  - ❌ Errors (red)
- **Clear Recommendations**: Based on flowchart logic
- **Detailed Issue Descriptions**: Shows specific problems found
- **Client Summary**: When all checks pass, shows full client details
- **Early Exit**: Stops at first major issue found (auth → DHCP → health)

## Requirements

- Python 3.6+
- Mist API token
- Organization ID
- Client IP address
- Client MAC address

## License

[Add your license information here]
