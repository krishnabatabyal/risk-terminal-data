# Scoring methodology changelog

This is the public record of material changes to the scoring methodology and the measurement pipeline. It covers every change up to the release cutoff of 2026-09-08. Every material scoring change bumps the `model_version` string stamped on the rows it produced. Weights, prompts and lexicons stay private, but their SHA-256 fingerprints (`weights_hash`, `pipeline_hash`) are published with every row and listed in the register at the end. Entries are added when a release first carries rows they describe.

Disclaimer: this is not a prediction product. All scores, readings and analysis are based on current conditions.

## Scoring-pool scope — 2026-09-08 — Office-change events excluded from the event pool

**What changed.** Model version unchanged (`scorer-v5.0.1`). No stored score moves. The people pipeline now writes wire events when a public knowledge base records an appointment, departure or death for a head of state or government, a minister, or a senior security office. These events carry the category `appointments` and the lowest-weight credibility tier. They appear on the wire and are available to briefs, but they are not scoring inputs: the single eligibility clause that every scoring event-pool query uses now excludes that source. The exclusion list is part of the parameter fingerprint, so the change is stamped on every score from this release on (weights hash `5f0a54876c21a64413f05a5a3a548a1b3d14595ac12fb883b15b0495e2f8ca67`).

**Why.** These events are derived records of who holds office, not news pressure. A new derived source entering the pool part-way through the observation window would change what the series measures. Nothing about how a scored event is priced changes, so this is a scope constant, not a weight.

## Taxonomy and attribution repair — 2026-09-07 — Political-family split and three country misattributions

**What changed.** Model version unchanged (`scorer-v5.0.1`). No stored score moves, and no historical event or score was altered or backfilled.

1. The catch-all `political_development` category carried 37.5% of a 40-event audit sample. The enrichment step now offers three siblings: `diplomacy` (between states), `domestic_politics` (inside one state) and `appointments` (who holds which office), with `political_development` redefined as the residual. All four categories reference one shared prior object, so an identical event scores identically whichever of the four the classifier picks; this is asserted across the severity and tone grid. Every downstream rule that named the parent (spillover rules, leadership-shift and election detection, cluster typing, driver grouping) now names the family. Stored rows keep `political_development`, and the API category filter treats the parent as a group that returns the parent plus the three children. Previously orphaned labels were deliberately not folded into the family, since that would be a scoring change.
2. Country attribution had three root causes. A class of monitoring agencies is named for its host city but covers an ocean-sized region (the volcanic ash advisory centres), so agency names are now blanked before the keyword scan; the same city named elsewhere still counts. Demonyms were missing for about 55 major countries and are now backfilled under a minimum-length rule and a homograph exclusion list, with fixed collocations added to the negative patterns. The keyword scan now runs on the title first and falls back to title plus summary only when the title names no country, so a passing body mention can no longer outrank the headline subject; suppression and corroboration rules still see the full text. A sub-national table for Hawaii, Alaska and the Pacific territories closes a gap where the same storm resolved to the US or to no country depending on the place name used. It is deliberately not a general US-city dictionary.

**Why.** A sharper taxonomy makes category filters and explainers useful, and the attribution errors placed events on the wrong country. The enrichment version moved from `enrich-v1.1` to `enrich-v1.2`. Both fingerprints move (weights `f7d18360db8cd38da3792d11af7e96ed659435b938eb836484b75c83343fb7b9`, pipeline `118745d7e2b28cb3f604418675fe55f5a422a135af8c6492f06e7eff60787248`) because the apparatus changed shape; the numeric effect on any event, past or future, is zero. The prompt change applies only to events ingested after release.

## Data-input repair — 2026-08-23 — UCDP candidate-release month mapping

**What changed.** Model version unchanged (`scorer-v5.0.1`). The fix is in ingestion, not the scoring engine, and is logged here because it moves conflict floors inside the observation window. An earlier backfill assumed candidate release `YY.0.MM` covers event month MM-2 or MM-3. It covers month MM itself (about 99% of rows, checked against all 19 releases from 25.0.1 to 26.0.7). Each cycle the job re-fetched six already-stored releases, used up its row budget, stored nothing and never reached the steady-state fetch, so the newest stored conflict event froze at 2026-05-31. The fix maps the release for hole month M to `YY.0.M`, raises the hole threshold from 100 to 1,000 rows (real months run 1,280 to 2,550), fetches three whole releases per cycle under a 9,000-row budget, aligns the trailing-count window to 13 whole months, and falls through to the steady-state fetch when the hole fetch returns nothing.

