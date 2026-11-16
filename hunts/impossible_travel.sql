-- Impossible travel: two logins by the same actor whose required speed exceeds 900 km/h.
-- Haversine over lat/lng; time from epoch_s (portable, no engine-specific functions).
WITH logins AS (
  SELECT actor, epoch_s, lat, lng,
         LAG(epoch_s) OVER w AS prev_s,
         LAG(lat)     OVER w AS prev_lat,
         LAG(lng)     OVER w AS prev_lng
  FROM audit_log
  WHERE action = 'google.login.LoginSuccess'
  WINDOW w AS (PARTITION BY actor ORDER BY epoch_s)
),
calc AS (
  SELECT actor, epoch_s, prev_s,
         6371 * ACOS(LEAST(1.0, GREATEST(-1.0,
           COS(RADIANS(prev_lat)) * COS(RADIANS(lat)) * COS(RADIANS(lng) - RADIANS(prev_lng))
           + SIN(RADIANS(prev_lat)) * SIN(RADIANS(lat))))) AS km,
         (epoch_s - prev_s) / 3600.0 AS hours
  FROM logins
  WHERE prev_s IS NOT NULL
)
SELECT actor, epoch_s, km, hours, km / NULLIF(hours, 0) AS kmh
FROM calc
WHERE hours >= 0 AND km / NULLIF(hours, 0) > 900;
