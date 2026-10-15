# Data dictionary — rt-data-2026-09

Generated from the models at build time, so this file cannot drift from
the columns that actually shipped.

**Provenance** reads as follows.

| Value | Meaning |
|---|---|
| `measured` | Recorded from a source, or computed deterministically from recorded values. |
| `AI-assisted` | The column is recorded, but it sits in a table whose narrative columns are model-written. |
| `AI-derived` | The value itself came out of a language model. Read it as prose, not as an observation. |

Every value in this release is a reading of observed conditions at the row's
own timestamp. No column projects forward.

## `country_scores`

Source table `country_risk_scores` · licence CC BY 4.0

Country readings, one row per country per day (`score_date`), holding the latest hourly scoring cycle of that day, from 2026-04-18. Each row carries the model version and the parameter fingerprint that produced it. The daily archive with the full component breakdown is `country_scores_daily`.

*A reading of observed conditions at computed_at, not a projection.*

`--since` filters this table on `computed_at`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `country` | string | no | measured |  |
| `country_code` | string | yes | measured | ISO 3166-1 alpha-2 |
| `region` | string | no | measured |  |
| `score` | double | no | measured |  |
| `score_short_term` | double | yes | measured | The engine's event-driven reading before any structural floor lifts it. Mean-reverting: it falls when the news quiets. `score` is the larger of this and `score_structural`. |
| `score_structural` | double | yes | measured |  |
| `previous_score` | double | yes | measured |  |
| `engine_score_raw` | double | yes | measured | Pre-floor engine output (2026-07-02) — consumed by the tension-memory floor so the EWMA reads what the engine computed, not what floors lifted it to (post-floor input would ratchet). |
| `weights_hash` | string | yes | measured | SHA-256 over the full model parameter set at scoring time (2026-07-03). |
| `trend` | string | yes | measured | rising, falling, stable |
| `delta_7d` | double | yes | measured | score change vs 7 days ago |
| `avg_sentiment_24h` | double | yes | measured | avg event sentiment last 24h |
| `components` | string | yes | measured |  |
| `modifiers` | string | yes | measured |  |
| `baseline_30d` | double | yes | measured | 30-day rolling average score |
| `volatility_30d` | double | yes | measured | 30-day stdev of daily scores |
| `anomaly_zscore` | double | yes | measured | (score - baseline) / volatility |
| `anomaly_label` | string | yes | measured | null, "spike", "calm", "extreme" |
| `anomaly_flag` | bool | no | measured | 90-day anomaly flag: z > 2.5 with at least 14 data points |
| `market_attention_score` | double | yes | measured | Market attention: avg abs(change_pct) across country-linked market symbols, scaled 0-100 |
| `computed_at` | timestamp | no | measured |  |
| `score_date` | date | no | measured |  |
| `model_version` | string | yes | measured | Scoring model versioning — populated by the scoring job |
| `calibration_date` | date | yes | measured |  |

## `country_scores_daily`

Source table `country_score_daily` · licence CC BY 4.0

Frozen end-of-day country reading, one row per country per day.

`--since` filters this table on `score_date`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `country` | string | no | measured |  |
| `country_code` | string | no | measured | ISO 3166-1 alpha-2 |
| `region` | string | yes | measured |  |
| `score_date` | date | no | measured |  |
| `score` | double | no | measured | Frozen EOD reading |
| `delta_7d` | double | yes | measured |  |
| `delta_30d` | double | yes | measured |  |
| `trend` | string | yes | measured |  |
| `anomaly_zscore` | double | yes | measured |  |
| `components` | string | yes | measured | Frozen component decomposition (top_contributors, modifiers etc.) |
| `modifiers` | string | yes | measured |  |
| `snapshotted_at` | timestamp | no | measured | When this snapshot row was written (i.e. the EOD job time). |

## `region_scores`

Source table `region_risk_scores` · licence CC BY 4.0

Regional readings, one row per region per scoring cycle.

`--since` filters this table on `computed_at`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `region` | string | no | measured |  |
| `score` | double | no | measured |  |
| `previous_score` | double | yes | measured |  |
| `trend` | string | yes | measured |  |
| `delta_7d` | double | yes | measured | score change vs 7 days ago |
| `avg_sentiment_24h` | double | yes | measured | avg event sentiment last 24h |
| `top_drivers` | string | yes | measured |  |
| `computed_at` | timestamp | no | measured |  |
| `score_date` | date | no | measured |  |