**Why.** While broken, every conflict floor was attenuated by `0.5^((lag-60)/180)` (0.912 on 2026-08-23) on top of an under-counted trailing 12-month window. Measured against complete data, the Ukraine floor read 85.0 versus 97.5 (42.7k versus 92.1k deaths), Iran 69.7 versus 89.9 (3.7k versus 23.6k, with the January 2026 war month absent), and Israel 69.8 versus 78.3. After the backfill, floors step up for active-war states (Ukraine toward the floor ceiling near 95, Iran toward 90, Israel largely unchanged because it is event-driven). This is a dated input-data correction, not drift. The pre-floor short-term reading is unaffected.

## scorer-v5.0.1 — 2026-08-05 — Baseline attenuation removed, theater flag scoped, historical-headline guard

**What changed.** Version `scorer-v5.0` to `scorer-v5.0.1`, from a full audit of all 200 entities.

- The evidence-attenuation rule on the structural baseline floor was removed. It pulled the baseline toward the engine score by `direct_event_count/5` for countries with 1 to 4 direct events but exempted the zero-event case, so the applied baseline was discontinuous at the 0-to-1 event boundary and non-monotone across 0 to 5. One wire mention entering or leaving the window moved zero-coverage scores by 11 to 20 points in a week (Eritrea +18.3, Comoros -18.3, Maldives -20.4, Nauru -11.1). The baseline now applies at full strength and moves only with its own structural inputs (governance indicators, 365-day conflict data, displacement data). Measured against stored components, 23 countries rise to their full structural floor (mean +5.7, max +20.5, min +0.8; all upward; mostly micro-states and chronically quiet states). Hard derived floors were never attenuated and are unchanged. The removed threshold was a literal never covered by the parameter fingerprint, so this version bump is the stamp for the change.
- The `theater_uncorroborated` annotation now requires an actual claim (at least one direct own-soil war-class event) that lacks corroboration. It had fired on 135 of 200 countries. Reporting only; scoring gates are untouched.
- The top-contributors display drops fully decayed zero-weight events. Display only.
- Both enrichment prompts now bar historical, retrospective or commemorative pieces and metaphorical kinetic language from live kinetic categories, and the rules path suppresses old-war references with no hard-news anchor. Trigger cases were a piece on wartime munitions found off a Pacific island (scored as `conflict` 47.8, moving that country +18.7 as its only event) and a metaphorical "constitutional coup" essay (scored as `coup` 58.1). Applies to newly enriched events only; stored events are never re-enriched or deleted.

**Why.** Floors were producing event-speed motion on zero-coverage states, a decomposition flag had lost its meaning at n=135, and relic or essay headlines inflated micro-state scores. After release, baseline-pinned countries move near-frozen week to week.

## scorer-v5.0 — 2026-07-21 — De-magic-numbering, data-derived geo-exposure, steeper fatality curve, struck-location attribution

**What changed.** Version `scorer-v4.2` to `scorer-v5.0`. Weights fingerprint `2b29d791…` to `7bdda525ebb44cf4b79ee2fa71ffe92d7488e7520ba5f23e018786a0a5687e63`. The fingerprint was extended to cover every v5.0 parameter that lives outside the core scoring tables (geo-exposure tunables and alignment tables, war-exposure fraction and regimes, the proxy and spillover prior layer, job-layer governance, fragility and spillover constants, and the new fatality anchors). Earlier claims that the fingerprint covered the full parameter set were incorrect for those constants; this release makes them true. A determinism bug was also fixed: set-valued constants were serialized in hash-seed-dependent order, so the fingerprint varied by process. Sets are now sorted, and the hash is stable across restarts and machines.

