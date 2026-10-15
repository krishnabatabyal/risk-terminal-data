# Risk Terminal data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PENDING.svg)](https://doi.org/10.5281/zenodo.PENDING)

Open data releases from [Risk Terminal](https://risk-terminal.com/data): daily
country, regional and sub-national risk readings for 195 scored countries
(201 tracked) and 9 regions, with the model version and parameter fingerprint
stamped on every row.

> Disclaimer: this is not a prediction product. All scores, readings and
> analysis are based on current conditions.

Each release lives in its own folder under `releases/` and is immutable. A
correction ships as a later release, with a changelog note saying what changed
and why. Every tagged GitHub release is archived by Zenodo and receives its own
DOI.

## Releases

| release | status | folder |
|---|---|---|
| `rt-data-2026-09` | in preparation | `releases/rt-data-2026-09/` |

Each release folder carries its own `README.md`, `LICENSE`, `MANIFEST.json`
(SHA-256, byte size, row count and column list for every file),
`DATA_DICTIONARY.md`, `CHANGELOG.md` and `verify_release.py`.

## Verify a release

`verify_release.py` uses only the Python standard library:

```
python verify_release.py releases/rt-data-2026-09
```

It recomputes every file's hash and byte size, recounts rows, checks headers
against the manifest, and exits 0 on a clean pass.

## Quickstart

Every table ships as `<table>.parquet` and `<table>.csv.gz` with identical rows
and column order.

**Python**

```python
import pandas as pd

rel = "releases/rt-data-2026-09"
daily = pd.read_parquet(f"{rel}/country_scores_daily.parquet")
# or: pd.read_csv(f"{rel}/country_scores_daily.csv.gz")

ua = daily[daily["country_code"] == "UA"].sort_values("score_date")
print(ua[["score_date", "score", "delta_7d", "trend"]].tail())
```

**R**

```r
library(arrow)   # or: readr::read_csv("…/country_scores_daily.csv.gz")

rel <- "releases/rt-data-2026-09"
daily <- read_parquet(file.path(rel, "country_scores_daily.parquet"))
ua <- daily[daily$country_code == "UA", ]
tail(ua[order(ua$score_date), c("score_date", "score", "delta_7d", "trend")])
```

## How to cite

Cite the release id and its DOI, and state the model versions listed in that
release's `README.md`. That pair is enough for someone else to obtain the same
rows and recompute the same numbers.

```bibtex
@dataset{riskterminal_rt_data_2026_09,
  author    = {Batabyal, Krishna},
  title     = {Risk Terminal country risk readings, release rt-data-2026-09},
  year      = {2026},
  version   = {2026.09},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.PENDING},
  url       = {https://github.com/krishnabatabyal/risk-terminal-data}
}
```

The study design is pre-registered:
[10.17605/OSF.IO/2SVZF](https://doi.org/10.17605/OSF.IO/2SVZF).
`CITATION.cff` in this repository gives the same metadata in machine-readable
form.

## Licence

- Our tables and all documentation: **CC BY 4.0**.
- Office-holder facts sourced from Wikidata: **CC0 1.0**. Portrait columns are a
  URL, a credit and a per-row image licence; no image file is redistributed.
  Check each row's own licence before reusing a portrait.
- Model weights, prompts and lexicons are not published. Their SHA-256
  fingerprints are, on every row they produced.

Each release's `LICENSE` file gives the per-table statement. The data are free
to use, provided as-is, without warranty of any kind.
