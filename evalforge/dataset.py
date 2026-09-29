import pandas as pd

def build_cases(df, per_cluster=6, fail_per_cluster=2, edge_k=10):
    """Three case types: representative (coverage), failure (regressions), edge (long tail)."""
    parts = []
    for c, g in df[df.cluster >= 0].groupby("cluster"):
        parts.append(g[g.quality >= 0.7].nsmallest(per_cluster, "dist").assign(kind="representative"))
        parts.append(g[g.quality < 0.4].head(fail_per_cluster).assign(kind="failure"))
    noise = df[df.cluster == -1]
    parts.append(noise.sample(min(edge_k, len(noise)), random_state=0).assign(kind="edge"))
    cases = pd.concat(parts).drop_duplicates("id")
    cases["reference"] = cases.response.where(cases.kind == "representative")
    return cases[["id", "cluster", "label", "kind", "prompt", "response", "reference", "quality"]]
