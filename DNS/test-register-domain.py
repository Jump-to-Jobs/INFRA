#!/usr/bin/env python3
# This script registers the getjjobs.nz domain with Metaname.
# It uses the 1Password CLI to fetch credentials and contact details.
# Admin and registrant contacts are set to: ops.jjobs@gmail.com
# Technical contact is set to John's personal email.
# Supports toggling between production and test environments.

import requests
import subprocess

# --- Environment toggle ---
use_test_api = True # Set to False to use the prod API
API_ENDPOINT = (
    "https://test.metaname.net/api/1.1"
    if use_test_api
    else "https://metaname.net/api/1.1"
)
vault_name = "JJobs"
item_name = "Metaname Test API Key" if use_test_api else "Metaname Prod API Key"
domain = "testjjobs.nz" if use_test_api else "getjjobs.nz"
term = 12  # registration term in months

# --- Fetch field from 1Password ---
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

# --- Load credentials ---
account_reference = fetch_op_field(item_name, "account_reference", vault_name)
api_key = fetch_op_field(item_name, "credential", vault_name)
contact_email = fetch_op_field(item_name, "username", vault_name)

# --- Contact details ---
contact_name = fetch_op_field(item_name, "contact_name", vault_name)
contact_org = fetch_op_field(item_name, "contact_org", vault_name)
address_line1 = fetch_op_field(item_name, "address_line1", vault_name)
address_line2 = fetch_op_field(item_name, "address_line2", vault_name)
address_city = fetch_op_field(item_name, "address_city", vault_name)
address_region = fetch_op_field(item_name, "address_region", vault_name)
address_postcode = fetch_op_field(item_name, "address_postcode", vault_name)
address_country = fetch_op_field(item_name, "address_country", vault_name)
phone_cc = fetch_op_field(item_name, "phone_cc", vault_name)
phone_area = fetch_op_field(item_name, "phone_area", vault_name)
phone_local = fetch_op_field(item_name, "phone_local", vault_name)

base_contact_fields = {
    "name": contact_name,
    "organisation_name": contact_org,
    "postal_address": {
        "line1": address_line1,
        "line2": address_line2,
        "city": address_city,
        "region": address_region,
        "postal_code": address_postcode,
        "country_code": address_country
    },
    "phone_number": {
        "country_code": phone_cc,
        "area_code": phone_area,
        "local_number": phone_local
    },
    "fax_number": None
}

# --- Contact Roles ---
registrant_contact = base_contact_fields.copy()
registrant_contact["email_address"] = "ops.jjobs@gmail.com"

admin_contact = base_contact_fields.copy()
admin_contact["email_address"] = "ops.jjobs@gmail.com"

technical_contact = base_contact_fields.copy()
technical_contact["email_address"] = "john@startmeup.nz"

contacts = {
    "registrant": registrant_contact,
    "admin": admin_contact,
    "technical": technical_contact
}

# --- Registration payload ---
name_servers = None  # Use Metaname DNS
payload = {
    "jsonrpc": "2.0",
    "method": "register_domain_name",
    "params": [account_reference, api_key, domain, term, contacts, name_servers],
    "id": 3
}

# --- Perform the registration request ---
try:
    response = requests.post(API_ENDPOINT, json=payload)
    print(f"Status: {response.status_code}")
    print("Response:", response.json())
except Exception as e:
    raise RuntimeError(f"Failed to reach Metaname API: {e}")
