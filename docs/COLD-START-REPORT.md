# Cold-Start Report — WITNESS (stranger / judge simulation)

**Lane:** B2 (stranger cold-start). **Date:** 2026-08-27. **Tester carried no insider knowledge.**
**Method:** cloned the local repo fresh to `/tmp/witness-judge-test`, read only the README, then ran
every command literally as written — including a **true-stranger sandbox** (`HOME` + gcloud config
pointed at empty dirs, GCP env stripped) to remove this machine's ambient key/credential state.

---

## Overall verdict: RED as publicly shippable today → conditional GREEN once one commit is pushed

Do not average this into a mushy yellow. It is two distinct states:

- **RED — as a judge can actually clone it today.** The README's own clone URL
  (`github.com/Morkeeth/agent-work-record-witness-ata`) serves the **pre-rebrand** repo. `origin/main` is at
  `9fc3620`; the WITNESS rebrand is commit `32f78f5`, **local and unpushed** (`git branch -r
  --contains 32f78f5` is empty). A real judge cloning that URL reads a README titled
  `# hack-fleet-ata` / "Nothing governs the prompts" — none of the WITNESS story, none of the clean
  root. **Every green result below is invisible to them.** This blocks submission.

- **Conditional GREEN/YELLOW — the moment `32f78f5` is pushed.** With the rebranded tree in hand, the
  quickstart runs clean end-to-end offline, the live Cloud Run URL matches the README exactly, and the
  eligibility gate is honest about its own exit codes. Remaining issues are YELLOW, not blockers.

**The whole submission currently hangs on one `git push`.** That single line is the difference between
RED and GREEN.

---

## README as a judge reads it (2-minute test): GREEN

In two minutes I could answer all four questions: **what** (a trust/assurance layer that verifies
what agent fleets claim against the real object), **what it does** (two surfaces — verify each claim
vs git/deploy/test; rank + propagate winning prompts), **why it matters** (assurance, not trace
theater; between an agent's "done" and your trust), **how to try it** (curl the live URL + a 5-line
quickstart). Strong problem statement, honest "limits" section, clear eligibility table. This is the
best part of the repo.

---

## What I verified (primary-source, reproducible)

| Check | Result |
|---|---|
| Clone path actually tested | `git clone ~/CODE/hack-fleet-ata /tmp/witness-judge-test` → HEAD `32f78f5` (rebranded WITNESS state confirmed) |
| Live URL `/health` | **HTTP 200** · `{"ok":true,"store":"firestore","agent":"google.adk.agents.llm_agent.LlmAgent"}` — matches README |
| Live URL `/` | HTTP 200, same body |
| `python3 fleet_cli.py wedge` | exit 0 · `VERIFIED-BY-REPO` — **runs clean with NO gemini key + NO GCP** (true-stranger sandbox) |
| `python3 fleet_cli.py prove` | exit 0 · A 0 vs B 2 corrective turns · writes `surface/org-proof.html` — clean offline |
| `python3 -m gate.tonight_cases` | prints the 4-claim self-catch, GATE: BLOCK, **exit 1** (by design) |
| `pip install -r requirements.txt` | exit 0, clean |

The quickstart's "**stranger, no GCP required**" promise for `wedge` / `prove` is **TRUE** — verified
with the gemini key path made unreachable. Good.

---

## Where the core claim holds up (task step 4): PARTIAL — one live proof, one re-enactment

The core claim is "Witness catches false agent claims against the object." A judge can verify it from
the repo alone, but the two demos are not equal:

- **`contract/eligibility.py` — GENUINELY non-stageable.** It exercises the real environment live: the
  agent claimed "3 of 3 Google techs MET at runtime"; run cold, the object disagrees. This IS the tool
  catching a false claim against the object, reproducibly. **This is the demo to point judges at.**
- **`gate/tonight_cases.py` — real gate logic, hardcoded inputs.** The BLOCK/UNMEASURED verdicts are
  computed by real probes, but the case inputs are **hardcoded literals** (`call=lambda: "JsonlStore"`,
  fixed `observed=`/`actual_kind=` strings) — a narrated re-enactment of 2026-08-22, not a live
  re-read of the repo/logs. Its "not invented fixtures — see CURSOR-LOG.md" provenance rests on a doc
  in the authors' own world. A harsh judge will note the "not stageable" headline is itself, for this
  command, staged. Lead with eligibility.py; frame tonight_cases as a logged case series, not a live audit.

---

## Ranked friction points (harshest first) + one-line fixes

1. **[RED / BLOCKER] The rebrand is unpushed — the public clone serves the old repo.**
   → `cd ~/CODE/hack-fleet-ata && git push origin main` (verify `git branch -r --contains 32f78f5`).

2. **[YELLOW] `eligibility.py` shows 1/3 for a real stranger, not the README's headline "3 of 3 MET".**
   Cold (no gemini key, no GCP) only ADK is MET; Gemini + Firestore are NOT MET; exit 1. The 3/3 is only
   reproducible with the specific GCP project. The live URL's `store:firestore`+ADK is the real proof but
   the README never connects that dot.
   → In the eligibility table, point the "how to verify 3/3" probe at `curl .../health` (shows firestore+adk live), and label `eligibility.py` as "3/3 only with ADC + hack-fleet project; 1/3 cold, by design."

3. **[YELLOW] `.DS_Store` and `fleet/__pycache__/*.pyc` ship in the clone despite being in `.gitignore`** —
   they were committed before the ignore rule. Sloppy for a Google submission.
   → `git rm --cached .DS_Store fleet/__pycache__/*.pyc gate/__pycache__/*.pyc && git commit`.

4. **[YELLOW] Repo + dir are still `hack-fleet-ata` while the brand is WITNESS.** The quickstart does
   `git clone .../hack-fleet-ata && cd hack-fleet-ata` — a small credibility ding on first contact.
   → Rename the GitHub repo to `witness` (or note the mismatch explicitly in the README).

5. **[LOW] `open surface/org-proof.html` is macOS-only** — Linux judges have no `open`.
   → `open surface/org-proof.html 2>/dev/null || xdg-open surface/org-proof.html`.

6. **[LOW] `docs/` has 17 top-level files; the README links only 4.** The rebrand moved *some* process
   docs to `docs/internal/` but left BUILD-PLAN, GEAP-RULING, DETERMINISTIC-FLOOR, THIRTY-DAY-PLAN,
   VARIANCE-APPENDIX, etc. at top level — clutter a browsing judge wades through.
   → Move remaining process/spec docs into `docs/internal/`; keep only judge-facing docs at `docs/` top level.

7. **[LOW] `tonight_cases` exits 1 by design** (it's a gate that BLOCKs). A judge scripting exit codes
   reads that as failure.
   → One line in the README next to the command: "exits 1 = gate correctly BLOCKED; that's the demo."

---

## Bottom line for Oscar

The product is real and the live URL proves 3/3 for real. But **as a judge can clone it right now, they
get the old repo and none of this.** Push `32f78f5` first — nothing else matters until that is done. Then
address YELLOW #2 (the eligibility headline overstates what a cold run shows) so a judge who runs the
local probe instead of curling the URL doesn't see 1/3 and bounce.
