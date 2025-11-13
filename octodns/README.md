# OctoDNS workflow for `getjjobs.nz`

The `octodns/` directory contains the infrastructure-as-code workflow for the
Metaname zones. It manages the test domain (`testjjobs.nz`) and the production
domain (`getjjobs.nz`).

## Setup

Environment variables live in `env/metaname-test.env`. Source that file so the
resolver and Metaname credentials are exported:

```bash
cd private/jjobs/INFRA/octodns
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
source env/metaname-test.env
```

The env file uses `op://` references and exports everything (including
`OCTODNS_METANAME_SECRET_RESOLVER="op_opsdevnz.octodns_hooks:resolve"`) so
OctoDNS reads the same secrets the ad-hoc scripts used.

## Running plans / applies

```bash
# Dry-run the test zone
octodns-validate --config-file configs/metaname.test.yaml
octodns-sync --config-file configs/metaname.test.yaml

# Apply changes to the Metaname test API
octodns-sync --config-file configs/metaname.test.yaml --doit
```

Once we add `configs/metaname.prod.yaml` (plus a matching env file) the same
commands will manage `getjjobs.nz`.
