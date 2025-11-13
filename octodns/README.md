# OctoDNS workflow for `testjjobs.nz` / `getjjobs.nz`

The `octodns/` directory contains the infrastructure-as-code workflow for the
Metaname zones. It manages the test domain (`testjjobs.nz`) today and includes
the production config (`getjjobs.nz`) so we can wire that up next.

## Setup

Environment variables live in `env/`. Source whichever file matches the target
zone so the resolver and credentials are exported:

```
cd private/jjobs/INFRA/octodns
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
source env/metaname-test.env   # or env/metaname-prod.env
```

The env files use `op://` references for `METANAME_ACCOUNT_REF(_REF)` and
`METANAME_API_TOKEN(_REF)` plus
`OCTODNS_METANAME_SECRET_RESOLVER="op_opsdevnz.octodns_hooks:resolve"`, so no
secrets are written to disk.

## Running plans / applies

```
# Test domain
octodns-validate --config-file configs/metaname.test.yaml
octodns-sync --config-file configs/metaname.test.yaml
octodns-sync --config-file configs/metaname.test.yaml --doit

# Production domain
octodns-validate --config-file configs/metaname.prod.yaml
octodns-sync --config-file configs/metaname.prod.yaml
octodns-sync --config-file configs/metaname.prod.yaml --doit
```
