# TOMPECS version: structure, provenance, and open items

The TOMPECS manuscript is `tompecs/` on `main` (which Overleaf syncs); the original ACL-style paper is
kept, unedited, in `sections/` and `main.pdf`. The `tompecs` branch on the remote is stale.

## What was verified about the venue, and how sure we are

| fact | source | confidence |
|---|---|---|
| Use `acmart` with format `acmsmall`; the journal macro is `\acmJournal{TOMPECS}` | the acmart user guide (CTAN `acmguide.pdf`), Table 1 and the journal-abbreviation table | read directly |
| Review copy: `\documentclass[acmsmall,review]{acmart}`; `anonymous` hides authors | same guide | read directly |
| CCS concepts and keywords are required for articles over two pages | same guide | read directly |
| Length limit: 30 pages in ACM Transactions style; badly formatted or over-length papers may be returned without review | a search result quoting the journal's author-guidelines page | **secondhand**: the ACM page itself returns 403 to automated fetch; confirm on the page |
| Submission through Manuscript Central (`mc.manuscriptcentral.com/tompecs`); cover letter must explain fit with scope and any earlier versions or parallel submissions; ORCID required for submitting authors | same search result | **secondhand** |
| Scope: modeling, analysis and performance evaluation of computing and communication systems; topics include measurement/instrumentation, statistical analysis, verification and validation, workload characterization | a 2014 launch announcement and listing pages | secondhand and old |
| Whether review is single- or double-blind; whether references count toward the 30 pages; artifact policy | not found | **unknown** |

## Structure (since 2026-10-29)

On 2026-10-29 the manuscript was restructured a second time, to the reviewer's outline
(introduction / methodology / experimental setup / results / discussion / related work / conclusion),
with one subsection per experiment in Sections 3 and 4. The old section files were deleted (git keeps
them; the previous layout is commit c95638e). All old labels are kept on the matching new heading, so
cross-references still resolve.

| new section | file | label(s) | built from (previous TOMPECS layout) |
|---|---|---|---|
| 1 Introduction | `01_introduction.tex` | `sec:intro` | old 1, plus a plain definition of gaming; contributions restated with the per-variant counts of Table 1 |
| 2 Methodology | `02_methodology.tex` | `sec:method`; 2.1 `sec:subject`, 2.2 `sec:profdata`, 2.3 `sec:promptstructure`, 2.4 `sec:ablation`, 2.5 `sec:constraint`, 2.6 `sec:correctness`, 2.7 `sec:timing` | old 3 (pipeline, profiling data, prompt), 5.1 (variants), 6.2 (constraint text), 4.3-4.5 and 7.2-7.3 (gates, timing, conventions), the arm definitions of 8.1/8.2 |
| 3 Experimental Setup | `03_setup.tex` | `sec:setup`; 3.1 `sec:explanation`, 3.2 `sec:models`, 3.3 `sec:hardware`, 3.4-3.8 `sec:setup-e1` .. `sec:setup-e5` | old 4.1-4.2, 7.1 (`tab:apps`), and the setup paragraphs of 5-8 |
| 4 Results | `04_results.tex` | `sec:results`; 4.1 `sec:prompts` (+`sec:gaming-obs`), 4.2 `sec:intent`, 4.3 `sec:realapps`, 4.4 `sec:evidence`+`sec:profabl`, 4.5 `sec:guidvar` | old 5.2-5.3, 6, 7.4, 8.1, 8.2 (results only) |
| 5 Discussion | `05_discussion.tex` | `sec:discussion`; 5.1 `sec:analysis`, 5.2 `sec:gaming-disc`, 5.3 `sec:whatmodels`, 5.4 `sec:profdisc`, 5.5 `sec:bva`, 5.6 `sec:pitfalls`+`sec:defects`, 5.7 `sec:limits` | old 5.3 (as a list), 6.2 detection, 7.4 (optimization details), 8.1-8.2 interpretation, 9, 10 (condensed) |
| 6 Related Work | `06_related.tex` | `sec:relatedwork` | old 2, rewritten in plainer language; reward hacking defined |
| 7 Conclusion | `07_conclusion.tex` | `sec:conclusions` | old 11 |