## `subnational_scores`

Source table `country_subnational_scores` · licence CC BY 4.0

Admin-1 sub-national readings for the countries with admin-1 coverage.

`--since` filters this table on `computed_at`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `country` | string | no | measured |  |
| `country_code` | string | no | measured |  |
| `admin1_code` | string | no | measured |  |
| `admin1_name` | string | no | measured |  |
| `region` | string | yes | measured |  |
| `score` | double | no | measured |  |
| `score_short_term` | double | yes | measured |  |
| `score_structural` | double | yes | measured |  |
| `previous_score` | double | yes | measured |  |
| `trend` | string | yes | measured | rising, falling, stable |
| `delta_7d` | double | yes | measured |  |
| `direct_event_count` | int64 | yes | measured |  |
| `components` | string | yes | measured |  |
| `modifiers` | string | yes | measured |  |
| `computed_at` | timestamp | no | measured |  |
| `score_date` | date | no | measured |  |
| `model_version` | string | yes | measured |  |

## `measurement_regime_daily`

Source table `measurement_regime_daily` · licence CC BY 4.0

Daily record of the measurement apparatus itself — what the pipeline could see on a given day. Needed to read the panel honestly.

`--since` filters this table on `day`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `day` | date | no | measured |  |
| `total_events` | int64 | yes | measured | Event coverage — how the day's events were classified |
| `llm_enriched` | int64 | yes | measured |  |
| `rules_only` | int64 | yes | measured |  |
| `coverage_pct` | double | yes | measured |  |
| `enrichment_spend_usd` | double | yes | measured |  |
| `floor_decided` | int64 | yes | measured | Criterion-4 share — which mechanism decided each country's published score |
| `engine_decided` | int64 | yes | measured |  |
| `engine_within_3pts` | int64 | yes | measured |  |
| `countries_total` | int64 | yes | measured |  |
| `model` | string | yes | measured | Provenance |
| `enrichment_version` | string | yes | measured |  |
| `pipeline_hash` | string | yes | measured | integrity.pipeline_fingerprint() |
| `created_at` | timestamp | no | measured | When this row was first written by the pipeline. |

## `score_explainers`

Source table `country_score_explainers` · licence CC BY 4.0

Current per-country narrative and key drivers behind a reading.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | AI-assisted | Primary key of the source row. Stable across releases. |
| `country_code` | string | no | AI-assisted | ISO 3166-1 alpha-2 |
| `country` | string | no | AI-assisted |  |
| `score_at_generation` | double | no | AI-assisted | Score state at the moment of generation — so we can detect when an explainer is stale relative to the current score. |
| `delta_7d_at_generation` | double | yes | AI-assisted |  |
| `summary` | string | no | AI-derived | AI output |
| `key_drivers` | string | yes | AI-derived | key_drivers: [{"factor": "M23 advances", "magnitude": "+12.3 pts", "tone": "negative"}] |
| `voice_score` | double | yes | AI-assisted | House-prose quality score of the explainer text at generation (0-100). Diagnostic only; nothing gates on it. Null on rows written before 2026-09-08. |
| `model_used` | string | yes | AI-assisted | Provenance |
| `generated_at` | timestamp | no | AI-assisted |  |

## `score_explainer_history`

Source table `country_score_explainer_history` · licence CC BY 4.0

Append-only history of every explainer generation, each attributed to the score, model version and parameter fingerprints that produced it.

`--since` filters this table on `generated_at`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | AI-assisted | Primary key of the source row. Stable across releases. |
| `country_code` | string | no | AI-assisted | ISO 3166-1 alpha-2 |
| `country` | string | no | AI-assisted |  |
| `score_at_generation` | double | no | AI-assisted | Score state at the moment of generation |
| `delta_7d_at_generation` | double | yes | AI-assisted |  |
| `summary` | string | no | AI-derived | AI output — copied verbatim from the current-row schema |
| `key_drivers` | string | yes | AI-derived |  |
| `model_used` | string | yes | AI-assisted | Provenance |
| `weights_hash` | string | yes | AI-assisted | scoring.weights_fingerprint() |
| `pipeline_hash` | string | yes | AI-assisted | integrity.pipeline_fingerprint() |
| `generated_at` | timestamp | no | AI-assisted |  |

## `people`

Source table `people` · licence CC0 1.0 (Wikidata facts); per-row licence for portrait URLs

