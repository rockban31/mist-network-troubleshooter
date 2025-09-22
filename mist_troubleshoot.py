#!/usr/bin/env python3
"""
Mist Network Troubleshooting Automation Script
Analyzes client connectivity issues using Mist API
"""

import requests
import json
import sys
import argparse
from datetime import datetime, timedelta
import time

class MistTroubleshooter:
    def __init__(self, api_token, org_id):
        self.api_token = api_token
        self.org_id = org_id
        self.base_url = "https://api.mist.com/api/v1"
        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }
    
    def make_api_request(self, endpoint, params=None):
        """Make API request to Mist with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def get_client_info(self, mac_address):
        """Get client information and current session"""
        endpoint = f"/orgs/{self.org_id}/clients/search"
        params = {
            "mac": mac_address,
            "limit": 1
        }
        
        result = self.make_api_request(endpoint, params)
        if result and result.get('results'):
            return result['results'][0]
        return None
    
    def get_client_events(self, mac_address, hours_back=24):
        """Get client events and logs for analysis"""
        end_time = int(time.time())
        start_time = end_time - (hours_back * 3600)
        
        endpoint = f"/orgs/{self.org_id}/clients/{mac_address}/events"
        params = {
            "start": start_time,
            "end": end_time,
            "limit": 100
        }
        
        return self.make_api_request(endpoint, params)
    
    def get_ap_info(self, ap_mac):
        """Get Access Point information"""
        endpoint = f"/orgs/{self.org_id}/devices/{ap_mac}"
        return self.make_api_request(endpoint)
    
    def get_ap_stats(self, ap_mac):
        """Get AP statistics and uptime"""
        endpoint = f"/orgs/{self.org_id}/devices/{ap_mac}/stats"
        return self.make_api_request(endpoint)
    
    def analyze_auth_issues(self, events):
        """Check for authentication and authorization failures"""
        auth_failures = []
        
        if not events:
            return auth_failures
        
        for event in events:
            event_type = event.get('type', '').lower()
            
            # Check for various authentication failure types
            if any(failure_type in event_type for failure_type in [
                'auth_failed', 'assoc_failed', 'eap_failure', 
                'radius_failure', '802_1x_failure', 'psk_failure'
            ]):
                auth_failures.append({
                    'timestamp': event.get('timestamp'),
                    'type': event.get('type'),
                    'reason': event.get('reason', 'Unknown'),
                    'details': event.get('text', '')
                })
        
        return auth_failures
    
    def analyze_dhcp_dns_issues(self, events):
        """Check for DHCP and DNS related issues"""
        network_issues = []
        
        if not events:
            return network_issues
        
        for event in events:
            event_type = event.get('type', '').lower()
            event_text = event.get('text', '').lower()
            
            # Check for DHCP issues
            if any(issue in event_type or issue in event_text for issue in [
                'dhcp_failure', 'dhcp_timeout', 'no_dhcp_response',
                'dns_failure', 'dns_timeout', 'ip_conflict'
            ]):
                network_issues.append({
                    'timestamp': event.get('timestamp'),
                    'type': event.get('type'),
                    'issue_type': 'DHCP/DNS',
                    'details': event.get('text', '')
                })
        
        return network_issues
    
    def analyze_client_health(self, client_info):
        """Analyze client health metrics"""
        health_issues = []
        
        if not client_info:
            return health_issues
        
        # Check RSSI (Signal Strength) - typically good above -67 dBm
        rssi = client_info.get('rssi')
        if rssi and rssi < -70:
            health_issues.append({
                'metric': 'RSSI',
                'value': rssi,
                'issue': f'Poor signal strength: {rssi} dBm (should be > -67 dBm)',
                'severity': 'HIGH' if rssi < -80 else 'MEDIUM'
            })
        
        # Check SNR (Signal-to-Noise Ratio) - typically good above 20 dB
        snr = client_info.get('snr')
        if snr and snr < 15:
            health_issues.append({
                'metric': 'SNR',
                'value': snr,
                'issue': f'Poor signal quality: {snr} dB SNR (should be > 20 dB)',
                'severity': 'HIGH' if snr < 10 else 'MEDIUM'
            })
        
        # Check retry rates
        tx_retries = client_info.get('tx_retries', 0)
        rx_retries = client_info.get('rx_retries', 0)
        
        if tx_retries > 20 or rx_retries > 20:
            health_issues.append({
                'metric': 'Retries',
                'value': f'TX: {tx_retries}%, RX: {rx_retries}%',
                'issue': f'High retry rates detected (TX: {tx_retries}%, RX: {rx_retries}%)',
                'severity': 'MEDIUM'
            })
        
        # Check latency if available
        latency = client_info.get('latency_ms')
        if latency and latency > 100:
            health_issues.append({
                'metric': 'Latency',
                'value': f'{latency} ms',
                'issue': f'High latency detected: {latency} ms',
                'severity': 'MEDIUM' if latency < 200 else 'HIGH'
            })
        
        return health_issues
    
    def check_ap_uptime(self, ap_mac):
        """Check AP uptime and suggest reboot if needed"""
        ap_stats = self.get_ap_stats(ap_mac)
        
        if not ap_stats:
            return None
        
        uptime = ap_stats.get('uptime', 0)
        uptime_hours = uptime / 3600
        
        # Suggest reboot if uptime is very high (>30 days) or very low (<1 hour, indicating recent issues)
        needs_reboot = uptime_hours > (30 * 24) or uptime_hours < 1
        
        return {
            'uptime_hours': uptime_hours,
            'uptime_days': uptime_hours / 24,
            'needs_reboot': needs_reboot,
            'reason': 'High uptime - consider scheduled reboot' if uptime_hours > (30 * 24) 
                     else 'Recent restart detected - may indicate stability issues' if uptime_hours < 1 
                     else 'Uptime normal'
        }
    
    def troubleshoot_client(self, client_ip, client_mac):
        """Main troubleshooting function"""
        print(f"\n{'='*60}")
        print(f"MIST NETWORK TROUBLESHOOTING ANALYSIS")
        print(f"{'='*60}")
        print(f"Client IP: {client_ip}")
        print(f"Client MAC: {client_mac}")
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Get client information
        print("\n[1/5] Gathering client information...")
        client_info = self.get_client_info(client_mac)
        
        if not client_info:
            print(f"❌ ERROR: Client {client_mac} not found in Mist database")
            return
        
        print(f"✅ Client found: {client_info.get('hostname', 'Unknown')} on AP {client_info.get('ap_mac', 'Unknown')}")
        
        # Get client events
        print("\n[2/5] Analyzing client events and logs...")
        events = self.get_client_events(client_mac)
        
        # Check for authentication issues
        print("\n[3/5] Checking authentication and authorization...")
        auth_issues = self.analyze_auth_issues(events.get('results', []) if events else [])
        
        if auth_issues:
            print(f"\n🔴 AUTHENTICATION/AUTHORIZATION ISSUES DETECTED:")
            for issue in auth_issues[-3:]:  # Show last 3 issues
                print(f"   • {issue['type']}: {issue['reason']} ({issue.get('details', '')})")
            
            print(f"\n📋 RECOMMENDATION:")
            print(f"   Due to detected authentication/authorization failures,")
            print(f"   troubleshoot on ISE (Identity Services Engine).")
            return
        
        # Check for DHCP/DNS issues
        print("\n[4/5] Checking DHCP and DNS...")
        network_issues = self.analyze_dhcp_dns_issues(events.get('results', []) if events else [])
        
        if network_issues:
            print(f"\n🔴 DHCP/DNS ISSUES DETECTED:")
            for issue in network_issues[-3:]:  # Show last 3 issues
                print(f"   • {issue['type']}: {issue.get('details', '')}")
            
            print(f"\n📋 RECOMMENDATION:")
            print(f"   Due to detected DNS/DHCP lease errors,")
            print(f"   check network infrastructure (LAN, WAN, DHCP, DNS).")
            return
        
        # Check client health metrics
        print("\n[5/5] Analyzing client health metrics...")
        health_issues = self.analyze_client_health(client_info)
        
        if health_issues:
            print(f"\n🟡 CLIENT HEALTH ISSUES DETECTED:")
            
            signal_issues = False
            for issue in health_issues:
                print(f"   • {issue['metric']}: {issue['issue']} [{issue['severity']}]")
                if issue['metric'] in ['RSSI', 'SNR']:
                    signal_issues = True
            
            if signal_issues:
                # Check AP uptime for signal-related issues
                ap_mac = client_info.get('ap_mac')
                if ap_mac:
                    print(f"\n   Checking AP {ap_mac} uptime...")
                    ap_uptime = self.check_ap_uptime(ap_mac)
                    
                    if ap_uptime:
                        print(f"   AP Uptime: {ap_uptime['uptime_days']:.1f} days ({ap_uptime['reason']})")
                        
                        if ap_uptime['needs_reboot']:
                            print(f"\n📋 RECOMMENDATION:")
                            print(f"   Signal-related issues detected with AP uptime concerns.")
                            print(f"   Consider rebooting AP {ap_mac} during maintenance window.")
                            return
            
            print(f"\n📋 RECOMMENDATION:")
            print(f"   Client health metric issues detected;")
            print(f"   refer to manual troubleshooting workflow for detailed analysis.")
            return
        
        # If all checks pass
        print(f"\n✅ All automated checks completed successfully!")
        print(f"\n📋 RECOMMENDATION:")
        print(f"   All automated checks look good;")
        print(f"   proceed with manual troubleshooting steps as needed.")
        
        # Display summary
        print(f"\n{'='*60}")
        print(f"CLIENT SUMMARY")
        print(f"{'='*60}")
        print(f"Hostname: {client_info.get('hostname', 'Unknown')}")
        print(f"AP MAC: {client_info.get('ap_mac', 'Unknown')}")
        print(f"SSID: {client_info.get('ssid', 'Unknown')}")
        print(f"RSSI: {client_info.get('rssi', 'Unknown')} dBm")
        print(f"SNR: {client_info.get('snr', 'Unknown')} dB")
        print(f"Band: {client_info.get('band', 'Unknown')}")
        print(f"Channel: {client_info.get('channel', 'Unknown')}")

    def list_organizations(self):
        """List all organizations for this API token"""
        endpoint = "/orgs"
        return self.make_api_request(endpoint)
    
    def auto_select_org(self):
        """Automatically select organization if only one exists"""
        orgs = self.list_organizations()
        if not orgs:
            print("❌ No organizations found for this API token")
            return None
        
        if len(orgs) == 1:
            print(f"✅ Auto-selected organization: {orgs[0]['name']} ({orgs[0]['id']})")
            return orgs[0]['id']
        
        print(f"\n📋 Multiple organizations found:")
        for i, org in enumerate(orgs, 1):
            print(f"   {i}. {org['name']} ({org['id']})")
        
        while True:
            try:
                choice = input(f"\nSelect organization (1-{len(orgs)}): ")
                idx = int(choice) - 1
                if 0 <= idx < len(orgs):
                    selected_org = orgs[idx]
                    print(f"✅ Selected: {selected_org['name']} ({selected_org['id']})")
                    return selected_org['id']
                else:
                    print(f"❌ Please enter a number between 1 and {len(orgs)}")
            except ValueError:
                print("❌ Please enter a valid number")

def main():
    parser = argparse.ArgumentParser(description='Mist Network Troubleshooting Script')
    parser.add_argument('--token', required=True, help='Mist API Token')
    parser.add_argument('--org-id', help='Mist Organization ID (optional - will auto-detect if not provided)')
    parser.add_argument('--client-ip', required=True, help='Client IP Address')
    parser.add_argument('--client-mac', required=True, help='Client MAC Address')
    parser.add_argument('--list-orgs', action='store_true', help='List available organizations and exit')
    
    args = parser.parse_args()
    
    # If just listing orgs
    if args.list_orgs:
        temp_troubleshooter = MistTroubleshooter(args.token, "temp")
        orgs = temp_troubleshooter.list_organizations()
        if orgs:
            print("\n📋 Available Organizations:")
            for org in orgs:
                print(f"   Name: {org['name']}")
                print(f"   ID: {org['id']}")
                print(f"   Sites: {org.get('num_sites', 'Unknown')}")
                print("-" * 50)
        return
    
    # Determine org_id
    org_id = args.org_id
    if not org_id:
        temp_troubleshooter = MistTroubleshooter(args.token, "temp")
        org_id = temp_troubleshooter.auto_select_org()
        if not org_id:
            return
    
    # Initialize troubleshooter with determined org_id
    troubleshooter = MistTroubleshooter(args.token, org_id)
    
    # Run analysis
    troubleshooter.troubleshoot_client(args.client_ip, args.client_mac)

if __name__ == "__main__":
    main()