New material in that restructure (all marked `% EDIT (2026-10-29)` or `% NEW`):

- `figures/pipeline.tex`: a TikZ workflow figure (`fig:pipeline`), drawn from `src/opal_cli_codex.py`.
  **Never compiled**: no LaTeX here, and the cluster's TeX install lacks font metrics. If the Overleaf
  build fails, look here first; `main.tex` loads `tikz` with `arrows.meta,positioning,calc`.
- `tab:prompt`: the prompt region by region with the text as sent (from
  `src/results/atan2-codex-gpt5-cot/atan2_pc+rl_gpt5_cot_prompt_1.txt`).
- `tab:variants`: which regions each variant carries (ticks/crosses; `\cmark`/`\xmark` in `main.tex`).
  Derived by diffing the saved prompts of each variant. This corrected two earlier descriptions:
  `no_constraints` removes only the six rules written as "Do NOT" (rules 9-11 and entry-point
  guardrails 2, 3, 5), not the signature/rename rules; `minimal` keeps the hardware guidance and the
  entry-point guardrails. `no_role` removes the hardware-guidance paragraph; the one-line persona is a
  system message present in every variant.
- `tab:variantsum`: per-variant first-attempt, timed-result and slowest-valid counts, read off Table 1.
- Variant order everywhere (Tables 1, `tab:variants`, Section 2.4): minimal, no_role, no_constraints,
  no_proof, no_explanation, cot (least to most populated).
- Section 3.2 states that Gemini 2.5 Pro was disabled on the API after E1 (the author's statement in
  the 2026-10-29 review; not documented in the experiments repo).
- `tab:intent` header rebuilt; `tab:realapps` caption defines the arms; "pedantic" removed; "drift"
  defined before use and the 49% clarified (same unmodified binary, two sessions).
- The measurement protocol is stated once (2.7) and only referenced elsewhere.

### Previous TOMPECS layout (2026-10-22 to 2026-10-29), for reading older commits

| section | label | built from (ACL files) |
|---|---|---|
| 1 Introduction | `sec:intro` | `introduction` + research questions |
| 2 Background and Related Work | `sec:relatedwork` | `relatedWork` |
| 3 The Optimization Pipeline Under Study | `sec:subject` | `methodology`: Pipeline, Profiling data, Prompt structure |
| 4 Experimental Methodology | `sec:method` | `experiments` + `methodology`: Workload selection, Correctness, Timing + Reporting Conventions |
| 5 Prompt-Component Study | `sec:prompts` | `ablation`, `results`, `analysis` |
| 6 Benchmark Validity | `sec:intent` | `analysis`: Benchmark gaming + `semantic_constraint` |
| 7 Production Applications | `sec:realapps` | `realapps` minus the defects subsection |
| 8 The Value of Profiling Evidence | `sec:evidence` | `profile_ablation`, `guidance_variance` |
| 9 Evaluation Pitfalls in Practice | `sec:pitfalls` | summary table + `realapps` defects + `analysis` |
| 10 Threats to Validity and Limitations | `sec:limits` | `limitations` |
| 11 Conclusion and Future Work | `sec:conclusions` | `conclusion` |

`tools/check.py --structure-only` verifies that every `\input` exists, braces and environments
balance, every `\ref` has a label, and every citation is in the bibliography. Its full mode compares
against the ACL original and is no longer meaningful after the two restructurings. **It does not
replace compiling**: there is no LaTeX on the machine this was written on.

## To do before submission

- **Compile it** (`latexmk -pdf main` or Overleaf with the `tompecs/` folder) and fix whatever the
  first build reports. Expect to adjust the table widths: tables written for two-column ACL pages
  now sit in a single column.
- **Length.** About 11,200 words and eight tables, which in acmsmall is probably in the mid-twenties
  of pages; this is an estimate. The venue limit is reported as 30 pages; whether references count
  is unknown.
- Fill in authors, affiliations, ORCIDs, acknowledgments, and the Data and Artifact Availability
  statement. The last is a heading only; nothing about availability is claimed.
- **Regenerate the CCS concepts** with the ACM tool. The identifiers in `main.tex` were written from
  memory and are not verified.
