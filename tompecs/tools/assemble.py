#!/usr/bin/env python3
"""Assemble the TOMPECS manuscript from the existing sections.

Every sentence of the original paper is carried over by *extracting blocks from the old files*,
never by retyping them, so numbers and claims cannot drift. The only differences are the ones
listed in EDITS and the new connective text in NEW below; both are marked `% NEW` / `% EDIT` in
the generated files and listed in MAPPING.md.

    python3 tools/assemble.py          (from tompecs/; reads ../sections, writes sections/*.tex)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "..", "..", "sections")
NEW_DIR = os.path.join(HERE, "..", "sections")


def read(name):
    return open(os.path.join(OLD, name + ".tex"), encoding="utf-8").read()


def split(text, cmd):
    """(preamble, {title: chunk}) for top-level `\\cmd{title}` units, in file order."""
    pat = re.compile(r"^\\%s\{(.*?)\}.*$" % cmd, re.M)
    marks = [(m.start(), m.group(1)) for m in pat.finditer(text)]
    pre = text[:marks[0][0]] if marks else text
    units = {}
    for i, (s, title) in enumerate(marks):
        e = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        units[title] = text[s:e].rstrip() + "\n"
    return pre, units


def pick(units, *titles):
    out = []
    for t in titles:
        hit = [k for k in units if k.startswith(t)]
        assert len(hit) == 1, (t, list(units))
        out.append(units[hit[0]])
    return "\n".join(out)


def as_subsection(chunk, new_title=None, label=None):
    """Turn a leading \\paragraph{...} unit into a \\subsection."""
    m = re.match(r"\\paragraph\{(.*?)\}", chunk)
    title = new_title or m.group(1).rstrip(".")
    body = chunk[m.end():].lstrip("\n")
    return "\\subsection{%s}\n%s%s" % (title, ("\\label{%s}\n" % label) if label else "", body)


NEWTAG = "% NEW (written for the TOMPECS version; not in the original paper)\n"
EDITTAG = "% EDIT (original wording changed; see MAPPING.md)\n"
sections = {}

# ---------------------------------------------------------------- 1. introduction
intro = read("introduction")
pat = re.compile(r"(Within this loop we treat the prompt as the object of study\.)\s+Our\s+contributions are:")
assert pat.search(intro)
rq_text = "\n" + NEWTAG + r"""Because the loop's output is a measured execution time, the study is as much about how such systems
must be \emph{evaluated} as about how they should be prompted. We organize it around five research
questions:
\begin{description}\itemsep2pt
\item[RQ1] Which components of the prompt matter, and how reliably? (Section~\ref{sec:prompts})
\item[RQ2] Can speedups reported on benchmarks be trusted, and what does a model do when the
  benchmark's own scaffolding can be deleted? (Section~\ref{sec:intent})
\item[RQ3] Do conclusions drawn on single-kernel benchmarks transfer to the production applications
  those kernels represent? (Section~\ref{sec:realapps})
\item[RQ4] What is profiling evidence worth, supplied raw and supplied interpreted?
  (Section~\ref{sec:evidence})
\item[RQ5] What measurement and validation practice is needed to report any of this credibly on shared
  hardware? (Sections~\ref{sec:method}, \ref{sec:pitfalls} and~\ref{sec:limits})
