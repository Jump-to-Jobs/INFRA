#!/usr/bin/env python3

import requests
import subprocess
import json

# --- Environment toggle ---
use_test_api = False  # Set to True to use test environment
API_ENDPOINT = (
    "https://test.metaname.net/api/1.1"
    if use_test_api
    else "https://metaname.net/api/1.1"
)

# --- Setup ---
vault_name = "JJobs"
item_name = "Metaname Test API Key" if use_test_api else "Metaname Prod API Key"
domain = "testjjobs.nz" if use_test_api else "getjjobs.nz"

# --- Reusable 1Password field fetcher ---
def fetch_op_field(item: str, field: str, vault: str) -> str:
    try:
        return subprocess.check_output([
            "op", "item", "get", item,
            "--vault", vault,
            "--field", field,
            "--reveal"
        ]).decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to fetch '{field}' from 1Password item '{item}': {e}")

# --- Fetch credentials from 1Password ---
if use_test_api:
    account_reference = fetch_op_field(item_name, "username", vault_name)
else:
    account_reference = fetch_op_field(item_name, "account_reference", vault_name)

api_key = fetch_op_field(item_name, "credential", vault_name)

# --- Query DNS zone ---
payload = {
    "jsonrpc": "2.0",
    "method": "dns_zone",
    "params": [account_reference, api_key, domain],
    "id": 10
}

try:
    response = requests.post(API_ENDPOINT, json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()

    print("Zone records:")
    if "result" in result:
        for record in result["result"]:
            print(json.dumps(record, indent=2))
    else:
        print("No records found or error:")
        print(json.dumps(result, indent=2))

except Exception as e:
    raise RuntimeError(f"Failed to query DNS zone: {e}")