One row per office-holder. Portrait columns are a URL, a credit and a licence string — no image file is redistributed.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `wikidata_qid` | string | yes | measured | Natural key when the person came from Wikidata (the usual case). |
| `person_key` | string | yes | measured | Fallback key for non-Wikidata sources: "<source>:<slug>". Unique together with nothing — the uniqueness is enforced by the upsert, not the DB, so a bad key can never wedge a sweep. |
| `name` | string | no | measured |  |
| `country_code` | string | no | measured |  |
| `gender` | string | yes | measured |  |
| `birth_date` | date | yes | measured |  |
| `image_url` | string | yes | measured | Portrait — populated only when the licence check passes. |
| `image_credit` | string | yes | measured |  |
| `image_license` | string | yes | measured |  |
| `image_checked_at` | timestamp | yes | measured |  |
| `authority_score` | int64 | yes | measured | 0-100, deterministic: how much executive authority the person's highest current office carries. |
| `source` | string | no | measured |  |
| `last_verified_at` | timestamp | yes | measured |  |
| `last_revid` | int64 | yes | measured | Wikidata `lastrevid` of this person's item at the last change check. Only items whose revision moved are re-read. |
| `revid_checked_at` | timestamp | yes | measured | When the delta job last looked. Drives the "oldest checked first" half of the delta cursor, so every person is eventually re-checked even if the authority ordering never reaches them. |
| `created_at` | timestamp | no | measured | When this row was first written by the pipeline. |
| `updated_at` | timestamp | no | measured | When this row was last rewritten by the pipeline. |

## `people_positions`

Source table `people_positions` · licence CC0 1.0 (Wikidata facts); per-row licence for portrait URLs

One row per office held. ended_on IS NULL means sitting.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `person_id` | int64 | no | measured |  |
| `country_code` | string | no | measured |  |
| `position_label` | string | no | measured |  |
| `position_qid` | string | yes | measured |  |
| `tier` | string | no | measured | A = heads of state and government and ministers; B = national legislators; C = departments and security offices. |
| `role_kind` | string | yes | measured | head_of_state \| head_of_government \| minister \| central_bank_governor \| … |
| `org` | string | yes | measured | Ministry / chamber / agency the office sits in. Free text — the label of the parent organisation when Wikidata has one, else the position label. |
| `chamber_code` | string | yes | measured |  |
| `party` | string | yes | measured |  |
| `term` | string | yes | measured | Tier B: the P2937 "parliamentary term" qualifier ("21st Riksdag") and the P768 electoral district. Both are per-statement facts, so they belong on the position and not on the person. |
| `district` | string | yes | measured |  |
| `started_on` | date | yes | measured |  |
| `ended_on` | date | yes | measured |  |
| `authority_score` | int64 | yes | measured |  |
| `source` | string | no | measured |  |
| `confidence` | double | no | measured |  |
| `verified_at` | timestamp | yes | measured |  |
| `created_at` | timestamp | no | measured | When this row was first written by the pipeline. |

## `people_changes`

Source table `people_changes` · licence CC0 1.0 (Wikidata facts); per-row licence for portrait URLs

Append-only ledger of appointments, departures and reshuffles.

`--since` filters this table on `ts`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `ts` | timestamp | no | measured |  |
| `country_code` | string | no | measured |  |
| `person_id` | int64 | yes | measured |  |
| `person_name` | string | yes | measured |  |
| `kind` | string | no | measured | appointed \| left \| reshuffled \| portrait_added \| died |
| `from_position` | string | yes | measured |  |
| `to_position` | string | yes | measured |  |
| `tier` | string | yes | measured |  |
| `role_kind` | string | yes | measured | The office's role kind (head_of_state \| minister \| chief_of_defence …). Added in P4: the wire-event filter is "tier A, or a tier-C SECURITY office", and the tier letter alone cannot tell a chief of defence from an ambassador. Populated by every sweep that writes a change row. |
| `source_ref` | string | yes | measured |  |
| `event_emitted_at` | timestamp | yes | measured | Set once a wire event has been emitted for this change; it stops a re-run from posting the same change twice. |

## `people_coverage`

Source table `people_coverage` · licence CC BY 4.0