1. Governance modifier is continuous: `gov_bonus = 7.5 · (1 − 2·Φ(WGI_political_stability_percentile))`, where 7.5 is half a 15-point band and Φ is the standard-normal CDF. The median country gets 0, the worst-governed tail +7.5, the best -7.5. Fragile-but-quiet states with no conflict corroboration keep 0.4 of the premium.
2. Ladder anchor floors are derived from the band edges (80/65/50) instead of eight hand-tuned rungs. Conflict and war rungs floor at Critical, terrorism at the midpoint of High and Elevated.
3. Target-fitting was retired: ten named-country governance overrides and six proxy weights fitted to specific Gulf scores were deleted, verified score-neutral.
4. Fatality curve anchors (battle deaths to floor): 25 to 50, 1,000 to 65, 10,000 to 85 (was 80), 100,000 to 98 (new catastrophe tier).
5. War-floor exposure = `proximity · (neutral_share + (1 − neutral_share) · max(alignment, energy))`. Proximity combines a maritime-adjacency table (0.90) with haversine decay (half-life 1,400 km). Alignment combines UN voting ideal-point distance, treaty blocs and hosted foreign bases. Neutral share is 0.5, the maximum exposure fraction is 0.65, and the war floor is now a hard floor.
6. Expeditionary filter: war-theatre rungs require the country's own on-soil evidence plus a per-event target-country match, so overseas belligerence no longer inflates a home score. Live kinetic exposure bypasses the governance ceiling.
7. Kinetic spillover to neighbours = neighbour level × 0.55, where level is the greater of the fatality floor and the conflict-probability baseline on the Elevated-to-High band.
8. Struck-location attribution: the enrichment prompt sets `target_country` to the soil where a kinetic event physically occurred, and scoring injects that event into the struck country's pool, deduplicated by cluster. Jordan moved 60 to 77 after troops were killed on its soil.
9. Fixes: a shock ramp replaces a severity cliff at 0.90, a floor-scale correction in the inverse-logistic bound, a clamp on future-dated events, direct-only maximum signal contribution, and a bug that stripped the primary country from its own affected-country list (which had depressed Sudan, Yemen, Ethiopia and DR Congo).
10. `economic_crisis` moves to a 21-day half-life class, since currency collapse and default persist for months.

**Why.** To remove hand-set numbers from the formula and make any weight change cryptographically detectable. In a dry run, 22 to 28 countries moved by 2 points or more. The Middle East region moved 78.3 to 81.5 (into Critical); Gulf states rose (UAE 40 to 63, Qatar 36 to 57, Saudi Arabia 53 to 68, Bahrain 62 to 69) and the US home score fell. The population-weighted global figure moved 61.8 to 61.2.

**Registered deviation.** This release is recorded as a deviation from the pre-registered protocol. A memory-epoch rebaseline dated 2026-07-21 filters the 120-day-half-life tension-memory average to post-freeze scores, correcting accumulated hysteresis (for example, the US memory component read 77.4 against a 24.8 structural baseline). No historical scores or events were deleted. Pre-v5.0 and post-v5.0 series should be analysed as two regimes. The expeditionary and strike-injection mechanisms fire only where enrichment populated `target_country` (about 8 to 16% of kinetic events at release, rising), so behaviour drifts as that coverage grows.

**Known residuals.** India's monsoon flooding volume plus one casualty event lifts it into the top seven. Mali's persistence floor, governance override and memory stack place it above Sudan on thinner evidence. The earlier hold-out validation figure (mean absolute error 0.15) is retired as a non-test: it is a small single-category set that the deterministic formula reconstructs near-tautologically, and the integrity endpoint now reports that it is not a generalization estimate.

## enrich-v1.0 — 2026-07-09 — Provenance lockdown (no scoring change)

**What changed.** No scoring behaviour changed; the deployed model version at this date was `scorer-v4.0`. This entry introduces a separate version axis for the enrichment pass, `enrich-v1.0`, bumped on every material change to the enrichment prompt, lexicons, gates or pinned model, with a dated entry here.

