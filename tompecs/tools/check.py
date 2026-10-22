#!/usr/bin/env python3
"""Structural checks for the TOMPECS manuscript, for use where no LaTeX compiler is available.

This does NOT replace compiling: it cannot find an undefined macro, a bad package option, or a
float that will not fit. It does check what an assembly mistake would break:

  1. every \\input target exists
  2. braces and \\begin/\\end environments balance in every file
  3. every \\ref has a \\label, and no label is defined twice
  4. every citation key exists in custom.bib, and the cited set equals the original paper's
  5. no number of the original paper has been lost, and no number appears fewer times
  6. every non-comment line of the original sections still appears in the new ones, except a short
     list of lines that were deliberately changed (reported, so they can be reviewed)

Exit status 1 if any check fails.
"""
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OLD = os.path.join(ROOT, "..", "sections")
OLD_FILES = ["abstract", "introduction", "relatedWork", "methodology", "experiments", "ablation",
             "results", "semantic_constraint", "realapps", "profile_ablation", "guidance_variance",
             "analysis", "limitations", "conclusion"]
fails = []


def strip_comments(t):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in t.splitlines())


def rd(p):
    return open(p, encoding="utf-8").read()


new_paths = [os.path.join(ROOT, "main.tex")] + sorted(glob.glob(os.path.join(ROOT, "sections", "*.tex")))
new = {p: strip_comments(rd(p)) for p in new_paths}
old = {n: strip_comments(rd(os.path.join(OLD, n + ".tex"))) for n in OLD_FILES}
new_all = "\n".join(new.values())
old_all = "\n".join(old.values())

# 1. inputs
for p, t in new.items():
    for m in re.finditer(r"\\input\{([^}]+)\}", t):
        tgt = os.path.join(os.path.dirname(p) if "sections" in p and not m.group(1).startswith("sections") else ROOT,
                           m.group(1) + ".tex")
        if not os.path.exists(tgt) and not os.path.exists(os.path.join(ROOT, m.group(1) + ".tex")):
            fails.append("missing \\input target %s (from %s)" % (m.group(1), os.path.basename(p)))

# 2. balance
for p, t in new.items():
    flat = re.sub(r"\\[{}%$&#_]", "", t)
    if flat.count("{") != flat.count("}"):
        fails.append("%s: unbalanced braces (%d open, %d close)" % (os.path.basename(p), flat.count("{"), flat.count("}")))
    stack = []
    for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", t):
        if m.group(1) == "begin":
            stack.append(m.group(2))
        else:
            if not stack or stack.pop() != m.group(2):
                fails.append("%s: \\end{%s} does not match" % (os.path.basename(p), m.group(2)))
    if stack:
        fails.append("%s: unclosed environment(s) %s" % (os.path.basename(p), stack))

# 3. labels / refs
labels = collections.Counter(re.findall(r"\\label\{([^}]+)\}", new_all))
for k, c in labels.items():
    if c > 1:
        fails.append("label %s defined %d times" % (k, c))
refs = set()
for m in re.finditer(r"\\(?:ref|autoref|cref)\{([^}]+)\}", new_all):
    refs.add(m.group(1))
for r in sorted(refs - set(labels)):
    fails.append("\\ref{%s} has no \\label" % r)

# 4. citations
bib = set(re.findall(r"@\w+\{([^,\s]+),", rd(os.path.join(ROOT, "custom.bib"))))


def cites(t):
    keys = set()
    for m in re.finditer(r"\\cite[a-z]*\{([^}]+)\}", t):
        keys |= {k.strip() for k in m.group(1).split(",")}
    return keys


cn, co = cites(new_all), cites(old_all)
for k in sorted(cn - bib):
    fails.append("citation key %s not in custom.bib" % k)
if cn != co:
    fails.append("cited keys differ from the original: only-new=%s only-old=%s" % (sorted(cn - co), sorted(co - cn)))


# 5. numbers
def numbers(t):
    t = t.replace("{,}", "").replace("\\,", "")
    t = re.sub(r"\\label\{[^}]*\}|\\ref\{[^}]*\}|\\cite[a-z]*\{[^}]*\}", " ", t)
    return collections.Counter(re.findall(r"\d+(?:[.,]\d+)*", t))


no, nn = numbers(old_all), numbers(new_all)
lost = {k: v - nn.get(k, 0) for k, v in no.items() if nn.get(k, 0) < v}
for k, v in sorted(lost.items()):
    fails.append("number %s appears %d fewer time(s) than in the original" % (k, v))

# 6. lines
norm = lambda l: " ".join(l.split())
new_lines = {norm(l) for l in new_all.splitlines() if l.strip()}
missing = []
for n in OLD_FILES:
    for l in old[n].splitlines():
        if l.strip() and norm(l) not in new_lines:
            missing.append((n, norm(l)))
EXPECTED = [  # lines deliberately changed by assemble.py
    ("introduction", "number of repair iterations. Within this loop we treat the prompt as the object of study. Our"),
    ("introduction", "contributions are:"),
    ("semantic_constraint", "Section~\\ref{sec:analysis} motivates an explicit computational-intent constraint to prevent models from"),
    # headings renamed or promoted (a \paragraph became a \subsection; title case)
    ("methodology", "\\subsection{Correctness}"),
    ("methodology", "\\subsection{Timing}"),
    ("methodology", "\\subsection{Workload selection}"),
    ("realapps", "\\subsection{Prompt-fidelity defects exposed by real code}"),
    ("analysis", "\\paragraph{Benchmark gaming.}"),
    ("analysis", "\\paragraph{From benchmarks to applications.}"),
]
unexpected = [m for m in missing if m not in EXPECTED]
for n, l in unexpected:
    fails.append("original line missing from the new manuscript [%s]: %s" % (n, l[:110]))

print("files checked: %d | labels: %d | refs: %d | citation keys: %d (bib has %d)" %
      (len(new), len(labels), len(refs), len(cn), len(bib)))
print("original lines: %d, carried over verbatim: %d, deliberately changed: %d" %
      (sum(1 for n in OLD_FILES for l in old[n].splitlines() if l.strip()),
       sum(1 for n in OLD_FILES for l in old[n].splitlines() if l.strip()) - len(missing), len(missing) - len(unexpected)))
if fails:
    print("\nFAILED (%d):" % len(fails))
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("OK")
