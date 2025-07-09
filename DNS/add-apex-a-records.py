#!/usr/bin/env python3
"""
Create A records for the apex domain using Metaname's create_dns_record method.
Supports both test and production environments.
"""

import requests
import subprocess
import json

# --- Toggle for test or production ---
use_test_api = False  # Set to False to use the production API

API_ENDPOINT = (
    "https://test.metaname.net/api/1.1"
    if use_test_api else
    "https://metaname.net/api/1.1"
)
vault_name = "JJobs"
item_name = "Metaname Test API Key" if use_test_api else "Metaname Prod API Key"
domain = "testjjobs.nz" if use_test_api else "getjjobs.nz"

# --- A records required for Netlify apex domain support ---
apex_ips = ["75.2.60.5", "99.83.190.102"]

# --- Fetch credentials from 1Password ---
def fetch_op_field(item, field, vault):
    return subprocess.check_output([
        "op", "item", "get", item,
        "--vault", vault,
        "--field", field,
        "--reveal"
    ]).decode().strip()

account_reference = fetch_op_field(item_name, "account_reference", vault_name)
api_key = fetch_op_field(item_name, "credential", vault_name)

# --- Loop over IPs and create A records ---
for ip in apex_ips:
    record = {
        "name": "@",
        "type": "A",
        "ttl": 3600,
        "aux": None,
        "data": ip
    }

    print(f"Creating A record {domain} → {ip}")
    response = requests.post(API_ENDPOINT, json={
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, record],
        "id": 1
    })

    print("Status:", response.status_code)
    try:
        result = response.json()
        print("Response:", json.dumps(result, indent=2))
    except Exception as e:
        print("Failed to decode JSON response:", e)
        print("Raw Response:", response.text)
