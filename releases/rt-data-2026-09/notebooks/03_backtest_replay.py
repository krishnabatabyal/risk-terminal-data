# %% [markdown]
# # 03 · Replaying the backtest corpus
#
# `backtest_events` is the dated corpus the engine is checked against:
# 500+ events across numbered phases, each with the model's reading at the
# time it was scored (`model_score_original`), the reading under the current
# model (`model_score_current`), and a hand-assigned reference severity
# (`human_score`). Phase 11 is a hold-out that is never retrained against.

# %%
from pathlib import Path
import pandas as pd

RELEASE = Path(".")

def load(table: str) -> pd.DataFrame:
    pq = RELEASE / f"{table}.parquet"
    return pd.read_parquet(pq) if pq.exists() else pd.read_csv(RELEASE / f"{table}.csv.gz")

bt = load("backtest_events")
bt["event_date"] = pd.to_datetime(bt["event_date"])
bt[["event_date", "country_code", "category", "severity", "phase",
    "model_score_original", "model_score_current", "human_score"]].head(10)

# %%
# Absolute error of the current model against the reference, per phase.
bt["abs_err"] = (bt["model_score_current"] - bt["human_score"]).abs()
by_phase = bt.groupby("phase")["abs_err"].agg(["count", "mean", "median"]).round(2)
by_phase

# %%
# Where the current model moved most relative to the reading it gave at the
# time. Large moves should line up with a methodology changelog entry.
bt["drift"] = bt["model_score_current"] - bt["model_score_original"]
bt.reindex(bt["drift"].abs().sort_values(ascending=False).index)[
    ["event_date", "country_code", "title", "phase", "model_score_original", "model_score_current", "drift"]
].head(15)

# %% [markdown]
# Keep Phase 11 out of any fitting you do on this corpus; it is the
# hold-out the project reports out-of-sample error on.
