import os
DB_URL = os.getenv("DATABASE_URL", "sqlite:///evalforge.db")
PROVIDER = os.getenv("LLM_PROVIDER", "heuristic")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
PASS_THRESHOLD = 0.5
NIGHTLY_AT = os.getenv("NIGHTLY_AT", "02:00")
