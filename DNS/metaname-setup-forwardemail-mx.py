#!/usr/bin/env python3

import requests
import subprocess

# --- Environment toggle ---
use_test_api = False  # Set to False to use production Metaname API

# --- Metaname API endpoints ---
API_ENDPOINT = (
    "https://test.metaname.net/api/1.1"
    if use_test_api
    else "https://metaname.net/api/1.1"
)

# --- Domain Profile: GETJJOBS.NZ ---

vault_name = "JJobs"
item_name = "Metaname Test API Key" if use_test_api else "Metaname Prod API Key"
domain = "testjjobs.nz" if use_test_api else "getjjobs.nz"

verification_txt_value = "forward-email-site-verification=Zh8I4ySdmv"
dmarc_rua_address = "mailto:dmarc-6832438f6dff8fa7b72b9251@forwardemail.net"


# --- Reusable 1Password field fetcher ---
def fetch_op_field(item: str, field: str, vault: str) -> str:
    try:
        return (
            subprocess.check_output(
                [
                    "op",
                    "item",
                    "get",
                    item,
                    "--vault",
                    vault,
                    "--field",
                    field,
                    "--reveal",
                ]
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to fetch '{field}' from 1Password item '{item}': {e}"
        )


# --- Fetch credentials from 1Password ---
account_reference = (
    fetch_op_field(item_name, "username", vault_name)
    if use_test_api
    else fetch_op_field(item_name, "account_reference", vault_name)
)
api_key = fetch_op_field(item_name, "credential", vault_name)

# --- Define MX records for Forward Email ---
mx_records = [
    {
        "name": "@",
        "type": "MX",
        "data": "mx1.forwardemail.net.",
        "ttl": 3600,
        "aux": 10,
    },
    {
        "name": "@",
        "type": "MX",
        "data": "mx2.forwardemail.net.",
        "ttl": 3600,
        "aux": 10,
    },
]

# --- Fetch current DNS zone ---
zone_payload = {
    "jsonrpc": "2.0",
    "method": "dns_zone",
    "params": [account_reference, api_key, domain],
    "id": 1,
}

try:
    response = requests.post(API_ENDPOINT, json=zone_payload)
    zone_records = response.json().get("result", [])
except Exception as e:
    raise RuntimeError(f"Failed to fetch DNS zone: {e}")

# --- Create MX records ---
for i, record in enumerate(mx_records, start=1):
    exists = any(
        r["type"] == "MX"
        and r["name"] == record["name"]
        and r["data"].rstrip(".").lower() == record["data"].rstrip(".").lower()
        and r.get("aux") == record["aux"]
        for r in zone_records
    )

    if exists:
        print(
            f"[MX {i}] ✅ Already exists: {record['data']} (priority {record['aux']})"
        )
        continue

    payload = {
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, record],
        "id": i,
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        print(f"[MX {i}] 🚀 Created: {record['data']} (priority {record['aux']})")
        print(f"[MX {i}] Response:", res.json())
    except Exception as e:
        raise RuntimeError(f"[MX {i}] ❌ Failed to create record: {e}")

# --- Forward Email TXT Verification Record ---
verification_txt = {
    "name": "@",
    "type": "TXT",
    "data": verification_txt_value,
    "ttl": 3600,
}

txt_exists = any(
    r["type"] == "TXT"
    and r["name"] == verification_txt["name"]
    and r["data"] == verification_txt["data"]
    for r in zone_records
)

if txt_exists:
    print("✅ Forward Email TXT verification record already exists.")
else:
    print("🔧 Creating Forward Email TXT verification record...")
    payload = {
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, verification_txt],
        "id": 99,
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        print("🚀 TXT record created.")
        print("TXT Response:", res.json())
    except Exception as e:
        raise RuntimeError(f"❌ Failed to create TXT verification record: {e}")

# --- SPF TXT Record ---
spf_txt = {
    "name": "@",
    "type": "TXT",
    "data": "v=spf1 a include:spf.forwardemail.net include:_spf.google.com -all",
    "ttl": 3600,
}

spf_exists = any(
    r["type"] == "TXT" and r["name"] == spf_txt["name"] and r["data"] == spf_txt["data"]
    for r in zone_records
)

if spf_exists:
    print("✅ SPF TXT record already exists.")
else:
    print("🔧 Creating SPF TXT record...")
    payload = {
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, spf_txt],
        "id": 100,
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        print("🚀 SPF TXT record created.")
        print("SPF Response:", res.json())
    except Exception as e:
        raise RuntimeError(f"❌ Failed to create SPF TXT record: {e}")

# --- DKIM TXT Record ---
dkim_txt = {
    "name": "fe-e1a7480ff1._domainkey",
    "type": "TXT",
    "data": (
        "v=DKIM1; k=rsa; "
        "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCpE8sJ9NqDxdZWoZMAyzNzBNvgFgrwQm+EBN/fKw6Pk5TUEhcirkK7VOtjkLcuKB2eawO8wCDFBsRvV/o4/e31r0zVKLlEUFizTsQrZy8F8fbsrM1Si0xnfVSbtnbUqH/bnZBcz5UxVFxQGn63a858bnH5LLfb+ZUpCxunFdnSQQIDAQAB;"
    ),
    "ttl": 3600,
}

dkim_exists = any(
    r["type"] == "TXT"
    and r["name"] == dkim_txt["name"]
    and r["data"] == dkim_txt["data"]
    for r in zone_records
)

if dkim_exists:
    print("✅ DKIM TXT record already exists.")
else:
    print("🔧 Creating DKIM TXT record...")
    payload = {
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, dkim_txt],
        "id": 101,
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        print("🚀 DKIM TXT record created.")
        print("DKIM Response:", res.json())
    except Exception as e:
        raise RuntimeError(f"❌ Failed to create DKIM TXT record: {e}")

# --- Return-Path CNAME Record ---
cname_record = {
    "name": "fe-bounces",
    "type": "CNAME",
    "data": "forwardemail.net.",
    "ttl": 3600,
}

cname_exists = any(
    r["type"] == "CNAME"
    and r["name"] == cname_record["name"]
    and r["data"] == cname_record["data"]
    for r in zone_records
)

if cname_exists:
    print("✅ Return-Path CNAME record already exists.")
else:
    print("🔧 Creating Return-Path CNAME record...")
    payload = {
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, cname_record],
        "id": 102,
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        print("🚀 Return-Path CNAME record created.")
        print("CNAME Response:", res.json())
    except Exception as e:
        raise RuntimeError(f"❌ Failed to create Return-Path CNAME record: {e}")

# --- DMARC TXT Record ---
dmarc_txt = {
    "name": "_dmarc",
    "type": "TXT",
    "data": f"v=DMARC1; p=reject; pct=100; rua={dmarc_rua_address};",
    "ttl": 3600,
}

dmarc_exists = any(
    r["type"] == "TXT"
    and r["name"] == dmarc_txt["name"]
    and r["data"] == dmarc_txt["data"]
    for r in zone_records
)

if dmarc_exists:
    print("✅ DMARC TXT record already exists.")
else:
    print("🔧 Creating DMARC TXT record...")
    payload = {
        "jsonrpc": "2.0",
        "method": "create_dns_record",
        "params": [account_reference, api_key, domain, dmarc_txt],
        "id": 103,
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        print("🚀 DMARC TXT record created.")
        print("DMARC Response:", res.json())
    except Exception as e:
        raise RuntimeError(f"❌ Failed to create DMARC TXT record: {e}")
