# Changelog

Releases are immutable. A release is never edited after publication; a
correction ships as a later release with a note here saying what changed and
why.

## rt-data-2026-09 — 2026-10-15T12:57:02+00:00

- Cut with `rt-release-builder/1.1`. Builder commit: 6a4b8b5a.
- 18 tables, 36 data files, 531,648 rows.
- `--since` filter applied to this cut: none (full history).
- Cutoff (`--until`, exclusive) applied to this cut: 2026-09-08T01:27:06+00:00.
- Current scoring model version at build time: `scorer-v5.0.3`.
- Fingerprints present in this cut:

- **Model versions:** `scorer-v3.2`, `scorer-v4.0`, `scorer-v4.2`, `scorer-v5.0`, `scorer-v5.0.1`, `subnational-v1.0`
- **Parameter fingerprints (`weights_hash`):** `2b29d791dbb5aae81177fe4abda829dc4ffd79211c77948e412e4e04cc0d93ba`, `7bdda525ebb44cf4b79ee2fa71ffe92d7488e7520ba5f23e018786a0a5687e63`, `eeb2d3581732f9f3b91788eb5947bd1b0c33c08a9a458e0b281d42708311bea2`, `f7d18360db8cd38da3792d11af7e96ed659435b938eb836484b75c83343fb7b9`
- **Pipeline fingerprints (`pipeline_hash`):** `118745d7e2b28cb3f604418675fe55f5a422a135af8c6492f06e7eff60787248`, `2875e622b819663fc4d5e9ea511f376bf921a190f884592616d7c85d2f06b635`, `34e965c481c622a0773bc43080019c938b21e70261e1aa0c548569368f6f935b`, `7781e1878b784ef0ce298e7c1ad8e17c1dfadfd76ff0179c5ba1eb0efeafc158`, `7fc6b7e2ed195209ab5c1bd0d8a23f33f49e880e9026de04600b728145252dbc`

### Values withheld in this cut

Rows ship; these individual values are set to null.

- `backtest_events.outcome_source`: 136 citation segments naming such an organisation removed.
- `elections.opposition_note`: 3 forward-looking wording.
- `elections.risk_note`: 6 forward-looking wording.
- `events_metadata.ai_summary`: 170 names an organisation the release does not reference; 37,457 never read by the enrichment model (the text was the cleaned headline); 2,472 ends in a publisher suffix, i.e. a syndicated headline; 41 a raw social-media fragment; 7,259 a copy or near-copy of the source headline.
- `events_metadata.source_url`: 2 names an organisation the release does not reference.
- `leaders.ai_summary`: 5 forward-looking wording.
- `leadership_events.detail`: 40 names an organisation the release does not reference; 295 ends in a publisher suffix, i.e. a syndicated headline; 1 a raw social-media fragment; 1,213 a copy or near-copy of the source headline.
- `score_explainer_history.key_drivers`: 3 forward-looking wording; 1 names an organisation the release does not reference.
- `score_explainer_history.summary`: 16 forward-looking wording; 2 names an organisation the release does not reference.

Withheld for wording (row ids, value set to null):

- `elections.opposition_note` (3): 148, 181, 238
- `elections.risk_note` (6): 117, 122, 156, 188, 239, 253
- `leaders.ai_summary` (5): 94, 142, 183, 213, 222
- `score_explainer_history.key_drivers` (3): 214, 478, 1493
- `score_explainer_history.summary` (16): 243, 419, 425, 480, 778, 848, 854, 955, 1028, 1075, 1108, 1201, 1223, 1516, 1538, 1564

### Methodology changes

Model methodology has its own versioned changelog,
`METHODOLOGY_CHANGELOG.md`, shipped inside this release. Every material
change to the scoring methodology bumps `model_version`, and that string is
stamped on the rows it produced, so the changelog and this panel can always be
read against each other. `verify_release.py` checks that every version and
fingerprint in `MANIFEST.json` appears in that changelog.

This file records what happened to the *release*: what was cut, when, and from
where. It does not restate the methodology.
