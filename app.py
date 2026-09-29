import json
import pandas as pd, plotly.express as px, streamlit as st
from evalforge import db
from evalforge.pipeline import run_pipeline

st.set_page_config("EvalForge", "⚡", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Inter:wght@400;600&display=swap');
.stApp{background:radial-gradient(circle at 15% 0%,#12154a 0%,#05060f 55%);color:#e6f7ff;font-family:Inter,sans-serif}
h1,h2,h3{font-family:Orbitron,sans-serif!important;letter-spacing:.06em}
.hero{font-family:Orbitron;font-size:2.6rem;font-weight:800;background:linear-gradient(90deg,#00f0ff,#ff2bd6);-webkit-background-clip:text;color:transparent}
.kpi{background:rgba(255,255,255,.04);border:1px solid rgba(0,240,255,.35);border-radius:16px;padding:16px;backdrop-filter:blur(8px);box-shadow:0 0 22px rgba(0,240,255,.12)}
.kpi b{display:block;font-family:Orbitron;font-size:1.7rem;color:#00f0ff}.kpi span{color:#9fb3c8;font-size:.8rem;text-transform:uppercase}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="hero">EVALFORGE</div><p style="color:#9fb3c8">Production logs → living eval datasets</p>', unsafe_allow_html=True)
if st.sidebar.button("⚡ Run pipeline now", use_container_width=True):
    with st.spinner("Clustering, labeling, evaluating…"):
        run_pipeline()

runs, clusters = db.read("runs"), db.read("clusters")
if runs.empty:
    st.info("No runs yet — click **Run pipeline now** (synthetic logs are generated automatically)."); st.stop()
last = runs.iloc[-1]
cases, results = db.read("cases"), db.read("results")
cases, results = cases[cases.run_id == last.run_id], results[results.run_id == last.run_id]

for col, (v, l) in zip(st.columns(5), [(f"{last.n_logs:,}", "Logs processed"), (last.n_clusters, "Interaction clusters"),
        (last.n_cases, "Eval cases"), (f"{last.pass_rate:.0%}", "Pass rate"), (f"{last.drift:.3f}", "Traffic drift (JSD)")]):
    col.markdown(f'<div class="kpi"><b>{v}</b><span>{l}</span></div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["🌌 Cluster map", "🧪 Eval results", "✂️ Curate dataset", "📈 Run history"])
with t1:
    fig = px.scatter(clusters, x="x", y="y", color="label", hover_data=["prompt", "quality"], template="plotly_dark", height=520)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with t2:
    agg = results.groupby(["label", "kind"]).score.mean().reset_index()
    fig = px.bar(agg, x="label", y="score", color="kind", barmode="group", template="plotly_dark", color_discrete_sequence=["#00f0ff", "#ff2bd6", "#ffd166"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with t3:
    ed = st.data_editor(cases.assign(keep=True)[["keep", "kind", "label", "prompt", "reference", "quality"]], use_container_width=True, height=420)
    kept = ed[ed.keep].drop(columns="keep")
    st.download_button(f"⬇ Export {len(kept)} cases (JSONL)", "\n".join(kept.to_json(orient="records", lines=True).splitlines()), "eval_dataset.jsonl")
with t4:
    st.plotly_chart(px.line(runs, x="ts", y=["pass_rate", "drift"], markers=True, template="plotly_dark"), use_container_width=True)

st.markdown("---")
st.markdown("""**Designed and Developed by**

### NIKHIL CHARY SRIRAMOJU
BTech CSE (Final Year)

- GitHub: [Nikhil-creat](https://github.com/Nikhil-creat)
- LinkedIn: [nikhil-chary-sriramoju](https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a)
- Email: sriramojunikhil66@gmail.com
- Instagram: [@nikhil__sriramoju](https://www.instagram.com/nikhil__sriramoju)
- Facebook: [Profile](https://www.facebook.com/profile.php?id=100079201124141)""")
