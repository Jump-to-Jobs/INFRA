# DNS Helper Scripts (Legacy / Deprecated)

This folder contains older one-off helper scripts for working directly with the
Metaname DNS API (credentials typically fetched via the 1Password CLI), plus a
few scripts that were used during the earlier Netlify setup.

These scripts are **not used anymore** for routine DNS changes. DNS is managed
via OctoDNS in `../octodns/`, which is the current source of truth.

## Why keep these around?

They’re still useful as “living documentation” for how the domain and records
were set up before we moved to DNS-as-code, for example:

- Domain registration and initial setup in Metaname (`register-domain.py`)
- Inspecting the live Metaname zone (`metaname-show-dns-zone.py`)
- ForwardEmail-related MX/TXT bootstrap (`metaname-setup-forwardemail-mx.py`)
- Legacy Netlify record setup (the various `add-*-netlify-*.py` scripts)

## Making DNS changes today

If you need to change DNS now, make the change in `../octodns/` (update the zone
YAML and run the plan/apply workflow there). Do not run scripts in this folder
unless you have a specific, reviewed reason.

## Notes / Warnings

- **Netlify is legacy for this project**; the Netlify-related scripts are kept
  for historical reference.
- Some scripts may default to the **production** Metaname API and can change
  live DNS if executed.
