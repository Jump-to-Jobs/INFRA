Infrastructure for JJobs

## DNS (OctoDNS)

- `DNS/` contains the older ad-hoc helper scripts that talk directly to the
  Metaname API.
- `octodns/` is the new IaC workflow for the Metaname zones. It stores the
  zone definition in YAML and uses the `octodns-metaname` provider.

Quick start:

```
cd octodns
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OCTODNS_METANAME_SECRET_RESOLVER="op_opsdevnz.octodns_hooks:resolve"
cp env/metaname-test.env.example env/metaname-test.env
set -a && source env/metaname-test.env && set +a
make plan-test            # dry-run
make apply-test           # push changes to the Metaname test API
```

The zone file lives in `octodns/zones/testjjobs.nz.yaml`. Update it like you
would any other OctoDNS project, open a PR, and run the plan/apply commands
above to sync the changes.
