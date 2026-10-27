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

## How the paper was restructured

The ACL paper was a flat sequence of studies. TOMPECS is a performance-evaluation venue, so the
manuscript is reorganised around the part of the work that is evaluation methodology: how to
measure, validate and report an LLM-based optimizer's results credibly on shared hardware. The
studies are unchanged; they are now grouped as answers to five research questions and the
evaluation material that was scattered across Limitations, Analysis and Real Applications is
gathered into Methodology, a Pitfalls section, and a Threats-to-Validity section.

| new section | label | built from (old files) |
|---|---|---|
| 1 Introduction | `sec:intro` | `introduction` (verbatim) + **new**: five research questions, organization paragraph |
| 2 Background and Related Work | `sec:relatedwork` | `relatedWork` (verbatim; moved earlier) |
| 3 The Optimization Pipeline Under Study | `sec:subject` | `methodology`: Pipeline, Profiling data, Prompt structure |
| 4 Experimental Methodology | `sec:method` | `experiments` (4.1) + `methodology`: Workload selection (4.2), Correctness (4.3), Timing (4.4) + **new** 4.5 Reporting Conventions |
| 5 Prompt-Component Study | `sec:prompts` | `ablation` (5.1), `results` (5.2), `analysis`: Optimization quality, Prompt components, Reliability (5.3) |
| 6 Benchmark Validity | `sec:intent` | `analysis`: Benchmark gaming (6.1) + `semantic_constraint` (6.2) |
| 7 Production Applications | `sec:realapps` | `realapps` minus the defects subsection |
| 8 The Value of Profiling Evidence | `sec:evidence` | `profile_ablation` (8.1), `guidance_variance` (8.2) |
| 9 Evaluation Pitfalls in Practice | `sec:pitfalls` | **new** summary table + `realapps`: defects subsection + `analysis`: From benchmarks to applications |
| 10 Threats to Validity and Limitations | `sec:limits` | `limitations`, regrouped under internal / statistical-conclusion / construct / external validity |
| 11 Conclusion and Future Work | `sec:conclusions` | `conclusion` (verbatim) |

All old labels are kept (`sec:ablation`, `sec:results`, `sec:analysis`, `sec:profabl`, `sec:guidvar`,
`sec:defects`, `sec:explanation`, ...) on the matching new heading, so cross-references still resolve.

## Everything that is not a verbatim move

New text, all marked `% NEW` in the generated files, and containing no measurement or claim that is
not already in the paper:

1. the research-question paragraph and the "Organization" paragraph in the introduction;
2. one- or two-sentence openers for Sections 3, 4, 5, 6, 8, 9, 10;
3. Section 4.5 Reporting Conventions, which restates conventions already stated elsewhere
   (medians over clean repetitions, speedups against the unmodified program, single-sample cells,
   the 5% unresolved threshold, the tie rule, the 5x alarm);
4. the pitfalls table (`tab:pitfalls`), a summary whose every row cites a finding made elsewhere.

Edits to existing wording (marked `% EDIT`, plus heading renames):

1. the first sentence of the semantic-constraint text. It said "Section analysis motivates an
   explicit computational-intent constraint"; the gaming paragraph it pointed to now sits immediately
   before it (Section 6.1), so it now reads "The gaming observed in the ablation (Section 6.1)
   motivates ...";
2. headings renamed to title case, and two `\paragraph` units promoted to `\subsection`
   (Benchmark gaming; From benchmarks to applications);
3. the intro's sentence "Within this loop we treat the prompt as the object of study. Our contributions
   are:" is split by the new research-question paragraph.

Duplication carried over from the original and left alone: the shared-node drift figures and the
measurement protocol appear in Section 4.4, in Section 7 (Measurement) and in Section 10. A journal
version would normally state them once and point to them.

`tools/check.py` verifies the assembly: every \input exists, braces and environments balance, every
`\ref` has a label, every citation is in the bibliography and the cited set equals the original's,
no number of the original appears fewer times, and 889 of the original's 898 non-comment lines are
carried over verbatim (the other 9 are exactly the edits listed above). **It does not replace
compiling**: there is no LaTeX on the machine this was written on, so the manuscript has never been
built.

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
