# Instructions for sessions in this repository

This repo holds the OPTIMAS paper, being prepared for ACM TOMPECS. **Read `WRITING_HANDOFF.md` first**,
then `tompecs/MAPPING.md`.

- Edit only `tompecs/` (the TOMPECS manuscript). The ACL-style `sections/` and `main.pdf` are the old
  version; leave them.
- Do not re-run `tompecs/tools/assemble.py`: it would overwrite later edits.
- No new claim or number without evidence from the sources listed in `WRITING_HANDOFF.md`; mark gaps
  with `\tzi{...}` rather than guessing. Ask the author about authors, ORCIDs, availability, CCS codes,
  review type, and anything that is a judgement about the paper's framing.
- The author also edits in Overleaf, which syncs `main`: `git pull --ff-only origin main` before
  working and before pushing; never force-push; do not push without the author's say-so.
- There is no LaTeX compiler on this machine. After each edit run
  `python3 tompecs/tools/check.py --structure-only`; it is not a substitute for a real build.
