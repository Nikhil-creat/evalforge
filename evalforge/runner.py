import pandas as pd
from .config import PASS_THRESHOLD
from .llm import ask
import re

def _f1(a, b):
    A, B = set(re.findall(r"\w+", a.lower())), set(re.findall(r"\w+", b.lower()))
    if not A or not B: return 0.0
    p, r = len(A & B) / len(A), len(A & B) / len(B)
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)

def judge(prompt, out, ref):
    if ref:
        j = ask(f"Score 0-1 how well ANSWER matches REFERENCE in meaning. Number only.\nQ:{prompt}\nREFERENCE:{ref}\nANSWER:{out}")
        m = re.search(r"[01](?:\.\d+)?", j or "")
        return float(m.group()) if m else _f1(out, ref)
    return 0.0 if len(out) < 25 or "not sure" in out.lower() else 0.7

def run_evals(cases, run_id, target=None):
    """target: callable(prompt)->str for the candidate model. Offline mode replays logged responses."""
    rows = []
    for r in cases.itertuples():
        out = target(r.prompt) if target else (ask(r.prompt, "You are a helpful assistant.") or r.response)
        s = judge(r.prompt, out, r.reference)
        rows.append(dict(run_id=run_id, id=r.id, cluster=r.cluster, label=r.label, kind=r.kind, score=s, passed=s >= PASS_THRESHOLD))
    return pd.DataFrame(rows)