- The enrichment model default moved from a floating alias to a dated snapshot, so the recorded model id is reproducible. Prompt text, lexicons, gates and temperature (0) were unchanged.
- An append-only archive stores the verbatim model output of every bulk-enrichment call (success and parse failure) before parsing, with prompt hash, enrichment version, batch ids and token counts. A failure to archive can never cost an enrichment.
- The enrichment version is persisted on every event and archive row, so a prompt or lexicon change is detectable even when the model id is unchanged.
- A daily measurement-regime series records total events, model-enriched versus rules-only counts, coverage, and the share of countries decided by floor versus engine versus engine-within-3-points. Reporting only.
- The published score thresholds were corrected from a stale 80/60/40/20 ladder to the 80/65/50/35 ladder the engine has always used. No boundary in the engine moved.

**Addendum, 2026-07-11.** A pipeline fingerprint was added. The weights hash covers only the scoring engine's numeric constants, so the measurement pipeline upstream (the enrichment prompts, the pinned model id, and the rules-path lexicons and gates) could change while `weights_hash` held still. `pipeline_hash` is a SHA-256 over the weights fingerprint, both prompt hashes, the model id, the enrichment version and a canonical hash of the rules-path lexicons, and it moves when either the engine or the pipeline changes. The weekly per-country explainer job, which previously overwrote one row per country, now also appends an immutable history row carrying score, drivers, model, and both fingerprints.

**Why.** Every published value should be attributable to the exact parameter set and pipeline that produced it.

## scorer-v4.2 — 2026-07-14 — Contagion-layer signals, locality-gated theater channel, enrich-v1.1

**What changed.** Scoring `scorer-v4.1` to `scorer-v4.2` (weights fingerprint `2b29d791dbb5aae81177fe4abda829dc4ffd79211c77948e412e4e04cc0d93ba`) and enrichment `enrich-v1.0` to `enrich-v1.1`. All constants are global formula values with a-priori coefficients, each decomposable under its own modifier key, none tuned to external indices or the hold-out set.

- A latent defect in the v4.1 release deleted a constant that the ladder-floor code still used, which stopped every hourly scoring run for about 19 hours after deployment. The definition was restored. Scores in that gap are absent, not wrong, and continuity accounting for the window must count the outage. The intermediate v4.1 fingerprint therefore never appears on a stored row.
- Four contagion signals: crowd-size log scaling of protest intensity (dormant until a crowd-size field exists); an asymmetric-Gaussian election-proximity curve peaking about 45 days before the poll (pre-sigma 55, post-sigma 25, cap 12 points, replacing a flat linear ramp); a macro economic-stress signal from inflation, growth, debt and current-account bands (cap 8); and a structural displacement-per-capita level signal (cap 6, saturating at 10% of population displaced). Each is a no-op where data is absent, and the caps keep all of them secondary to conflict. Displacement data is annual, so this is a level signal, not a velocity.
- Theater fast-corroboration channel, locality-gated: at least 3 war-class kinetic events in 7 days, each scoring 55 or more from at least 2 sources, and each with a persisted target country equal to the scored country. It runs only when conflict data does not already corroborate and fails closed on missing target data. Validation on production pools: Qatar's three on-soil missile events fire it, while the US pool (234 war-class events, all targeting Iran abroad) does not.
- Enrichment now persists the resolved target-country ISO code on each event.
- Statement attribution: when a title matches a statement verb, the extracted target resolves to a different country, and the category is event-located, the primary country becomes the target, the speaker drops to a 0.3-weight `statement_actor` entry, and severity caps at 0.45. A UAE statement condemning a bombing in Damascus now attributes to Syria, and one calling for a ceasefire in Sudan attributes to Sudan. Bilateral gates require a direct attribution at weight 0.6 or more, so a statement actor can never read as a war party.

**Why.** Scores should reflect where violence occurs rather than who comments on it, and secondary stress channels should be present but bounded.

## Input expansion — 2026-07-14 — Wire breadth and cross-provider dedup (no model change)

**What changed.** Source additions only; the formula, weights, floors and enrichment pass are untouched, and neither fingerprint moves. About 39 additional political and economic-crisis query terms (martial law, capital controls, mutiny, disputed election and others) plus Russian- and Spanish-language query variants were added to the global event feed, and the active-query cap rose from 60 to 100. A second, narrower dedup gate (same country, 48-hour window, title similarity of 0.58 or more) collapses one real-world event reported independently by several providers, keeping the highest-credibility source as canonical. Conflict-dataset records are exempt.

