# Looker Studio dashboard

Point Looker Studio at the BigQuery dataset and build three tiles from the hunt views:
- **Impossible travel** (actor, km/h) from `hunts/impossible_travel.sql`
- **Privilege escalation** (actor, role, resource) from `hunts/privilege_escalation.sql`
- **Logins by geography** (map) from `audit_log`

Schedule the hunts as BigQuery **scheduled queries** writing to `detections_*` tables; Looker reads those.
A public sample link goes here once published.
