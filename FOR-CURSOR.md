# FOR CURSOR — review lane

**This repo only.** Cursor works inside one repo; git is the mailbox. Do not reach into
`~/CODE/hack-agent-science` or `~/CODE/agent-claims-inbox` — separate lanes, separate reviewers.

## What this is
All Things Agentic (Devpost, **Aug 31 2026 5:00pm PDT**). Org-level fleet and prompt management
built on the `transcripto` corpus. Read `PHASE-0.md` → `CONTEXT.md` → `LANE.md`. Currently
**Phase 0**: no product code exists yet, by design.

## What to review — in this order
1. **`PHASE-0.md` ladder #2, the hours estimate.** ~52h across six slices. Agents are
   structurally blind to duration. **Is this scope honest for 9 days, or is it the
   under-ambition failure wearing a table?** This is the highest-value thing you can rule on.
2. **`CONTEXT.md` "What it is NOT".** Three incumbents are pre-answered — GitHub Agent HQ /
   Mission Control (Oct 2025, free in Copilot), Mount Helicon (Oscar's own product), and
   DX / GitClear / Jellyfish. **Find a fourth we missed, or break one of the three
   distinctions.** If Mission Control already does surface 3 or 5, that is fatal and we need
   to know now, not on Aug 30.
3. **The wedge.** Surface 5 — *"here is the better prompt, taken from your own best operator"*.
   Is that defensible, or does it collapse into "an LLM rewrites your prompt"?
4. **The moat claim.** `transcripto`'s finding that ~95% of `user` turns in a transcript are
   not the user. Verify it against `~/CODE/transcripto` rather than taking this file's word.

## The house rules
- **Cite the object, not the note.** Every number here is a claim with an author.
- Append to `CURSOR-LOG.md`; never overwrite another lane's file.
- **Outward acts are Oscar's alone** — push, deploy, publish, submit.
