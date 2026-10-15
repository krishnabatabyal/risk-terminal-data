# %% [markdown]
# # 01 · The score panel over a crisis
#
# Disclaimer: this is not a prediction product. All scores, readings and
# analysis are based on current conditions. Each row is what the engine
# measured about a country at that time. This notebook opens a
# release, picks a country, and plots its daily reading across a window,
# with the parameter fingerprint of the engine that produced each point.
#
# Run from a release directory (`rt-data-YYYY-MM/`). Needs pandas and
# pyarrow (or fall back to the `.csv.gz` files).

# %%
from pathlib import Path
import pandas as pd

RELEASE = Path(".")            # point this at the unpacked release
COUNTRY = "UA"                 # ISO 3166-1 alpha-2

def load(table: str) -> pd.DataFrame:
    pq = RELEASE / f"{table}.parquet"
    return pd.read_parquet(pq) if pq.exists() else pd.read_csv(RELEASE / f"{table}.csv.gz")

daily = load("country_scores_daily")
daily["score_date"] = pd.to_datetime(daily["score_date"])
one = daily[daily["country_code"] == COUNTRY].sort_values("score_date")
one[["score_date", "score", "delta_7d", "delta_30d", "trend"]].tail(10)

# %%
# The reading over time. Bands (from the site's methodology):
# critical ≥ 80 · high ≥ 65 · elevated ≥ 50 · moderate ≥ 35 · low < 35.
ax = one.plot(x="score_date", y="score", figsize=(10, 4), legend=False,
              title=f"{COUNTRY} · daily reading")
for level in (35, 50, 65, 80):
    ax.axhline(level, linewidth=0.5, linestyle=":")
ax.set_ylabel("reading (0–100)")

# %%
# Which apparatus produced which rows. `country_scores` carries the
# per-cycle fingerprint; join it to the daily archive by country and date.
cycles = load("country_scores")
cycles["score_date"] = pd.to_datetime(cycles["computed_at"]).dt.normalize() if "computed_at" in cycles else pd.NaT
fp = (cycles[cycles["country_code"] == COUNTRY]
      .groupby("weights_hash")["score_date"].agg(["min", "max", "count"])
      .sort_values("min"))
fp

# %% [markdown]
# Two rows with the same `weights_hash` came from the same parameter set.
# When the hash changes, look the date up in `METHODOLOGY_CHANGELOG.md`
# (shipped in the release) before comparing readings across it.
