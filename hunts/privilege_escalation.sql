-- Self-granted privilege escalation: an actor grants Owner/Editor to themselves.
SELECT actor, epoch_s, resource, role_granted, grantee
FROM audit_log
WHERE action = 'SetIamPolicy'
  AND role_granted IN ('roles/owner', 'roles/editor')
  AND grantee = actor;
