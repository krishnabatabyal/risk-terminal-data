# %% [markdown]
# # 02 · People turnover against the reading
#
# `people_changes` records appointments, departures and portrait additions
# for cabinets (tier A), legislatures (tier B) and departments (tier C),
# sourced from Wikidata (CC0). This notebook counts office changes per
# country per week and lays them next to the country's reading.
#
# Coverage caveat: `people_coverage` says how complete each country's record
# is. A country with few changes may simply be thinly covered.

# %%
from pathlib import Path
import pandas as pd

RELEASE = Path(".")

def load(table: str) -> pd.DataFrame:
    pq = RELEASE / f"{table}.parquet"
    return pd.read_parquet(pq) if pq.exists() else pd.read_csv(RELEASE / f"{table}.csv.gz")

changes = load("people_changes")
changes["ts"] = pd.to_datetime(changes["ts"])
tier_a = changes[(changes["tier"] == "A") & changes["kind"].isin(["appointed", "left", "died"])]
weekly = (tier_a.set_index("ts").groupby("country_code")
          .resample("W")["kind"].count().rename("office_changes").reset_index())
weekly.sort_values("office_changes", ascending=False).head(10)

# %%
daily = load("country_scores_daily")
daily["score_date"] = pd.to_datetime(daily["score_date"])
week_score = (daily.set_index("score_date").groupby("country_code")["score"]
              .resample("W").mean().rename("mean_reading").reset_index()
              .rename(columns={"score_date": "ts"}))
joined = weekly.merge(week_score, on=["country_code", "ts"], how="left")
joined.head()

# %%
coverage = load("people_coverage")
coverage[["country_code", "cabinet_posts_filled", "ministers_filled",
          "has_head_of_state", "has_head_of_government", "portrait_share"]].head(20)

# %% [markdown]
# Read the join with the coverage table open. The first sweep of a country
# writes no change rows (a backfill is not news), so turnover only starts
# accumulating from a country's second sweep onward.