\end{description}
Our contributions are:"""
intro = pat.sub(lambda m: m.group(1) + rq_text, intro)
intro = intro.rstrip() + "\n\n" + NEWTAG + r"""\paragraph{Organization.}
Section~\ref{sec:relatedwork} places the work in the literature and Section~\ref{sec:subject}
describes the optimization pipeline under study. Section~\ref{sec:method} states the workloads,
platforms, correctness validation and measurement protocol on which every later number depends.
Sections~\ref{sec:prompts}--\ref{sec:evidence} report the four studies behind RQ1--RQ4,
Section~\ref{sec:pitfalls} collects the evaluation pitfalls they exposed, Section~\ref{sec:limits}
states the threats to validity, and Section~\ref{sec:conclusions} concludes.
"""
sections["01_introduction"] = "\\section{Introduction}\n\\label{sec:intro}\n" + intro

# ---------------------------------------------------------------- 2. related work
sections["02_related"] = "\\section{Background and Related Work}\n\\label{sec:relatedwork}\n" + read("relatedWork")

# ---------------------------------------------------------------- 3. subject system
meth_pre, meth = split(read("methodology"), "subsection")
assert meth_pre.strip() == "", meth_pre
sections["03_subject"] = (
    "\\section{The Optimization Pipeline Under Study}\n\\label{sec:subject}\n"
    + NEWTAG
    + "This section describes the system whose behaviour the rest of the paper evaluates: the loop\n"
      "itself, the profiling evidence it can place in the prompt, and the structure of that prompt.\n\n"
    + pick(meth, "Pipeline", "Profiling data", "Prompt structure"))

# ---------------------------------------------------------------- 4. methodology
exp = read("experiments")
sections["04_methodology"] = (
    "\\section{Experimental Methodology}\n\\label{sec:method}\n"
    + NEWTAG
    + "Every result in this paper is a measured execution time on shared hardware, so its credibility\n"
      "rests on the protocol stated here: what was run, on what, how correctness was established, and\n"
      "how time was measured and summarized.\n\n"
    + "\\subsection{Workloads, Models and Platforms}\n\\label{sec:explanation}\n" + exp.lstrip()
    + "\n" + pick(meth, "Workload selection").replace("\\subsection{Workload selection}", "\\subsection{Workload Selection}")
    + "\n" + pick(meth, "Correctness").replace("\\subsection{Correctness}", "\\subsection{Correctness Validation}")
    + "\n" + pick(meth, "Timing").replace("\\subsection{Timing}", "\\subsection{Timing and Measurement Protocol}")
    + "\n" + NEWTAG
    + "\\subsection{Reporting Conventions}\n"
      "Speedups are reported against the unmodified program unless a table states otherwise, and every\n"
      "reported number comes from the separate measurement pass described above rather than from the\n"
      "pipeline's own in-run timing. Except where stated, each (application, model, prompt) cell is a\n"
      "single language-model sample, and an effect below roughly $5\\%$ in a single cell is treated as\n"
      "unresolved rather than small (Section~\\ref{sec:limits}). Where two arms are compared on a noisy\n"
      "benchmark, the comparison is scored against that pair's own repetition spread\n"
      "(Section~\\ref{sec:profabl}), and any speedup above $5\\times$ is treated as a correctness alarm and\n"
      "its diff inspected (Section~\\ref{sec:intent}).\n")

# ---------------------------------------------------------------- 5. prompt-component study
ana_pre, ana = split(read("analysis"), "paragraph")
assert ana_pre.strip() == "", ana_pre
sections["05_prompt_study"] = (
    "\\section{Prompt-Component Study}\n\\label{sec:prompts}\n"
    + NEWTAG
    + "This section reports the benchmark-scale ablation behind RQ1: six prompt variants, two models and\n"
      "six HeCBench kernels.\n\n"
    + "\\subsection{Prompt Variants}\n\\label{sec:ablation}\n" + read("ablation").lstrip()
    + "\n\\subsection{Results}\n\\label{sec:results}\n" + read("results").lstrip()
    + "\n\\subsection{Findings}\n\\label{sec:analysis}\n"
    + pick(ana, "Optimization quality", "Prompt components are not equally important", "Reliability"))

# ---------------------------------------------------------------- 6. gaming / validity of benchmarks
sc = read("semantic_constraint")
old_first = ("Section~\\ref{sec:analysis} motivates an explicit computational-intent constraint to prevent models from\n"
             "replacing the computation rather than optimizing it.")
assert old_first in sc, "semantic_constraint first sentence changed"
sc = sc.replace(old_first, EDITTAG + "The gaming observed in the ablation (Section~\\ref{sec:gaming-obs}) motivates an explicit "
                "computational-intent constraint to prevent models from\nreplacing the computation rather than optimizing it.", 1)
sections["06_gaming"] = (
    "\\section{Benchmark Validity: Gaming and the Semantic-Preservation Constraint}\n\\label{sec:intent}\n"
    + NEWTAG
    + "A speedup is only a result if the work that was timed is the work the program exists to do. This\n"
      "section shows that a model can deliver an enormous apparent speedup that passes both output\n"
      "comparison and a benchmark's own check, and evaluates a constraint that prevents it.\n\n"
    + as_subsection(ana["Benchmark gaming."], "Observation in the Ablation", "sec:gaming-obs")
    + "\n\\subsection{The Constraint and Its Effect}\n" + sc.lstrip())

# ---------------------------------------------------------------- 7. production applications
ra_pre, ra = split(read("realapps"), "subsection")
defects_title = [k for k in ra if k.startswith("Prompt-fidelity defects")][0]
defects_chunk = ra.pop(defects_title)
body = ra_pre.rstrip() + "\n\n" + "\n".join(ra.values())
sections["07_applications"] = "\\section{Production Applications}\n\\label{sec:realapps}\n" + body

# ---------------------------------------------------------------- 8. profiling evidence
sections["08_evidence"] = (
    "\\section{The Value of Profiling Evidence}\n\\label{sec:evidence}\n"
    + NEWTAG
    + "This section addresses RQ4 in two steps: whether profiling data helps at all (an arm with and an\n"
      "arm without it), and what happens when the data is converted into named remedies before the model\n"
      "sees it.\n\n"
    + "\\subsection{Does Profiling Data Help?}\n\\label{sec:profabl}\n" + read("profile_ablation").lstrip()
    + "\n\\subsection{When Profiling Data Becomes Prescriptive}\n\\label{sec:guidvar}\n" + read("guidance_variance").lstrip())

# ---------------------------------------------------------------- 9. pitfalls
sections["09_pitfalls"] = (
    "\\section{Evaluation Pitfalls in Practice}\n\\label{sec:pitfalls}\n"
    + NEWTAG
    + "Running the pipeline on production code exposed problems that benchmark runs had hidden, some of\n"
      "them in the evaluation itself. Table~\\ref{tab:pitfalls} collects them with the practice we adopted\n"
      "in response; each is discussed where it arose, and the last two subsections of this section give\n"
      "the tooling defects and the general contrast between benchmarks and applications.\n"
    + r"""
