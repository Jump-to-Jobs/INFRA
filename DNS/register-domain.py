#!/usr/bin/env python3
# This script registers the getjjobs.nz domain with Metaname.
# It uses the 1Password CLI to fetch credentials and contact details.
# Admin and registrant contacts are set to: ops.jjobs@gmail.com
# Technical contact is set to John's personal email.

# Standard library imports
import requests
import subprocess

# Function to fetch a field from a 1Password item
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

# Load credentials from 1Password vault
item_name = "Metaname API Key"
vault_name = "startmeup.nz"

# credentials for Metaname API
account_reference = fetch_op_field(item_name, "account_reference", vault_name)
api_key = fetch_op_field(item_name, "credential", vault_name)
contact_email = fetch_op_field(item_name, "username", vault_name)

# Domain to register
domain = "getjjobs.nz"
term = 12  # months (minimum is 12 months)

# Contact details for registration
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

# Construct base contact fields (excluding email)
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

# Registrant (owner) contact with override email
registrant_contact = base_contact_fields.copy()
registrant_contact["email_address"] = "ops.jjobs@gmail.com"

# Admin contact with override email
admin_contact = base_contact_fields.copy()
admin_contact["email_address"] = "ops.jjobs@gmail.com"

# Technical contact with default email from 1Password
technical_contact = base_contact_fields.copy()
technical_contact["email_address"] = contact_email

# Final contacts payload
contacts = {
    "registrant": registrant_contact,
    "admin": admin_contact,
    "technical": technical_contact
}

# Use Metaname's hosted DNS
name_servers = None

# JSON-RPC payload
payload = {
    "jsonrpc": "2.0",
    "method": "register_domain_name",
    "params": [account_reference, api_key, domain, term, contacts, name_servers],
    "id": 3
}

# Perform the request
try:
    response = requests.post(
        "https://metaname.net/api/1.1",
        json=payload
    )
except Exception as e:
    raise RuntimeError(f"Failed to reach Metaname API: {e}")

# Print result
print(f"Status: {response.status_code}")
try:
    print("Response:", response.json())
except Exception as e:
    print("Error parsing JSON response:", e)
    print("Raw response text:", response.text)
