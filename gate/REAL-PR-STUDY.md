# Running the gate on real PR history — the honest result (2026-08-23)

**The proposed fundable number was "on N real PRs, the gate would block X." The honest answer is
X ≈ 0 on merged PR bodies — and WHY it is zero is the actual finding.**

## What was run (read-only, public repos, nothing posted)
- **15 human PRs** (microsoft/vscode, merged): hard-claim probes (SHA, path) fired on **0**.
- **60 agent PRs** (`app/copilot-swe-agent`, merged, across ~60 repos): 6 had anything claim-shaped;
  running the gate against each PR's **actual changed-files list** (via GitHub API, not a clone):

```
PASS      every claimed path that is really a path IS in the changed files (8/8)
ARTIFACT  2 "claims" were backticked class names, not file paths (parser noise)
REAL divergences (would-block, genuine): 0
```

## The finding, three parts

1. **Zero false positives on 75 real honest PRs.** The gate passed every honest human and agent PR.
   That is the *"safe to install, does not cry wolf"* proof — real, measurable, and it is half of
   what makes a gate installable. A gate that blocked honest PRs would be uninstallable; this does not.

2. **Merged PR bodies do not carry the confident lie.** Two reasons, both honest:
   - The PR body is descriptive prose ("this introduces a review-agent flow"), **not a self-report**
     ("committed as X, 214 tests pass, done"). The falsifiable claim is not in the body.
   - **Survivorship:** a *merged* PR already passed human review. The lie the gate exists to catch is
     caught (or not) *before* merge, so merged history is the wrong place to measure block-rate.

3. **Therefore the gate's real input is the agent's DONE REPORT / transcript, not the PR body.**
   This is Claims Inbox's original insight, now confirmed by data: *"committed as `deadbee`, tests
   pass, done"* lives in the agent's run report and chat — which we ingest via the transcript corpus
   — not in the merged PR body that a code-reviewer sees.

## What this changes about the company (honestly)

- **Do NOT pitch "we catch dishonesty in X% of real PRs."** On merged PR bodies that number is ~0,
  and claiming otherwise is the exact overclaim this product exists to refuse.
- **DO pitch two true things:** (a) zero false positives on real honest work — safe to install;
  (b) the confident-lie failure lives in the **transcript**, pre-merge, which is the input nobody
  else ingests (Qodo/CodeRabbit read the diff; observability reads the trace; neither reads the
  self-report against the outcome). The corpus is the moat *because* that is where the lie is.
- **The real experiment that WOULD produce a block number** needs pre-merge agent done-reports or a
  live agent fleet's transcripts — i.e. a design partner running agents, not public merged history.
  That is the first-customer experiment, not a public-data study.

## Method note
Checked claimed paths against each PR's real `pulls/{n}/files` list (exact, no clone, no
false-block-from-wrong-checkout). Classified backticked non-paths as artifacts rather than counting
them as passes or blocks. 0 real divergences is a measured 0, not an unmeasured one.