**Why.** More and cleaner events enter the same formula, particularly for undersampled small states and non-English media regions, while correlated double-counting no longer reads as independent corroboration. The daily measurement-regime series records the volume and coverage step from this date.

## scorer-v4.1 — 2026-07-13 — Maritime spillover adjacency and de-escalation negation guard

**What changed.** Two fixes from a Gulf scores audit (Qatar read 36, Moderate, while intercepting missiles). Both are global, fingerprint-covered and decomposable.

- Maritime adjacency for the kinetic spillover floor. The floor had read land borders only, so island and peninsular states facing a war-grade neighbour across a narrow strategic waterway got no spillover (Qatar and Bahrain versus Iran). A geographic fact table now adds populated coasts within about 250 km across an enclosed or strategic waterway, excluding open-ocean technicalities, with the same probability tiers as land borders. Qatar and Bahrain gain the neighbour spillover floor of 45 immediately.
- De-escalation negation guard. A de-escalation headline that is actually about the de-escalation failing ("ceasefire violations continue", which had given Palestine a false -4.5 credit) no longer earns a stabilisation credit; it re-scores as neutral `political_development`. "Ceasefire violations continue" now scores +48.3 and "ceasefire agreement signed" still scores -12.0.

**Investigated and not shipped.** A fast channel for newly attacked countries was prototyped as at least 3 kinetic events scoring 55 or more in 7 days from at least 2 high-tier sources. It failed validation in both directions: aggregator URL masking resolves most live war reporting to a mid tier, so it never fired on the motivating case, and country pools carry no locality, so any loose enough trigger would reopen the power-projection hole closed in v4.0. The locality-based version shipped in v4.2.

**Why.** Conflict-adjacent states across water were invisibly exempt from spillover, and failed ceasefires were earning stabilisation credit.

## scorer-v4.0 — 2026-07-02 — The autonomy overhaul (derived floors, no human numbers)

**What changed.** All hand-set per-country values were deleted: the situational floor table (39 entries), the conflict-floor country list (8), the nuclear-state list, the chokepoint belligerent set, and analyst score overrides of up to 50 points. They were replaced by a derived floor stack: a conflict battle-death floor anchored to the dataset's own armed-conflict and war definitions and mapped to band edges; a tension-memory floor (120-day half-life exponential average over pre-floor engine output, with the raw engine score persisted per row); a continuous conflict-probability floor (probability × 50); and a nuclear-posture floor mapped to band edges. A dry run showed the battle-death mapping independently reproduces the deleted hand values from data. A theater corroboration gate requires on-soil conflict evidence for war-class ladder rungs and the kinetic persistence trigger, since belligerence abroad is not domestic risk (US 72.5 to 55.0, China 75.4 to 57.5; war zones unchanged). The conflict data feed was repaired after an 18-month silent outage caused by a fixed-window fetch against a publication lag, with staleness alarms and floor attenuation added. The weights fingerprint was extended to cover ladder and chokepoint tables and all derived-floor constants, and the SHA-256 is now stamped on every score row and exposed on the public integrity endpoint.

**Why.** The engine must run without analyst-given numbers, and every parameter change must be cryptographically detectable. About 40 countries moved off hand values onto derivations, with the transition bridged by the memory floor while conflict backfill matured. Weights hash `eeb2d3581732f9f3b91788eb5947bd1b0c33c08a9a458e0b281d42708311bea2`.

## scorer-v3.2 — 2026-04-07 to 2026-04-23 — Audit fixes, credibility tiers, GDELT tone

**What changed.** Wire tone became a sentiment modifier; categories expanded from 19 to 29; double-logistic, eigenvalue clamp and tone-calibration fixes landed; and a 5-tier source credibility multiplier with 167 source mappings was added (low-credibility social sources 0.7x, state-propaganda outlets 0.5x). Fifteen audit bugs were fixed, chiefly spillover dominance (Kuwait outscoring Israel): spillover countries can no longer outscore conflict parties, per-theater adjacency and a two-tier logistic were added, a direct-event floor prevents spillover dilution (Bahrain 34 to 85), spillover has a ceiling and a structural-only mode, and conflict-intensity damping by `sqrt(event_count/50)` is gated on direct events. A further sprint added a quiet floor, a channel cap, asymmetric governance weighting and a 20% cap on spillover share, plus organized-crime weights. The string `scorer-v3.2` with calibration date 2026-04-23 was introduced and stamped on every score row.

