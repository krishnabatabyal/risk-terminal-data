# Risk Terminal data — rt-data-2026-09

Disclaimer: this is not a prediction product. All scores, readings and analysis are based on current conditions.

Every number in this release is a reading of
conditions that were already observable when it was computed: what happened,
where, how credible the reporting was, and how much it moved a country's
position relative to its own recent history. Nothing here projects forward, and
no column should be read as an expectation about what comes next. The panel is
a measurement record, and it is published with the fingerprint of the apparatus
that produced each row so that a reviewer can tell which version of the engine
made which measurement.

## What is in here

- **18 tables**, 36 data files, 531,648 rows.
- **Countries:** 195 scored, 201 tracked. **Regions:** 9.
- **Panel start:** 2026-04-18. The clean observation window — the
  span scored end-to-end by one continuous methodology — opens
  **2026-07-02**. Rows before that date are real readings but
  were produced by earlier model versions; the changelog says which.
- **Cadence:** scoring runs hourly; releases are cut monthly, on the 5th.
- **This cut's `--since` filter:** none (full history).
- **This cut's cutoff (`--until`, exclusive):** 2026-09-08T01:27:06+00:00. Dated tables stop
  there. Current-state tables (leaders, elections, explainers, people coverage,
  chambers, legislation) are exported as they stood when the cut was built.
- **Built at:** 2026-10-15T12:57:02+00:00 · **builder commit:** 6a4b8b5a ·
  **current model version:** scorer-v5.0.3.

| file | rows | dated by | span | licence |
|---|---|---|---|---|
| `country_scores` | 21,547 | computed_at | 2026-04-18T23:11:44.232770+00:00 → 2026-09-07T23:43:56.926972+00:00 | CC BY 4.0 |
| `country_scores_daily` | 23,660 | score_date | 2026-05-12 → 2026-09-07 | CC BY 4.0 |
| `region_scores` | 1,753 | computed_at | 2026-03-17T00:00:00+00:00 → 2026-09-07T23:43:57.215887+00:00 | CC BY 4.0 |
| `subnational_scores` | 84,600 | computed_at | 2026-06-06T23:47:58.812531+00:00 → 2026-09-07T23:44:09.832867+00:00 | CC BY 4.0 |
| `measurement_regime_daily` | 60 | day | 2026-07-10 → 2026-09-07 | CC BY 4.0 |
| `score_explainers` | 201 | — | — | CC BY 4.0 |
| `score_explainer_history` | 1,494 | generated_at | 2026-07-19T04:00:06.440502+00:00 → 2026-09-07T04:05:33.818350+00:00 | CC BY 4.0 |
| `people` | 833 | — | — | CC0 1.0 (Wikidata facts); per-row licence for portrait URLs |
| `people_positions` | 851 | — | — | CC0 1.0 (Wikidata facts); per-row licence for portrait URLs |
| `people_changes` | 162 | ts | 2026-09-07T21:23:49.221690+00:00 → 2026-09-08T00:29:52.295502+00:00 | CC0 1.0 (Wikidata facts); per-row licence for portrait URLs |
| `people_coverage` | 201 | — | — | CC BY 4.0 |
| `people_chambers` | 283 | — | — | CC0 1.0 (Wikidata facts); per-row licence for portrait URLs |
| `leaders` | 252 | — | — | CC BY 4.0 (ours) with open-source facts attributed per row |
| `leadership_events` | 28,161 | — | — | CC BY 4.0 (ours) with open-source facts attributed per row |
| `elections` | 187 | — | — | CC BY 4.0 (ours) with open-source facts attributed per row |
| `legislation` | 0 | — | — | CC BY 4.0 (ours) with open-source facts attributed per row |
| `backtest_events` | 544 | — | — | CC BY 4.0 |
| `events_metadata` | 366,859 | ingested_at | 2026-03-17T20:18:13.195880+00:00 → 2026-09-08T01:24:52.194005+00:00 | CC BY 4.0 |

Files ship as `<table>.csv.gz` and, where the build environment had Parquet
support, `<table>.parquet`. Both carry identical rows and identical column
order. `MANIFEST.json` lists every file with its SHA-256, byte size, row count,
column list and column types.

## Fingerprints in this release

- **Model versions:** `scorer-v3.2`, `scorer-v4.0`, `scorer-v4.2`, `scorer-v5.0`, `scorer-v5.0.1`, `subnational-v1.0`
- **Parameter fingerprints (`weights_hash`):** `2b29d791dbb5aae81177fe4abda829dc4ffd79211c77948e412e4e04cc0d93ba`, `7bdda525ebb44cf4b79ee2fa71ffe92d7488e7520ba5f23e018786a0a5687e63`, `eeb2d3581732f9f3b91788eb5947bd1b0c33c08a9a458e0b281d42708311bea2`, `f7d18360db8cd38da3792d11af7e96ed659435b938eb836484b75c83343fb7b9`
- **Pipeline fingerprints (`pipeline_hash`):** `118745d7e2b28cb3f604418675fe55f5a422a135af8c6492f06e7eff60787248`, `2875e622b819663fc4d5e9ea511f376bf921a190f884592616d7c85d2f06b635`, `34e965c481c622a0773bc43080019c938b21e70261e1aa0c548569368f6f935b`, `7781e1878b784ef0ce298e7c1ad8e17c1dfadfd76ff0179c5ba1eb0efeafc158`, `7fc6b7e2ed195209ab5c1bd0d8a23f33f49e880e9026de04600b728145252dbc`

