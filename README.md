# ⚡ EvalForge — Automated Eval Dataset Generator from Production Logs

Turns production LLM traffic into a living eval dataset, so you never depend on stale hand-curated golden sets.

**Pipeline:** logs → PII scrub → embed → cluster → LLM topic labels + quality scoring → dataset builder (representative / failure / long-tail edge) → eval runner (LLM judge) → drift (JSD) → regression gate → dashboard → nightly scheduler.

## Repo layout
| Path | What |
|---|---|
| `docs/index.html` | Static in-browser demo, hosted on GitHub Pages |
| `evalforge/` | Python engine (HDBSCAN, LLM labeling, eval harness) |
| `app.py` | Streamlit dashboard |
| `api.py` | FastAPI: `/ingest`, `/run`, `/runs` |
| `scripts/eval_gate.py` + `.github/workflows/eval-gate.yml` | CI regression gate |
| `docker-compose.yml` | Postgres + dashboard + API + nightly worker |

## Run the full stack
```bash
cp .env.example .env && docker compose up --build   # dashboard :8501, API :8000
```
Set `LLM_PROVIDER=anthropic|openai` plus the API key in `.env` for real labeling and judging.

## Live demo (GitHub Pages)
Settings → Pages → Deploy from a branch → `main` / `/docs`. Demo loads `.jsonl` logs with `prompt`, `response`, `feedback` fields.

---
**Designed and Developed by**

### NIKHIL CHARY SRIRAMOJU
BTech CSE (Final Year)

- GitHub: [Nikhil-creat](https://github.com/Nikhil-creat)
- LinkedIn: [nikhil-chary-sriramoju](https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a)
- Email: sriramojunikhil66@gmail.com
- Instagram: [@nikhil__sriramoju](https://www.instagram.com/nikhil__sriramoju)
- Facebook: [Profile](https://www.facebook.com/profile.php?id=100079201124141)