**Why.** Spillover dominated direct scores, and sources of unequal reliability carried equal weight. Conflict parties re-ranked above neighbours.

### Maintenance within scorer-v3.2 (no version bump)

- **2026-05-04 to 05-09.** Decay normalisation with a signal-preservation floor (0.70), a logistic-bound fix, credibility by domain, a dual-row fix for one country, a persistence floor on absolute kinetic count, and a region depth-of-crisis blend (sigmoid on the count of countries at 75 or above; Middle East 75.8 to 80.2). War scores stop sagging between news cycles.
- **2026-05-19 to 05-26.** Engine attribution filters (two bias fixes), conflict floor suppressed on stable democracies, component caps clamped at source, ladder-anchor floors so active war reads 80 or above, several sum gates reverted where they starved Ukraine and Israel, situational floors for about 21 states with African attribution rules and a subject-classifier gate, a governance ceiling that caps event-driven noise in high-governance states (bypass scoped to kinetic exposure only), and unified score bands with country-name canonicalization. Misattributed events stopped inflating bystanders and duplicate-row aliases were eliminated.
- **2026-06-01 to 06-11.** A baseline-attenuation fix, brief-derived signals made load-bearing, cluster deduplication before the weighted mean, a split of the headline into short-term and structural components, and ladder-anchor floors that now decay with their underlying evidence. Floors become derived and self-expiring.

## scorer-v3.1 — 2026-04-03 — financial_warfare category and explainability

**What changed.** A new `financial_warfare` category (payment-network exclusion, reserve immobilisation) with a 21-day half-life, separated from `sanctions`; score-movement explainability ("why this score", "why it moved").

**Why.** Weaponised monetary-system attacks differ qualitatively from trade sanctions (a payment-network exclusion at severity 0.98 scores 91, versus a trade embargo at 0.33 scoring 46). Backtest error for the category is about 0.01.

## scorer-v3.0 — 2026-04-02 — Methodology remediation

**What changed.** De-escalation architecture (10-day half-life, credit capped at 25 points), a severity exponent of 0.7, and sanctions and trade priors recalibrated against backtest phase 9 (sanctions sum 71 to 56, trade 60 to 49).

**Why.** A scoring audit found 10 structural issues, including category-level bias (+10.9 average on sanctions, +7.7 on trade) and no mechanism for scores to fall on verified de-escalation. Sanctions-event error fell 10.10 to 5.68 and trade 7.50 to 4.27.

## scorer-v2.2 — 2026-03-26 to 2026-03-30 — Backtest system and first calibration

**What changed.** A backtest harness over seeded historical events, post-backtest recalibration of category priors, a reduced region anchor, an authoritative region map with a conflict persistence floor, and nuclear scoring and proxy propagation fixes. Coup events were de-biased.

**Why.** First systematic validation against known historical outcomes.

## scorer-v2.1 — 2026-03-24 to 2026-03-25 — Systemic event layer

**What changed.** `financial_crisis` and `pandemic` categories with a 45-day half-life, a global shock floor, a `systemic_shock` component capped at 20, a four-layer war-escalation floor architecture with a systemic war trigger, and war-zone scoring fixes.

**Why.** Pandemic- and financial-crisis-class events have multi-month trajectories and global transmission, and a 5-day half-life erased them in two weeks. Systemic events now score about 85 to 90 and persist about three months; war-adjacent countries receive exposure floors.

## scorer-v2.0 — 2026-03-24 — Decay overhaul

**What changed.** Continuous exponential decay (5-day half-life), a logistic cap, and market sensitivity decoupled from the geopolitical total to avoid endogeneity, followed by a weight calibration pass.

**Why.** Scores were dominated by stale events and the linear cap saturated. Quiet countries mean-revert faster and the top end is smoother.

## scorer-v1.0 — 2026-03-15 — Initial engine

**What changed.** The first scoring engine: event scores from weighted subfactors with simple country aggregation, recalibrated shortly afterward for realistic conflict scores.

**Why.** Launch baseline. It establishes the 0 to 100 scale.

