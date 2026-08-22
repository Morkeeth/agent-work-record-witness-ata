# The market, validated — 2026-08-22 (not asserted; searched)

## The pain is real, hard-budget, and board-level

- **53% of enterprises** run at least one coding agent in production (Q1 2026). Razorpay's "Slash"
  merges **thousands of agent PRs a month, a third with no human in the loop.**
- **The bottleneck inverted:** codegen is 5–10× faster, so *verification before merge* is now the
  constraint, not writing code.
- **Trust is the gap:** only 33% of developers trust AI output; 46% actively distrust it.
  AI-co-authored PRs average **10.83 issues vs 6.45** for human-only.
- **Incidents wrote the policies:** Replit's agent deleted a production database (Jul 2025);
  Amazon's Kiro tore down a CloudFormation stack (Feb 2026) → Amazon now requires senior sign-off.

## The category is crowded — and we are NOT in the crowded part

| Player | What it does | Object it checks |
|---|---|---|
| **Qodo** ($70M Series B, "independent verification layer") | multi-agent code review — bug/compliance/architecture | the **code artifact** (is the diff good?) |
| **CodeRabbit, Augment, Baz, Code Metal** | automated PR review, adversarial maker-checker | the **code artifact** |
| **Langfuse / AgentOps / Datadog** | tracing, spans, tokens | the **trace** (what the agent did) |
| **THIS** | outcome-based verification of the agent's SELF-REPORT | the **claim vs the object** (is what it *said* true?) |

## The wedge the market just named, and nobody sells

The 2026 failures are not "the code is buggy" (Qodo's lane). They are the agent's **report** diverging
from the **outcome**, verbatim from the discourse:

- *"a clean 200 and a confident lie that dashboards won't detect"*
- *"reported deployed while production still served the old revision"*
- *"self-reports advance to Done even when git, deployment, and production disagree"*
- *"outcome-based verification — check what actually happened instead of what the agent said happened"*

**Code review reviews the diff. Observability scores the trace. Neither asks whether the agent's
"done" is TRUE against the repo, the deploy, and the tests.** That is this product, and the emerging
term for it — *outcome-based verification* — did not exist as a category name six months ago.

## Why this repo can do it and a code-reviewer structurally cannot

A code-reviewer sees one diff in isolation. This reads the agent's **full execution trace + the repo
state** (the transcript corpus + repo-witness), so it can catch *"I ran the tests"* when the
transcript shows the test command was never called — a claim a diff-reviewer cannot even see. The
authorship-gated corpus (per-harness, `promptSource`-aware) is the moat that makes claim-vs-trace
possible, not just claim-vs-repo.

## Sources
- siliconangle.com / techcrunch.com — Qodo $70M, "verification is the new bottleneck"
- augmentcode.com — adversarial code review, the inverted verification bottleneck
- medium.com/kairi-ai — "my agent passed every health check and was confidently wrong"
- magicmoment.jp — "reported deployed while prod served the old revision"
- dev.to/moonrunnerkc — "AI coding agents lie about their work; outcome-based verification catches it"
- Stack Overflow 2025 Developer Survey; Carnegie Mellon AI-adoption study (10.83 vs 6.45 issues/PR)