Each of these is documented in the methodology changelog. Weights, prompts and
lexicons stay private; their SHA-256 fingerprints are published with every row,
so a reviewer can prove two rows came from the same apparatus without seeing the
apparatus.

## What does not ship

- **Headlines and article text** — Third-party editorial text from the feeds. Source URL only.
- **Image files** — Portrait URLs, credits and licences ship; no image bytes are redistributed.
- **Model weights, prompts, lexicons** — Private. Their SHA-256 fingerprints are published with every row.
- **Market vendor quotes** — Vendor terms. Derived stress readings only, if at all.
- **Third-party inputs carried on a score row** — Published macro projections and search-interest series are inputs we are licensed to read, not to redistribute. The readings they feed do ship.
- **Prohibited and held sources** — Sources whose terms forbid automated access, or whose licence is unresolved, are never ingested.
- **Customer institution names** — Private unless an institution asks to be listed.

A table ships only when every column in it is ours, CC0, or explicitly
open-licensed with the licence recorded beside the value. A value in a column
we write ships only when it is our own text: a summary that copies a source
headline, carries a publisher suffix, or reads forward is set to null, and the
changelog counts every such value.

## Known gaps — read these before you model anything

- **Event coverage is uneven by country.** The pipeline reads what the world
  publishes in the languages and feeds it can reach. A country with few rows in
  `events_metadata` is a country with thin coverage, not a quiet country. Use
  `measurement_regime_daily` to see what the apparatus could observe on a given
  day before attributing a change to the world.
- **People coverage is per country and is stated, not implied.** Read
  `people_coverage` alongside `people` and `people_positions`: a missing
  legislature is a gap in our reach, not an empty chamber.
- **Explainer text is model-written.** Columns marked `AI-derived` in the data
  dictionary came out of a language model reading our own structured data. They
  are commentary on the reading, not evidence for it.
- **Structural inputs move slowly.** Some baselines refresh annually. A flat
  structural component across several months is the source's cadence, not a
  stalled pipeline.
- **Some inputs are read but not redistributed.** The engine reads material we
  are licensed to consume and not to pass on — published macro projections from
  an intergovernmental statistical body, search-interest series from a search
  provider, market quotes under vendor terms. Those raw columns are struck out
  of every export. The readings they feed do ship, so a row can be traced to the
  model version that produced it even where an input cannot be re-obtained from
  this release alone.
- **Corrections are new releases.** Nothing in a published release is ever
  edited in place. If a row was wrong, a later release carries the fix and the
  changelog says so.

## How to verify this release

```
python verify_release.py .
```

The script recomputes every file's SHA-256 and byte size, recounts rows by
streaming the gzipped CSVs, checks each header against the manifest, asserts
that no third-party editorial column appears anywhere, and — when a copy of the
methodology changelog is available — checks that every model version and
fingerprint in the manifest is documented. It exits 0 on a clean pass and 1 on
any mismatch. It has no dependencies beyond the Python standard library, so it
runs inside a downloaded release directory with nothing else installed.

## Licence

Our tables are CC BY 4.0. Tables whose facts come from a public knowledge base
are CC0 for the facts; portrait columns carry a URL, a credit and a per-row
image licence, and no image file is redistributed. Documentation is CC BY 4.0.
See `LICENSE` for the per-table statement.

Free for academic use.

## How to cite

Pre-registration: [10.17605/OSF.IO/2SVZF](https://doi.org/10.17605/OSF.IO/2SVZF), frozen at commit
`ec9f02c` on 2026-07-04.

Dataset DOI: `10.5281/zenodo.PENDING` (assigned on deposit; until then cite the
pre-registration DOI and the release id).

```bibtex
@dataset{riskterminal_rt-data-2026-09,
  title   = {Risk Terminal geopolitical risk readings, release rt-data-2026-09},
  year    = {2026},
  version = {rt-data-2026-09},
  doi     = {10.5281/zenodo.PENDING},
  note    = {Disclaimer: this is not a prediction product. All scores, readings and analysis are based on current conditions.
             Pre-registration DOI 10.17605/OSF.IO/2SVZF.}
}
```

When a paper reports results from this panel, state the release id and the
model versions listed above. That pair is enough for someone else to obtain the
same rows and recompute the same numbers.
