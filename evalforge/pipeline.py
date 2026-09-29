import json, uuid
import numpy as np, pandas as pd
from datetime import datetime
from . import db
from .cluster import cluster
from .dataset import build_cases
from .llm import label_cluster, score_quality
from .pii import scrub
from .runner import run_evals
from .synth import generate

def jsd(p, q):
    ks = sorted(set(p) | set(q))
    P, Q = np.array([p.get(k, 0) for k in ks]), np.array([q.get(k, 0) for k in ks]); M = (P + Q) / 2
    kl = lambda a, b: float(np.sum(np.where(a > 0, a * np.log2(a / np.where(b > 0, b, 1)), 0)))
    return .5 * kl(P, M) + .5 * kl(Q, M)

def run_pipeline(target=None):
    logs = db.read("logs")
    if logs.empty:
        db.write(generate(), "logs"); logs = db.read("logs")
    logs["prompt"], logs["response"] = logs.prompt.map(scrub), logs.response.map(scrub)   # privacy first
    logs["cluster"], xy, logs["dist"] = cluster(logs.prompt.tolist())
    logs["x"], logs["y"] = xy[:, 0], xy[:, 1]
    names = {c: label_cluster(logs[logs.cluster == c].prompt.tolist()) for c in set(logs.cluster) if c != -1}
    names[-1] = "long-tail"
    logs["label"] = logs.cluster.map(names)
    logs["quality"] = [score_quality(p, r, f) for p, r, f in zip(logs.prompt, logs.response, logs.feedback)]

    run_id = uuid.uuid4().hex[:8]
    cases = build_cases(logs).assign(run_id=run_id)
    res = run_evals(cases, run_id, target)
    dist = logs.label.value_counts(normalize=True).to_dict()
    prev = db.read("runs")
    drift = jsd(dist, json.loads(prev.dist.iloc[-1])) if len(prev) else 0.0

    db.write(logs[["id", "ts", "prompt", "label", "cluster", "x", "y", "quality", "feedback"]], "clusters", "replace")
    db.write(cases, "cases"); db.write(res, "results")
    db.write(pd.DataFrame([dict(run_id=run_id, ts=datetime.utcnow(), n_logs=len(logs), n_clusters=len(names) - 1,
                                n_cases=len(cases), pass_rate=float(res.passed.mean()), drift=drift, dist=json.dumps(dist))]), "runs")
    return run_id
