"""CI regression gate: exit 1 if representative-case pass rate < 80%."""
import sys
from evalforge import db
from evalforge.pipeline import run_pipeline

rid = run_pipeline()
r = db.read("results"); r = r[(r.run_id == rid) & (r.kind == "representative")]
rate = r.passed.mean(); print(f"representative pass rate: {rate:.0%}")
sys.exit(0 if rate >= 0.8 else 1)
