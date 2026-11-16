"""Run the hunt SQL against seeded data in DuckDB and assert the planted threats are found."""
import pathlib, duckdb, sys
sys.path.insert(0, "loader")
import load  # noqa: E402

def _con():
    con = duckdb.connect(":memory:")
    con.execute("""CREATE TABLE audit_log(ts TIMESTAMP, epoch_s BIGINT, actor TEXT, action TEXT,
        src_ip TEXT, lat DOUBLE, lng DOUBLE, resource TEXT, role_granted TEXT, grantee TEXT)""")
    con.executemany("INSERT INTO audit_log VALUES (" + ",".join("?"*10) + ")",
                    [[r[c] for c in load.COLS] for r in load.ROWS])
    return con

def test_impossible_travel_flags_alice():
    con = _con()
    sql = pathlib.Path("hunts/impossible_travel.sql").read_text()
    rows = con.execute(sql).fetchall()
    actors = {r[0] for r in rows}
    assert "alice@corp.com" in actors, "London->Sydney in 12 min must flag"
    assert all(r[0] != "bob@corp.com" for r in rows), "normal users must not flag"

def test_privilege_escalation_flags_self_grant():
    con = _con()
    sql = pathlib.Path("hunts/privilege_escalation.sql").read_text()
    rows = con.execute(sql).fetchall()
    actors = {r[0] for r in rows}
    assert actors == {"mallory@corp.com"}, "only the self-Owner-grant should flag, not the viewer grant"
