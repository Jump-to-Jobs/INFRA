#!/usr/bin/env python3
"""
Create a CNAME record for dev subdomain using Metaname's create_dns_record method.
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
subdomain = "app"
cname_value = "cd00d1410879ea24.vercel-dns-017.com."

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

# --- Compose the DNS record ---
record = {
    "name": subdomain,
    "type": "CNAME",
    "ttl": 3600,
    "aux": None,
    "data": cname_value
}

# --- Make the request ---
print(f"Creating CNAME {subdomain}.{domain} → {cname_value}")
response = requests.post(API_ENDPOINT, json={
    "jsonrpc": "2.0",
    "method": "create_dns_record",
    "params": [account_reference, api_key, domain, record],
    "id": 1
})

# --- Handle response ---
print("Status:", response.status_code)
try:
    result = response.json()
    print("Response:", json.dumps(result, indent=2))
except Exception as e:
    print("Failed to decode JSON response:", e)
    print("Raw Response:", response.text)
