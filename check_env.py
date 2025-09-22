#!/usr/bin/env python
"""
Script to check env for running Mist API calls. Useful to run
before trying to execute any scripts
Checks:
 1. DNS lookup
 2. Network connectivity: can we get to api.mist.com?
 3. Have we got an API key configured?
 4. Can we do a basic API call?
"""
import requests
import os
import socket
import json
from pprint import pprint
from http.client import responses
from modules.core.banner import header, footer
from modules.core.get_vars import GetVars

# supply required token
vars_obj = GetVars()
vars_found = vars_obj.find_vars()
api_token = vars_found.get('token')

def check_env():
    total_tests = 4
    passed_count = 0
    
    header()
    print("Executing tests to check if our environment is \nsuitable to use Mist API:\n")
    
    print("1. Checking our DNS is good (looking up api.mist.com)...")
    try:
        socket.gethostbyname("api.mist.com")
        print("   Result: OK.\n")
        passed_count += 1
    except socket.gaierror as e:
        print(f"   Result: ** Fail ** (DNS lookup failed: {e})\n")
    except Exception as e:
        print(f"   Result: ** Fail ** (Unexpected error: {e})\n")

    base_url = "https://api.mist.com"
    print("2. Checking we can get to Mist API URL ({})...".format(base_url))
    session = requests.Session()
    try:
        session.get(base_url, timeout=1)
        print("   Result: OK.\n")
        passed_count += 1
    except requests.exceptions.RequestException as e:
        print(f"   Result: ** Fail ** (Network error: {e})\n")
    except Exception as e:
        print(f"   Result: ** Fail ** (Unexpected error: {e})\n")
  
    print("3. Checking we have an API key defined (via env var MIST_TOKEN)...")
    if api_token:
        print("   Result: OK.\n")
        passed_count += 1
    else:
        print("   Result: ** Fail **. (Please define the env var MIST_TOKEN)\n")
    
    print("4. Try a 'who am I' via the API...")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token {}'.format(api_token)
    }
    url = "https://api.mist.com/api/v1/self"
    try:
        response = session.get(url, headers=headers, timeout=2)
        if response.status_code == 200:
            print("   Result: OK. (result below)\n")
            data = json.loads(response.content.decode('utf-8'))
            print("      Name: {} {}".format(data['first_name'], data['last_name']))
            print("      Email: {}".format(data['email']))
            passed_count += 1
        else:
            status_code = response.status_code
            status_text = responses.get(status_code, 'Unknown')
            print("   Result: ** Fail. ** (response received, but expected data was not received (code: {}, text: {}))".format(status_code, status_text))
            print("   (Maybe check that API token is available via env var MIST_TOKEN and is valid)")
    except requests.exceptions.RequestException as e:
        print(f"   Result: ** Fail ** (Network error: {e})\n")
    except json.JSONDecodeError as e:
        print(f"   Result: ** Fail ** (Invalid JSON response: {e})\n")
    except Exception as e:
        print(f"   Result: ** Fail ** (Unexpected error: {e})\n")
    
    print("\n  -- Tests complete (passed {}/{}) --".format(passed_count, total_tests))
    footer()
    
def main():
    check_env()

if __name__ == "__main__":
    main()
