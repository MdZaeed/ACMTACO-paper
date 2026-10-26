# Writing handoff: the OPTIMAS paper, for ACM TOMPECS

For a Claude Code session (or a person) that picks up the *writing* of this paper. Written
2026-10-26 by the session that did the experiments and the restructuring. The experiments continue in
another session in a different repository, so **you do not need to run anything on a GPU or a cluster
to work on the text**.

## 60-second orientation

- **The paper:** "Prompting for Performance: Profile-Guided LLM Optimization of Real GPU
  Applications": an empirical study of how prompt design (guardrails, profiling evidence) shapes an
  LLM's ability to optimize GPU code, pushed from HeCBench kernels onto AutoDock-GPU, LAMMPS and
  Cholla. Models: GPT-5, Gemini 2.5 Pro (benchmark ablation), Gemini 3.1 Pro (applications).
- **Target venue:** *ACM Transactions on Modeling and Performance Evaluation of Computing Systems*
  (TOMPECS), `acmart` format `acmsmall`. The paper started as an ACL-style draft.
- **The manuscript to edit is `tompecs/`** (entry point `tompecs/main.tex`, text in
  `tompecs/sections/`). The ACL-style files in `sections/` and `main.pdf` are the *old* version, kept
  for reference; do not edit them.
- **It has never been compiled by the session that wrote it** (no LaTeX on that machine). Whether it
  compiles on Overleaf is unknown to this handoff: the author reported a first error, `Undefined control
  sequence` in `output.aux`, a stale-cache symptom, and a clean recompile was suggested; the outcome was not
  reported back. Treat compilation as the first open question and ask.
- **Read `tompecs/MAPPING.md` next.** It says what was verified about the venue, how the paper was
  reorganised, which text is new, and the to-do list.

## Repository, branches, and the one coordination hazard

- Remote `git@github.com:MdZaeed/ACMTACO-paper.git`; **`main` is what the author's Overleaf project
  syncs.** A branch `tompecs` also exists on the remote and is behind `main`; ignore it.
- The author edits in Overleaf too. Overleaf pushes commits to `main` ("Updates from Overleaf"). So:
  **`git pull --ff-only` before you start and before every push; commit small; never force-push;
  never rebase published commits.** If the pull is not a fast-forward, stop and tell the author.
- Do not push to `main` without the author saying so. Local commits are fine.
- **Do not re-run `tompecs/tools/assemble.py`.** It generated the section files once from the old ones
  and would overwrite every edit made since. The files in `tompecs/sections/` are now the source of
  truth. `assemble.py` is kept only as provenance.
- A known problem the author introduced in Overleaf on 2026-10-22: the *old* file
  `sections/guidance_variance.tex` now contains `\bold{Two} practical consequences ...`. `\bold` is not a
  LaTeX command (use `\textbf{Two}`); it breaks the *old* ACL build only. The TOMPECS copy
  (`tompecs/sections/08_evidence.tex`) never received that edit. Mention it to the author.

## Checking your edits without a compiler