Per-country people coverage, so a gap reads as a gap and not as a zero.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `country_code` | string | no | measured |  |
| `cabinet_posts_filled` | int64 | no | measured |  |
| `ministers_filled` | int64 | no | measured | Ministers only (excludes the two heads and the central-bank governor). |
| `has_head_of_state` | bool | no | measured |  |
| `has_head_of_government` | bool | no | measured |  |
| `with_portrait` | int64 | no | measured |  |
| `portrait_share` | double | no | measured |  |
| `chambers_count` | int64 | no | measured | Number of national legislative chambers swept for this country. `seats_filled / seats_total` is the legislature coverage ratio; a country whose chambers were never swept keeps zeros rather than a false 100%. |
| `seats_total` | int64 | no | measured |  |
| `seats_filled` | int64 | no | measured |  |
| `seats_with_portrait` | int64 | no | measured |  |
| `seat_portrait_share` | double | no | measured |  |
| `tier_c_filled` | int64 | no | measured | Tier C offices filled. `tier_c_expected` counts the departments and security offices we expect a country to have, not what Wikidata happens to model, so the gap between the two is a stated coverage gap. |
| `tier_c_expected` | int64 | no | measured |  |
| `tier_c_with_portrait` | int64 | no | measured |  |
| `tier_c_gaps` | string | yes | measured | Comma-separated role kinds we found nothing for. Kept as text rather than a join table: it is a caveat string, ~8 short tokens, read by the coverage report and never queried by value. |
| `computed_at` | timestamp | no | measured |  |

## `people_chambers`

Source table `people_chambers` · licence CC0 1.0 (Wikidata facts); per-row licence for portrait URLs

Registry of national legislative chambers and their statutory seats.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `chamber_code` | string | no | measured |  |
| `country_code` | string | no | measured |  |
| `chamber_type` | string | no | measured | lower \| upper \| unicameral |
| `name` | string | yes | measured |  |
| `legislature_name` | string | yes | measured |  |
| `legislature_qid` | string | yes | measured |  |
| `chamber_qid` | string | yes | measured |  |
| `position_qid` | string | yes | measured |  |
| `seats` | int64 | yes | measured |  |
| `seats_filled` | int64 | no | measured | Filled in by the sweep — seats we actually hold a sitting member for. |
| `with_portrait` | int64 | no | measured |  |
| `member_source` | string | yes | measured | Which adapter last wrote this chamber's members ("wikidata", "uk_parliament", "congress_gov", …). Never used to delete anything. |
| `source` | string | no | measured |  |
| `last_swept_at` | timestamp | yes | measured |  |
| `updated_at` | timestamp | no | measured | When this row was last rewritten by the pipeline. |

## `leaders`

Source table `leaders` · licence CC BY 4.0 (ours) with open-source facts attributed per row

Heads of state and government tracked by the engine.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | AI-assisted | Primary key of the source row. Stable across releases. |
| `name` | string | no | AI-assisted |  |
| `country` | string | no | AI-assisted |  |
| `country_code` | string | yes | AI-assisted | ISO 3166-1 alpha-2 |
| `region` | string | no | AI-assisted |  |
| `title` | string | no | AI-assisted |  |
| `party` | string | yes | AI-assisted |  |
| `in_office_since` | date | yes | AI-assisted |  |
| `term_ends` | date | yes | AI-assisted |  |
| `status` | string | no | AI-assisted |  |
| `role_type` | string | yes | AI-assisted | head_of_state \| head_of_government |
| `stability` | string | yes | AI-assisted | Stable / Fragile / Weakened / Stressed / New — watch / Critical |
| `risk_factors` | string | yes | AI-assisted | JSON array string: ["factor1", "factor2"] |
| `ai_summary` | string | yes | AI-derived | 2-3 sentence analyst assessment |
| `last_refreshed` | timestamp | yes | AI-assisted |  |
| `last_verified_at` | timestamp | yes | AI-assisted | Human-verified date |
| `confidence` | double | yes | AI-assisted | 0.0–1.0 AI confidence in current identity |
| `source_count` | int64 | yes | AI-assisted | Number of sources confirming identity |
| `stability_score` | int64 | yes | AI-assisted | 0-100 numeric; derived from stability string |
| `bio_data` | string | yes | AI-assisted |  |
| `policy_positions` | string | yes | AI-assisted |  |
| `vuln_data` | string | yes | AI-assisted |  |
| `image_url` | string | yes | AI-assisted | Wikidata-sourced portrait URL. No image file ships. |
| `image_credit` | string | yes | AI-assisted |  |
| `effective_authority_score` | double | yes | AI-assisted | Sort key for leaders within a country: executive authority in practice. Example values: supreme leader or general secretary 99, president 95, prime minister 90, ceremonial head of state 20-25, vice president 30. |
| `acting` | bool | no | AI-assisted | True when the holder is interim (for example an acting president after a resignation). `identity_source` names the process that last set who holds the row; `succeeded_by_id` links a retired row to its successor's row. |
| `identity_source` | string | yes | AI-assisted |  |
| `succeeded_by_id` | int64 | yes | AI-assisted |  |
| `wikidata_qid` | string | yes | AI-assisted |  |

