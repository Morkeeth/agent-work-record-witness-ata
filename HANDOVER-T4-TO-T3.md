# T4 → T3 handover · 2026-08-27

**T4 is off this tree.** Coordinator ruled it after I reported a commit collision. **That report was
wrong, and correcting it is the first item here.**

---

## 1. RETRACTION — I did not sweep your rename. Verified at the object.

I told the coordinator, twice, that my commits had swept your repo rename
(`hack-fleet-ata` → `agent-work-record-witness-ata`) across 8 files, and I **amended two commit
messages to say so**. Checked properly:

```
$ git show --name-only --format="" 4590f57
README.md · SUBMISSION-PACK.md · docs/CORPUS-MEASUREMENT-2026-08-27.md
docs/ENTERPRISE-CASE-2026-08-27.md · gate/corpus_scan.py

$ git show --name-only --format="" bd2bc65
README.md · docs/ENTERPRISE-CASE-2026-08-27.md · gate/corpus_scan.py
gate/outcome_gate.py · tests/test_hard_wedge.py

$ git log --format='%h %s' -- examples/customer-workflow.yml
ccda627  Ship the gate as a composite action…      (19:41, mine, before your rename existed)
```

**Both commits contain only my own files. No commit in this repo carries your rename.** It is
still entirely uncommitted in the working tree, intact, yours to commit whole.

I had read `git diff HEAD~1 --stat` and taken its file list as my commit's contents. It was not,
and **I do not know what that diff was actually showing** — I am not going to invent a mechanism to
explain it, which is the same discipline the rest of this lane ran on. What is verifiable is the
`--name-only` output above.

### What that leaves for you to fix

**Two of my commit messages now carry a false disclosure**, in their closing paragraphs:

| commit | the false paragraph |
|---|---|
| `4590f57` | *"NOT MINE, AND SWEPT IN BY ACCIDENT… also contains T3's repo rename…"* |
| `bd2bc65` | *"NOT MINE, SWEPT IN AGAIN…"* |

Both are wrong. I did not amend them because the ruling took me off this tree and rewriting history
here is a tree write. **You own the tree — either amend them or leave a note; the coordinator has
the call.** Nothing in the *content* of either commit is affected.

## 2. Your rename is uncommitted and safe

Modified, untracked by any commit, exactly as you left it:

```
.github/workflows/outcome-gate.yml   docs/COLD-START-REPORT.md
docs/TESTCO-RUN-2026-08-27.md        docs/internal/CURSOR-LOG.md
docs/internal/FOR-CLAUDE.md          docs/internal/NEXT-STEPS.md
docs/internal/OSCAR-SUBMIT.md        examples/customer-workflow.yml
```

**Commit it whole.** There is no half-rename anywhere in the history to reconcile.

## 3. What I own, so you do not re-derive it

The measurement path is `gate/corpus_scan.py` — **one path, coordinator-ruled**. Do not add a
second. Your `gate/corpus_report.py` and `surface/fleet-report*.{html,json}` are view-side and
untracked; if they call anything, call `scan()`.

Its payload now carries, for your screen:

- `corpus_total_messages` · `examined_messages` · `examined_filter` · `messages_in_a_live_repo` —
  **three populations, print them together.** The heading used to say 144,306 while the scan
  examined 78,618.
- `claims` — 44 receipts (19 sha + 25 path), each with `probe` and `evidence`. This is the click
  target: *`git cat-file -t 48811937` → NOT a commit in this repo, nor in any of the 83 sibling
  repos checked*.
- `claims_pass` is `"corrected"`, and `claims_listing_rule` states that PASS rows and every RAW-pass
  row are counted but not listed. **Do not ship RAW or CORRECTED without saying which.**
- `claims_not_listed` — so the screen can state what it omitted instead of hardcoding a sentence.
- `path_claims_not_checkable_by_reason` — **render these**. A drop with no visible reason is the
  flattering version.

**Two rows stay listed and unprobed on purpose:** `wrote _jed.py` and `wrote needs.ts`. Nobody has
checked them. Label them unprobed; do not guess either way.

**Current numbers:** RAW 247 sha claims / 103 disagree / 41.7% · CORRECTED 236 / 19 / **8.1%**.

## 4. Not mine

The empty untracked file `NOT` at repo root, created 22:41. Not mine, not the coordinator's. Tree
owner's call.

*T4. Read-only from here.*
