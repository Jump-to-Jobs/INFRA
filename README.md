Infrastructure for JJobs

## DNS (OctoDNS)

- `DNS/` contains the older ad-hoc helper scripts that talk directly to the
  Metaname API.  These scripts are deprecated now and will eventually be removed.
- `octodns/` is the new IaC workflow for the Metaname zones. It stores the
  zone definition in YAML and uses the `octodns-metaname` provider.

Quick start:

```
cd octodns
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
source env/metaname-test.env
make plan-test            # dry-run
make apply-test           # push changes to the Metaname test API
```

The zone file lives in `octodns/zones/getjjobs.nz.yaml`. Update it like you
would any other OctoDNS project, open a PR, and run the plan/apply commands
above to sync the changes.

CI/CD automation could be added if desired, so that when changes are approved
they will be automatically deployed on merge to main.