## `leadership_events`

Source table `leadership_events` · licence CC BY 4.0 (ours) with open-source facts attributed per row

Dated leadership transitions and succession events.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | AI-assisted | Primary key of the source row. Stable across releases. |
| `leader_id` | int64 | yes | AI-assisted |  |
| `country` | string | no | AI-assisted |  |
| `region` | string | no | AI-assisted |  |
| `event_type` | string | no | AI-assisted | resignation, reshuffle, election, impeachment, coup |
| `detail` | string | yes | AI-derived |  |
| `occurred_at` | timestamp | no | AI-assisted |  |
| `ingested_at` | timestamp | no | AI-assisted |  |

## `elections`

Source table `elections` · licence CC BY 4.0 (ours) with open-source facts attributed per row

Scheduled and completed national elections, with verified results where published.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | AI-assisted | Primary key of the source row. Stable across releases. |
| `country` | string | no | AI-assisted |  |
| `country_code` | string | yes | AI-assisted | ISO 3166-1 alpha-2 |
| `region` | string | no | AI-assisted |  |
| `office` | string | no | AI-assisted |  |
| `election_date` | date | no | AI-assisted |  |
| `election_type` | string | yes | AI-assisted |  |
| `current_leader` | string | yes | AI-assisted |  |
| `ruling_party` | string | yes | AI-assisted |  |
| `opposition_front_runner` | string | yes | AI-assisted |  |
| `opposition_note` | string | yes | AI-derived |  |
| `status` | string | yes | AI-assisted | status: scheduled \| completed \| cancelled \| disputed |
| `risk_note` | string | yes | AI-derived |  |
| `source_url` | string | yes | AI-assisted |  |
| `last_verified_at` | timestamp | yes | AI-assisted | Human-verified date |
| `ai_assessment` | string | yes | AI-derived | Model-written post-election assessment, filled after the election is completed. |
| `ai_assessed_at` | timestamp | yes | AI-assisted |  |
| `result_status` | string | yes | AI-assisted | 'awaiting' or 'verified'. Results are filled after the election is completed. |
| `winner` | string | yes | AI-assisted |  |
| `winning_party` | string | yes | AI-assisted |  |
| `turnout` | double | yes | AI-assisted |  |
| `result_data` | string | yes | AI-assisted | {"candidates":[{"name":str,"party":str\|null,"share":float}],"margin":str\|null} |
| `result_summary` | string | yes | AI-assisted |  |
| `result_verified_at` | timestamp | yes | AI-assisted |  |
| `verified_source` | string | yes | AI-assisted | Provenance of the last automated change: 'wikidata:Q…+news', 'news:snap', or a manual review marker. Null means seed data entered by hand. |
| `wikidata_qid` | string | yes | AI-assisted |  |

## `legislation`

Source table `legislation` · licence CC BY 4.0 (ours) with open-source facts attributed per row

Bills and instruments from official open legislative data.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `country_code` | string | no | measured | ISO alpha-2 country code ("US", "GB", "FR", ...) or "EU" for Union-level acts. |
| `record_type` | string | no | measured | "bill" \| "law" |
| `title` | string | no | measured |  |
| `status` | string | yes | measured | Source-reported lifecycle state, lightly normalized. |
| `category` | string | yes | measured | Source-reported bill/law type or our coarse subject category. |
| `summary` | string | yes | AI-derived | SHORT factual summary (facts only — never source prose / full text). |
| `introduced_date` | string | yes | measured | YYYY-MM-DD |
| `last_action_date` | string | yes | measured | YYYY-MM-DD |
| `source_name` | string | no | measured |  |
| `source_ref` | string | no | measured | Stable per-source identifier used for idempotent upsert. |
| `source_url` | string | yes | measured |  |
| `updated_at` | timestamp | no | measured | When this row was last rewritten by the pipeline. |

