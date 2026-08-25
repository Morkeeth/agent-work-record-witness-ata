# HUMAN-WRITING-EVAL-METHOD — evaluating a person's own prompts and notes

**Task (Oscar, verbatim):** "put this as a task to review how to properly evaluate human writings, or maybe it's easy to digest."

**Answer to the "easy to digest" question, up front: YES, mostly.** Five of the six
dimensions below are deterministic (regex + word counts) and plug straight into the
existing `prompt_patterns()` in `fleet/coach.py`. Exactly ONE dimension — goal-sufficiency
— genuinely needs a light model judge. Ship the deterministic five first; they get most of
the value. Evidence: the two deterministic tags that already exist (`detailed`,
`states-a-check-or-done-condition`) sit at the TOP of the survival table (65% each vs a
47% base rate, `reports/coach-oscar-2026-08-25.txt`).

---

## 1. Why survival alone is not enough — the confound, in our own data

`fleet/coach.py` measures **SURVIVAL**: did the prompt reach a durable Write/Edit or an
un-reverted `git commit` in-episode. That is an OUTCOME proxy — cheap, objective, and
honest about its own limits (see the module docstring). It is not a judgment of the
writing.

The confound is visible in the current report:

> `60%  (21/35)  no-object (pronoun/vague)` — in the **TOP** patterns.

An intrinsically bad property (vague, no named object) out-survives the 47% base rate.
Two readings, both fatal to "survival alone":

1. **Confound** — outcome is a function of (writing quality × task difficulty × agent
   capability × luck). Easy tasks let vague prompts land; hard tasks make clear prompts
   loop. Survival rewards easy tasks, not good writing.
2. **Noise** — n=35 at a 47% base rate has a ~±16pt 95% interval. The ranking is
   unstable at these sample sizes. (`MIN_PATTERN_N = 3` is far too low for ranking;
   raise the rankable bar to n≥30 or attach Wilson score intervals to every rate.)

**The rule a good tool must obey: never punish a clear prompt that hit a hard task.**
Intrinsic quality and outcome are correlated, not the same. Two lenses, kept separate.

---

## 2. The INTRINSIC lens — six scorable dimensions

Grounded in real standards, not invented rules:

- **ASD-STE100 Simplified Technical English** — 53 writing rules, ~900-word controlled
  dictionary (one meaning, one part of speech per word); max 20 words/sentence in
  procedures, 25 in description; one instruction per sentence; active voice; direct
  commands. ([asd-ste100.org](https://asd-ste100.org/), [ASD Europe](https://www.asd-europe.org/standards-specifications/simplified-technical-english/), [Wikipedia](https://en.wikipedia.org/wiki/Simplified_Technical_English))
- **ISO 24495-1:2023 Plain language — governing principles** — content must be
  *findable, understandable, usable, consistent*. ([iso.org](https://www.iso.org/standard/78907.html), [IPL Federation](https://www.iplfederation.org/iso-standard/))
- **US Federal Plain Language Guidelines / Plain Writing Act 2010** — active voice
  naming the actor; sentences averaging 15–20 words; definite, concrete, everyday words.
  ([plainlanguage.gov guidelines](https://github.com/GSA/plainlanguage.gov/blob/main/_pages/guidelines/conversational/use-active-voice.md), [digital.gov plain-language guide](https://digital.gov/guides/plain-language/writing))
- **Gopen & Swan, "The Science of Scientific Writing" (American Scientist, 1990)** —
  meaning is what the READER constructs; each unit of discourse makes ONE point; the
  emphatic material belongs in the stress position (point first / end of unit).
  ([full text PDF](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf))

A prompt is a **procedure** (an instruction to an agent); a note is a **description**
(a message to a future reader, often yourself). STE's procedure/description split maps
exactly. The dimensions:

| # | Dimension | Measure | Standard | Where it fails |
|---|-----------|---------|----------|----------------|
| 1 | **Stated intent** — an imperative verb up front (add/fix/read/build) | deterministic: `_intent()` (exists in `contract/deterministic.py`) | STE + plain-language active voice ("name the actor and the act") | musings/questions have no imperative and can still be good notes |
| 2 | **Concrete object** — names a file, path, repo, or noun the agent can locate | deterministic: `_objects()` + `_FILE_RE` (exist) | plain language: "definite, concrete" words | punishes legitimately abstract asks ("what's our strategy") |
| 3 | **Done-condition** — states a check, test, or "done when" | deterministic: `_CHECK_RE` (exists) | STE one-instruction discipline; eval-first canon | some tasks are exploratory; no done-condition is honest there |
| 4 | **Sentence discipline** — mean words/sentence ≤20 (prompt) / ≤25 (note); ≤1 imperative per sentence | deterministic: split on `.!?\n`, count words; count imperative verbs per sentence | ASD-STE100 rules (20/25-word limits, one instruction per sentence) | terse ≠ clear: a 5-word vague prompt passes; gate with dim 2 |
| 5 | **Vagueness markers** — dangling pronouns opening the text ("it", "that thing", "this"), hedges ("somehow", "maybe", "kind of"), unresolved deixis | deterministic: small lexicon + position check (opener starting with a pronoun that has no in-text referent) | plain language "definite, concrete"; the existing `no-object` tag, sharpened | sarcasm/shorthand between long-term collaborators reads vague but works |
| 6 | **Goal-sufficiency** — could a stranger (human or agent) execute/understand this with NO other context? | **light judge**: one rubric call, 3-point scale (self-sufficient / needs session context / not executable), with the judge quoting the missing piece | ISO 24495-1 "usable"; Gopen & Swan reader-construction | the one genuinely model-shaped dimension; judge drift needs a frozen rubric + spot-audit |

**Notes need one extra dimension (7): Findability/structure** — point stated in the
first two lines, headings present for >150-word notes, one idea per paragraph. Measure:
deterministic (position of first imperative/claim sentence; heading count vs length).
Standard: ISO 24495-1 *findable*; Gopen & Swan stress position. `coach.py` is
prompts-only today; the method must not be.

**Deliberately excluded: Flesch-Kincaid and kin.** Surface formulas have weak validity
on short texts and don't correlate well with human judgment ([validity study](https://www.richtmann.org/journal/index.php/mjss/article/download/11036/10649/41930), [Readable on F-K](https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/)).
A prompt is 8–60 words; grade-level math on that is noise. Acceptable as a coarse
signal on long notes only, never on prompts.

---

## 3. Combining the lenses — a 2×2, never one blended number

Score intrinsic (dims 1–5 as 0/1 flags, sum 0–5; judge dim 6 separately) and outcome
(the existing tier: commit / artifact / none) **independently**, then read the quadrant:

| | **Survived** | **Died** |
|---|---|---|
| **Intrinsically clear** | ✓ Working pattern — do more | **Hard task, not bad writing. Do NOT coach this.** Investigate the task, the agent, or the tooling |
| **Intrinsically vague** | Easy task or lucky — do not learn from it | ✗ The coachable bucket: rewrite THESE |

- **Outcome lens** validates patterns *in aggregate* (n≥30, with intervals). It answers
  "which habits correlate with landing work here."
- **Intrinsic lens** coaches *individual pieces of writing*. It answers "is this
  well-written," independent of whether the day was hard.
- A blended single score would re-import the confound through the back door. Two
  numbers, one quadrant label.

**Where each lens fails, honestly:**
- *Outcome:* cross-session reverts invisible; answer-shaped payoffs read as "died";
  easy tasks inflate vague patterns; sample sizes lie without intervals (all already
  admitted in `coach.py`'s docstring — keep that honesty).
- *Intrinsic:* checkbox-clarity is gameable (a template-stuffed prompt scores 5/5 and
  can still be wrong about the world); it can't see factual correctness or whether the
  task was worth doing; shared-context shorthand scores unfairly low; the judge (dim 6)
  is the only non-reproducible part and must be frozen + spot-audited against Oscar's
  own verdicts.

---

## 4. Implementation order (smallest first)

1. Raise `MIN_PATTERN_N` 3→30 for *ranking* (keep 3 for display with an interval).
2. Add dims 4–5 (sentence discipline, vagueness markers) as new tags in
   `prompt_patterns()` — pure regex, zero new dependencies.
3. Emit the 2×2 quadrant per episode in the coach report: intrinsic 0–5 × tier.
4. Notes lane: point-first + structure checks over the vault (dim 7).
5. Only then the judge (dim 6): one frozen rubric, sampled (not every prompt),
   audited monthly against a hand-labelled set of ~30.

**Verdict, restated:** easy to digest. 6 of 7 dimensions are deterministic; the
existing code already implements three of them. The judge earns its complexity only for
goal-sufficiency, and only after the free checks are shipped.