## Fingerprint register

Every `weights_hash`, `pipeline_hash` and `model_version` that appears in a shipped release, with the span it was observed over. Entries are appended, never rewritten.

| kind | value | first seen | last seen | rows | model version |
|---|---|---|---|---|---|
| weights_hash | `eeb2d3581732f9f3b91788eb5947bd1b0c33c08a9a458e0b281d42708311bea2` | 2026-07-03 | 2026-07-13 | 2,211 | scorer-v4.0 |
| weights_hash | `2b29d791dbb5aae81177fe4abda829dc4ffd79211c77948e412e4e04cc0d93ba` | 2026-07-14 | 2026-07-21 | 1,608 | scorer-v4.2 |
| weights_hash | `7bdda525ebb44cf4b79ee2fa71ffe92d7488e7520ba5f23e018786a0a5687e63` | 2026-07-22 | 2026-09-06 | 9,447 | scorer-v5.0.1 |
| weights_hash | `f7d18360db8cd38da3792d11af7e96ed659435b938eb836484b75c83343fb7b9` | 2026-09-07 | 2026-09-07 | 201 | scorer-v5.0.1 |
| weights_hash | `5f0a54876c21a64413f05a5a3a548a1b3d14595ac12fb883b15b0495e2f8ca67` | 2026-09-08 | 2026-09-08 | 201 | scorer-v5.0.1 |
| pipeline_hash (measurement_regime_daily) | `7fc6b7e2ed195209ab5c1bd0d8a23f33f49e880e9026de04600b728145252dbc` | 2026-07-11 | 2026-07-13 | 3 | — |
| pipeline_hash (measurement_regime_daily) | `7781e1878b784ef0ce298e7c1ad8e17c1dfadfd76ff0179c5ba1eb0efeafc158` | 2026-07-14 | 2026-07-21 | 8 | — |
| pipeline_hash (measurement_regime_daily) | `34e965c481c622a0773bc43080019c938b21e70261e1aa0c548569368f6f935b` | 2026-07-22 | 2026-08-04 | 14 | — |
| pipeline_hash (measurement_regime_daily) | `2875e622b819663fc4d5e9ea511f376bf921a190f884592616d7c85d2f06b635` | 2026-08-05 | 2026-09-06 | 33 | — |
| pipeline_hash (measurement_regime_daily) | `118745d7e2b28cb3f604418675fe55f5a422a135af8c6492f06e7eff60787248` | 2026-09-07 | 2026-09-07 | 1 | — |
| pipeline_hash (score_explainer_history) | `7781e1878b784ef0ce298e7c1ad8e17c1dfadfd76ff0179c5ba1eb0efeafc158` | 2026-07-19 | 2026-07-19 | 200 | — |
| pipeline_hash (score_explainer_history) | `34e965c481c622a0773bc43080019c938b21e70261e1aa0c548569368f6f935b` | 2026-07-26 | 2026-08-02 | 400 | — |
| pipeline_hash (score_explainer_history) | `2875e622b819663fc4d5e9ea511f376bf921a190f884592616d7c85d2f06b635` | 2026-08-09 | 2026-09-07 | 894 | — |
| weights_hash (score_explainer_history) | `2b29d791dbb5aae81177fe4abda829dc4ffd79211c77948e412e4e04cc0d93ba` | 2026-07-19 | 2026-07-19 | 200 | — |
| weights_hash (score_explainer_history) | `7bdda525ebb44cf4b79ee2fa71ffe92d7488e7520ba5f23e018786a0a5687e63` | 2026-07-26 | 2026-09-07 | 1,294 | — |

Row counts per model version:

| table | model_version | rows |
|---|---|---|
| `country_scores` | `scorer-v3.2` | 8,079 |
| `country_scores` | `scorer-v5.0.1` | 7,035 |
| `country_scores` | `scorer-v5.0` | 2,814 |
| `country_scores` | `scorer-v4.0` | 2,211 |
| `country_scores` | `scorer-v4.2` | 1,608 |
| `subnational_scores` | `subnational-v1.0` | 85,500 |

`subnational-v1.0` covers the admin-1 sub-national readings. `scorer-v4.1` never reached a stored score row (see the `scorer-v4.2` entry).