## `backtest_events`

Source table `backtest_events` · licence CC BY 4.0

The dated validation corpus. Phase 11 is a hold-out and is never retrained against.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | measured | Primary key of the source row. Stable across releases. |
| `title` | string | no | measured | ── Identity ────────────────────────────────────────────────────────────── |
| `description` | string | yes | measured |  |
| `event_date` | date | no | measured |  |
| `country` | string | yes | measured |  |
| `country_code` | string | yes | measured | ISO 3166-1 alpha-2 |
| `region` | string | yes | measured |  |
| `category` | string | no | measured | must match CATEGORY_PRIORS keys |
| `severity` | double | no | measured | 0.0–1.0 AI-equivalent severity |
| `sentiment` | double | yes | measured | -1.0 to +1.0 tone estimate (None = neutral) |
| `phase` | int64 | no | measured | 1–5 execution phase |
| `model_score_current` | double | yes | measured | ── Computed scores ─────────────────────────────────────────────────────── Plan B: recomputed with current weights on each /api/backtest call |
| `model_components` | string | yes | measured | full component breakdown |
| `model_score_original` | double | yes | measured | Plan A: original stored score from events table if matched |
| `matched_event_id` | int64 | yes | measured | FK to events.id if matched |
| `human_score` | double | no | measured | 0–100 what model should score |
| `escalated` | bool | yes | measured |  |
| `market_impact` | string | yes | measured | none/low/medium/high |
| `contagion_spread` | bool | yes | measured |  |
| `severity_peak` | double | yes | measured | 0–100 actual peak severity |
| `timeframe_days` | int64 | yes | measured | days to peak escalation |
| `affected_countries` | string | yes | measured | ISO2 codes dragged in |
| `market_tickers` | string | yes | measured | assets that visibly moved |
| `outcome_source` | string | yes | measured | citation for outcome labels |
| `notes` | string | yes | measured | why this event was added / what gap it addresses |
| `source` | string | yes | measured | benchmark tag: FSI_divergence, GDELT_divergence, forecast_market_divergence, CDS_divergence, UCDP_divergence, severity_floor |
| `scored_at` | timestamp | yes | measured | ── Metadata ────────────────────────────────────────────────────────────── |
| `created_at` | timestamp | no | measured | When this row was first written by the pipeline. |

## `events_metadata`

Source table `events` · licence CC BY 4.0

Event METADATA only — timing, attribution, category, severity, credibility tier, cluster id, source domain and source URL, plus our own one-line summary. Headlines and feed summaries are third-party editorial text and are never redistributed; follow source_url.

`--since` filters this table on `ingested_at`.

| column | type | nullable | provenance | description |
|---|---|---|---|---|
| `id` | int64 | no | AI-assisted | Primary key of the source row. Stable across releases. |
| `occurred_at` | timestamp | yes | AI-assisted | When the event happened, as reported — the source's own publication timestamp. |
| `ingested_at` | timestamp | no | AI-assisted | When the pipeline first read the item. The gap to occurred_at is reporting lag, and it is uneven by country. |
| `country_code` | string | yes | AI-assisted | ISO 3166-1 alpha-2 code of the primary country. |
| `affected_countries` | string | yes | AI-assisted | Secondary countries beyond the primary one, as a JSON list of {country, region, weight, rule, attribution_type, confidence, evaluated_at}. attribution_type is 'direct' (a named party) or 'propagated' (a spillover rule). |
| `category` | string | yes | AI-assisted |  |
| `severity` | double | yes | AI-assisted |  |
| `credibility_tier` | int64 | yes | AI-assisted | 1-5 source credibility tier, resolved at export time from the source and the URL. 1 is the most credible. |
| `cluster_id` | int64 | yes | AI-assisted | Event clustering — events with the same cluster_id form a thread |
| `source_domain` | string | yes | AI-assisted | Host of source_url. Items routed through a news aggregator resolve to the aggregator's own host — that is the honest answer, not a guess at the publisher it masks. |
| `source_url` | string | yes | AI-assisted | Link to the original item. Headlines and article text are the publisher's; follow this URL and read their terms before reusing them. |
| `ai_summary` | string | yes | AI-derived | Our own one-line reading of the item, written by the enrichment model. This is not the feed's summary, which is never redistributed. |
