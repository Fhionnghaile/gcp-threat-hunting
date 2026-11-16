-- BigQuery table schema for normalised cloud-audit logs.
CREATE TABLE IF NOT EXISTS audit_log (
  ts           TIMESTAMP,
  epoch_s      INT64,       -- unix seconds (portable time math; no engine-specific TIMESTAMP_DIFF)
  actor        STRING,
  action       STRING,
  src_ip       STRING,
  lat          FLOAT64,
  lng          FLOAT64,
  resource     STRING,
  role_granted STRING,
  grantee      STRING
);
