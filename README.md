# GCP Threat-Hunting pipeline

<!-- at-a-glance -->
> **Threat-hunting over GCP logs: detections as queries you can run, test and version.**  
> **Result:** 2 tests; detections as reviewable, version-controlled queries.  
> **Reproduce:** `pytest -q`  
> ![CI](https://github.com/fhionnghaile/gcp-threat-hunting/actions/workflows/ci.yml/badge.svg)
>
> **What this is worth:** Turns 'we should look for X' into a repeatable, tested detection instead of a one-off console search.


Stream cloud-audit logs into **BigQuery**, hunt with **SQL**, dashboard in **Looker Studio**.

## Hunts
- **`impossible_travel.sql`** — same actor, two logins whose required speed > 900 km/h (haversine over lat/lng, time from `epoch_s`).
- **`privilege_escalation.sql`** — an actor granting themselves `roles/owner` / `roles/editor`.

Both are written in **portable Standard SQL** (no engine-specific time/geo functions), so they run on
**BigQuery** in production *and* on **DuckDB** in CI — which is how they're tested.

## Test the hunts (no GCP needed)
```bash
pip install duckdb && pytest -q      # loads seeded logs into DuckDB, runs each hunt, asserts the planted threats
```
The seed data (`data/synthetic_audit.jsonl`) contains a London→Sydney-in-12-minutes login and a
self-granted Owner — plus benign activity the hunts must **not** flag.

## Deploy
```bash
python loader/load.py --bq <project>.<dataset>   # load into BigQuery
# register the hunts as scheduled queries; point Looker Studio at the results (see looker/).
```

## License
MIT.

## Key decisions

- Detections-as-code, so a hunt is reviewable and re-runnable, not tribal knowledge.
- Mapped to recognisable attacker behaviours rather than raw log noise.

## Scope & limits

- A starter set of hunts; coverage grows with the environment's threat model.