% NEW: summary table. Every row restates a finding made elsewhere in the paper; no new measurement.
\begin{table}[t]
\centering
\footnotesize
\caption{Evaluation pitfalls observed in this study, where each is discussed, and the practice adopted.}
\label{tab:pitfalls}
\begin{tabular}{@{}p{0.27\textwidth}p{0.10\textwidth}p{0.52\textwidth}@{}}
\toprule
\textbf{Pitfall} & \textbf{Section} & \textbf{Practice adopted} \\
\midrule
Edits that delete the measured work while preserving output and the built-in check
  & \ref{sec:intent} & Semantic-preservation constraint; any speedup above $5\times$ is a correctness alarm and its diff is inspected \\
Built-in PASS/FAIL that gives no usable verdict on the unmodified program
  & \ref{sec:limits} & A candidate's verdict is informative only where it differs from the pristine one; explicit gates for applications \\
Drift between sessions on shared nodes (up to $49\%$ on identical code)
  & \ref{sec:method} & Build once, interleave arms, wait for an idle GPU, log foreign GPU processes per repetition, require repetitions to agree \\
Gates that pass once and fail on a rebuild (hand-tuned LAMMPS variant)
  & \ref{sec:realapps} & Gate every build that is timed; validate each gate by fault injection \\
Target kernel dominant in GPU time but not in application time
  & \ref{sec:realapps} & Confirm end-to-end dominance before evaluating (LAMMPS: switch to the Kokkos backend) \\
Wall clock dominated by setup (AutoDock-GPU CUDA setup: $68$\,s)
  & \ref{sec:method} & Use each application's own phase timer \\
Prompt contents differing from what was believed sent
  & \ref{sec:defects} & Defects fixed; earlier results reported as measured and not regenerated \\
Single samples and noisy pairs
  & \ref{sec:profabl}, \ref{sec:limits} & Score a pair a tie when its difference is inside its own spread; treat sub-$5\%$ single-cell effects as unresolved \\
Compilation context invisible to a single-file editor
  & \ref{sec:realapps} & Reported as the dominant real-code failure mode; carrying that context in the prompt is future work \\
\bottomrule
\end{tabular}
\end{table}

"""
    + defects_chunk.replace("\\subsection{Prompt-fidelity defects exposed by real code}",
                            "\\subsection{Prompt-Fidelity Defects Exposed by Real Code}", 1)
    + "\n" + as_subsection(ana["From benchmarks to applications."], "Benchmarks Versus Applications"))

# ---------------------------------------------------------------- 10. threats to validity
lim_pre, lim = split(read("limitations"), "paragraph")
assert lim_pre.strip() == "", lim_pre
sections["10_validity"] = (
    "\\section{Threats to Validity and Limitations}\n\\label{sec:limits}\n"
    + NEWTAG
    + "We group the limitations of the study by the kind of validity they threaten. The text of each item\n"
      "is as in the earlier version of this paper.\n\n"
    + "\\subsection{Measurement and Internal Validity}\n"
    + pick(lim, "Measurement on shared hardware", "Tooling defects discovered during the study")
    + "\n\\subsection{Statistical Conclusion Validity}\n"
    + pick(lim, "Sampling of model outputs", "Coverage of the profile-data ablation")
    + "\n\\subsection{Construct Validity}\n"
    + pick(lim, "Correctness gates are empirical", "Benchmark gaming is detected heuristically",
           "Benchmark verification was unusable", "Scope of the objective")
    + "\n\\subsection{External Validity}\n"
    + pick(lim, "Hardware and software scope", "Single-file editing"))

# ---------------------------------------------------------------- 11. conclusion
sections["11_conclusion"] = "\\section{Conclusion and Future Work}\n\\label{sec:conclusions}\n" + read("conclusion")

os.makedirs(NEW_DIR, exist_ok=True)
for name, text in sections.items():
    open(os.path.join(NEW_DIR, name + ".tex"), "w", encoding="utf-8").write(text.rstrip() + "\n")
    print("wrote sections/%s.tex  (%d words)" % (name, len(text.split())))