`python3 tompecs/tools/check.py --structure-only` checks that every `\input` exists, braces and
environments balance, every `\ref` has a `\label` (and none is duplicated), and every cited key is in
`tompecs/custom.bib`. Run it after every edit. It cannot find an undefined macro, a package problem, or a
float that will not fit: only a real build does. Without `--structure-only` it also compares against
the original paper and will now report every legitimate edit (and the author's `\bold` edit) as a
difference; that mode is only meaningful for the freshly assembled text.

## Where each claim's evidence lives

The paper's numbers come from experiments recorded in the sibling repository
**`/home/zayed/latest_opal/optimas`** (a different git repo; read-only for you). Every number you
write or change must trace to one of these. Memory-style summaries elsewhere can be stale; the
reports and CSVs are the evidence.

| paper section | claim | evidence |
|---|---|---|
| 5 Prompt-component study (Table 1) | 72 runs, 6 variants x 2 models x 6 kernels; `minimal` degrades, `cot` never hurts | `ablation_study_details.md` (raw runtimes with iteration counts, aggregate summary); `scripts/optimas_study/README.md` |
| 6 Benchmark validity | `atomicSystemWide` 1504x / 2809x without the constraint, 0.94x / 0.71x with it | `scripts/optimas_study/README.md` ("TL;DR"); `scripts/optimas_study/results/` |
| 7 Production applications | AutoDock-GPU, LAMMPS, Cholla results, gates, Amdahl point, hand references | `reports/OPTIMAS_real_applications_report.md`: sec. 4 AutoDock-GPU, 5 LAMMPS, 6 Cholla, 7 pipeline bugs (the defects table), 8 corrections to earlier claims, 9 findings |
| 8.1 Does profiling data help? | PC+roofline worth +7.7-11.5% on Cholla; ties on the HeCBench pairs | same report, sec. 13; `scripts/optimas_study/results/prof_ablation_*.csv` |
| 8.2 Prescriptive guidance | `chemv` 7.835x -> 1.075x; `bincount` 1.04x -> 1.37x; `concat` 0.349x | `scripts/optimas_study/results/four_arm_hopper2.csv`; `reports/PAPER_ADDITIONS_AND_PYTORCH_MEMO.md` sec. 1.1 |
| 10 Threats to validity | `chemv` verification is vacuous (all-NaN output passes) | the report above; note that `chemv` is *dropped* from the AMD arm for this reason |
| (optional) workload table | lines of code of the studied programs | `/home/zayed/latest_opal/optimas/reports/source_line_counts.md` |

Facts that look surprising and are correct, so do not "fix" them: the benchmark ablation uses
**Gemini 2.5 Pro** and the applications use **Gemini 3.1 Pro** (the paper says so); the profiles for the
six ablation benchmarks were collected on an A100 and timed on an H100 (stated in Section 4.1).

## What the earlier analysis recommended adding

`/home/zayed/latest_opal/optimas/reports/PAPER_ADDITIONS_AND_PYTORCH_MEMO.md` (Part 1) is a ranked list
of paper additions written 2026-09-25. Its most useful points for the text:

- **Positioning.** The closest work is *KernelPro* (interprets profiler output into guidance; reports
  +125% over raw metrics): their arms both have profiling data, ours is data vs no data, and the paper
  should say so explicitly in Related Work and Section 8. *KernelBench-Verified* (an audit of reward
  hacking in generated kernels) and *PerfAgent* (repository-level, profiler-guided) must also be cited.
  `custom.bib` has 26 entries of which 19 are cited; **check whether all three are present** before
  adding them.
- The guidance-variance result (Section 8.2) is presented there as the distinctive finding.
- Do not claim to be first to observe performance-setting reward hacking; the contribution is the HPC
  setting, a measured prompt-level mitigation, and a cheap detection rule.

## What needs the author, not you

Authors, affiliations, ORCIDs (TOMPECS requires one per submitting author); acknowledgments; the Data
and Artifact Availability statement (a heading only: nothing may be claimed about what is released until
the author says); the cover letter the journal asks for; whether review is single- or double-blind
(unknown; if double-blind add the `anonymous` option); the CCS concepts (written from memory in
`main.tex`; regenerate at https://dl.acm.org/ccs); whether the 30-page limit counts references.
**Ask; do not invent.**

## Open writing questions (author's call, in rough priority)

1. **Compile it** and fix the first real errors. Tables were written for two-column ACL pages and now
   sit in a single column.
2. **A model, or not.** TOMPECS is about modeling and performance evaluation; this is an empirical
   study with a strong methodology thread and no model of its own. The framing leans on the methodology.
   Candidate analyses already latent in the data (an Amdahl bound per application, a model of repetition
   noise) are *new analysis*, not rewriting, and need the author's decision first.
3. **Confidence intervals / single-sample cells** (Section 10.2) are the likeliest reviewer objection.
4. **Deduplicate.** The shared-node drift figures and the measurement protocol appear in Sections 4.4,
   7 and 10; a journal paper would state them once.
5. **A null arm.** A rerun of the unmodified binary, scored like the candidates, would measure the noise
   floor directly. A separate study by the same author (launch-configuration sweeps, README at
   `/home/zayed/latest_opal/optimas/scripts/launch_params/README.md`, section "A bias in every sweep so
   far") found that such null configurations exposed a baseline-first measurement bias that
   repetition-spread had hidden. Whether this paper's interleaved design is exposed is checkable from its
   existing timing data. **Do not import numbers from that study into this paper without the author's
   decision**; it is a different project.
6. Length: about 11,200 words and eight tables; probably mid-twenties of acmsmall pages (an estimate).

## Rules for this kind of editing

- **No new claim without evidence.** If a sentence needs a number, find it in the sources above or ask.
  If the evidence is missing, mark it `\tzi{...}` (a red FIX note, defined in `main.tex`) instead of
  guessing.
- Keep edits reviewable: small commits with messages that say what changed and why. When you rewrite
  existing text, say so in the message.
- Mark new prose you add with a `% NEW` comment, as the earlier version did, and keep `MAPPING.md`
  current when sections move.
- Preserve the paper's honesty about its own limits (Section 10); do not soften a limitation to make a
  claim read better.
- Report back to the author in plain terms: what you changed, what you could not verify, and what you
  need decided.

## Starting and continuing a session

```bash
cd /home/zayed/ACMTACO-paper
git pull --ff-only origin main            # needs the ssh agent; see below
claude                                     # CLAUDE.md here points the session at this file
# later, to pick the same conversation back up:
claude --continue                          # or: claude --resume   (choose from a list)
```

Starter prompt for a fresh session:

> Read WRITING_HANDOFF.md and tompecs/MAPPING.md, then run `python3 tompecs/tools/check.py
> --structure-only`. Do not edit anything yet. Summarise the state of the manuscript and list the open
> items you could make progress on without the author, in order.

Good first tasks that need no author input: (a) check the three related-work citations listed above
against `custom.bib` and draft the positioning sentences with `\tzi{}` where a reference is missing;
(b) deduplicate the measurement-protocol text across Sections 4.4, 7 and 10; (c) tighten Section 9's
table so every row's "Section" column matches the final numbering; (d) read the whole manuscript for
leftovers of the ACL layout (references to "columns", "this page", `\resizebox{\textwidth}` tables).

**Sessions do not share memory.** A session started in this directory has its own memory, separate from
the experiments session's. What the experiments session knows that matters here is in this file and in
the reports it points to. If you need more, the experiments session's notes are at
`/home/zayed/.claude/projects/-home-zayed-latest-opal-optimas/memory/` (index `MEMORY.md`); relevant files
are `optimas-prompt-study.md`, `autodock-gpu-real-app.md`, `diag-ablation-task.md`,
`guidance-variance-finding.md`, `chemv-verification-vacuous.md` and `optimas-anti-gaming-constraint.md`.
Read them as leads, verify against the reports.

**ssh to GitHub** needs an agent that holds the author's key. After a machine restart the agent socket
moves (it has been `/run/user/1000/keyring/ssh`, then `/run/user/1000/gcr/ssh`); a dead socket looks like
a network failure. `. /home/zayed/latest_opal/optimas/scripts/launch_params/agent.sh` sets
`SSH_AUTH_SOCK` to the first live one.

## Not this paper

The CPU-optimization arm is a separate paper in `~/latest_opal/optimas-cpu-paper` (its own handoff,
`LOG.md`). The launch-configuration / autotuning study has no paper yet. Do not mix them in.
