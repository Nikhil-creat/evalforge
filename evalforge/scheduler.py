import time, schedule
from .config import NIGHTLY_AT
from .pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
    schedule.every().day.at(NIGHTLY_AT).do(run_pipeline)
    while True:
        schedule.run_pending(); time.sleep(30)
