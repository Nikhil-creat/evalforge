import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from evalforge import db
from evalforge.pipeline import run_pipeline

app = FastAPI(title="EvalForge API", description="Ingest production logs, trigger pipeline runs, read run history.")

class Log(BaseModel):
    prompt: str
    response: str
    feedback: int = 0
    latency_ms: int = 0
    model: str = "prod"

@app.post("/ingest")
def ingest(logs: list[Log]):
    df = pd.DataFrame([l.model_dump() for l in logs]); df["ts"] = pd.Timestamp.utcnow().tz_localize(None)
    ex = db.read("logs"); start = int(ex.id.max()) + 1 if len(ex) else 0
    df.insert(0, "id", range(start, start + len(df))); db.write(df, "logs")
    return {"ingested": len(df)}

@app.post("/run")
def run(): return {"run_id": run_pipeline()}

@app.get("/runs")
def runs(): return db.read("runs").drop(columns="dist").to_dict("records")