- Confirm single- versus double-blind review; if double-blind, add the `anonymous` option.
- Write the cover letter the journal asks for (fit with scope; any earlier version of this material;
  parallel submissions).

## Where the fit with TOMPECS is thinner, for the authors to decide

- TOMPECS is about modeling and performance evaluation. This paper is an empirical evaluation study
  with a strong methodology thread but **no analytic or statistical model of its own**. The
  framing here leans on the methodology thread; if reviewers want a model, candidates already
  latent in the data are an Amdahl bound on end-to-end gain for each application and a model of
  repetition noise. Neither is added here, because that would be new analysis, not restructuring.
- Single-sample cells and the absence of confidence intervals (Section 10.2) are the most likely
  reviewer objection for a measurement-focused venue.
- A **null arm** (a rerun of the unmodified binary, scored the same way as the candidates) would
  measure the noise floor directly instead of inferring it from repetition spread. A related launch-
  configuration study found that this exposed a baseline-measurement bias that repetition spread had
  not shown; whether the interleaved design used here is exposed to it is checkable from the existing
  timing data and is worth checking before a methodology-heavy submission.

## Changes after assembly (writing session, from 2026-10-26)

Each is a separate commit; edited prose carries an `% EDIT (2026-10-26)` or `% NEW (2026-10-26)`
comment. Statements still awaiting evidence or a decision are marked `\needcheck{...}` (blue), defined
in `main.tex`.

- **LAMMPS removed** (author's decision: Kokkos C++ is outside the pipeline's CUDA scope). Two
  applications remain. Lost with it: the GPU-package Amdahl paragraph, the withdrawn hand-tuned
  variant, the capped-profile/launch-skip sentence.
- **`chemv` removed from all results** (its built-in check cannot certify output) and described in
  8.2 as an outlier: a correct removal of unneeded loop structure, checked on 2026-10-26 with
  REPEAT=1 against the CPU reference.
- **Section 5** text made consistent with Table 1 (first-attempt counts; `minimal`/`cot` claims; no
  full-prompt arm). Abstract, introduction and conclusion follow.
- **Methodology**: where each table was measured and over how many clean repetitions; the Section 5
  grid is in-pipeline timing.
- **Cholla headline** stated over all four baseline-prompt samples (1.476-1.584x).
- **8.2** re-attributes the `concat`/Gemini gain and most of the `boxfilter`/GPT-5 loss to the
  structural prompt; the >5x `boxfilter` diffs were inspected.
- **10.2**: no valid replicate of the guidance comparison (the round-2 timing ran on the broken node).
- **HeCBench half of the profile-data ablation re-timed** on illyad with CUDA 13.3.1
  (`~/latest_opal/rerun_cu133/` on the cluster; the original 2026-09-22 timing ran during the
  driver fault of report sec. 14). Written in on 2026-10-27: 8.1 rewritten with a per-benchmark table
  (`tab:profablhec`): 19 scored pairs, 9 ties, 6 for and 4 against the profile, geomean 1.003 (GPT-5)
  and 0.979 (Gemini), so "nothing measurable on benchmarks" became "both directions, no net gain" in
  the abstract, intro, related work, 9.3 and conclusion. The `atomicSystemWide` correctness point is
  dropped (node artifact); `background-subtract`/GPT-5 was re-checked on CUDA 13.3.1 and stands.
  Table `tab:intent` now shows both original-rules arms (pcrl 0.88/0.81, code_only 1.08/1.01). 10.3's
  "verification unusable" paragraph is replaced by one on the node fault and `chemv`'s check.
- Cross-references repaired (new labels `sec:timing`, `sec:constraint`); Related Work deduplicated.
- **2026-10-29: restructured to the reviewer's outline** (see "Structure" above). Open from that
  review: the unmodified-program runtimes of `atan2`, `md5hash` and `accuracy` for Table 1 were never
  measured (`ablation_study_details.md`: "Baselines still needed"); re-running E1 with Gemini 3.1 Pro
  needs API credentials and the launcher scripts (`scripts/run_*_ablation.sh`, run on a TXState host).
