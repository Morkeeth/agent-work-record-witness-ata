"""ADJACENCY — the claim class where every individual fact is true.

Every other check in this inbox asks a question about ONE claim. Did the repo
disprove it (CONTRADICTED-BY-REPO). Is there anything in the trace that could
support it (NO-EVIDENCE). Did the agent say done without producing a durable
artifact (ILLUSION-OF-DONE). Each one takes a sentence and holds it against the
world.

Adjacency is the failure that survives all of them, because it needs no false
sentence. An agent writes:

    22 of 23 projects have a phase on disk
    21 no repo · 1 unknown

Both lines are true. Check each number against its source and each passes. Sign
them, hash them, attest them — every one of them really happened. And the
report says 96% where the truth is 50%, because the denominator quietly
excluded the cases named directly underneath it.

**Two figures placed next to each other assert a relationship, and nothing in
this inbox — or in the attestation tools this space is otherwise building —
checks that claim.**

## Where the class came from

Eight instances in one product in a single day, found by hand:

    "22 of 23" above "21 no repo · 1 unknown"     96% shown, 50% true
    "3 artifacts · 3 unseen" above four rows      3 deliveries of 2 files
    "PROJECT PULSE · 54 repos" above 60 rows      count is not its own list
    a focal "0" above two overdue rows            two lists, one headline

Three were on surfaces already reviewed and approved. Three were written the
same day by the person who had just named the class. One was created by the fix
for another. One was inside the checking tool itself. **Knowing the class does
not confer immunity**, which is the argument for making it a program.

## What this does not do

It reads shape, not meaning. It cannot know that "users" and "sessions" count
different things. It finds the arithmetic and structural cases and prints both
sides verbatim so a human dismisses a wrong flag in one read. Every false
positive it produced in development came from a number that looked like a count
and was an ADDRESS — "3. COSMETIC" numbers a finding, "### 1.7" numbers a
section, "Phase 1" labels a phase — so those are excluded by shape.
"""
import re

# "22 of 23", "3 of 4 surfaced"
_FRACTION = re.compile(r"\b(\d[\d,]*)\s+of\s+(\d[\d,]*)\b")

# "21 no repo · 1 unknown", "12 held, 4 failed" — a breakdown into named parts
_PARTS = re.compile(r"\b(\d[\d,]*)\s+[a-z][a-z -]{2,24}?(?=\s*[·,]|\s*$)", re.I)

# A markdown/plain list item, or a table row
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\|)")

_INT = re.compile(r"(\d[\d,]*)")

# "4 repos", "3 artifacts" — a standalone number counting a plural noun. Not
# "T2", not "4am", not "gemma4", not "0.4", not a SHA.
_COUNT_OF = re.compile(
    r"(?<![\w.])(\d[\d,]*)\s+([a-z]{3,}(?:s|es)|items?|things?)\b", re.I
)

# A number that is an ADDRESS, not a count.
_ORDINAL = re.compile(r"^\s*(?:\*\*)?\d+(?:\.\d+)*[.)]\s")
_HEADING_NUM = re.compile(r"^\s*#{1,6}\s*\d+(?:\.\d+)*[.)]?\s")
_LABEL_NUM = re.compile(
    r"\b(?:phase|step|part|stage|rung|slice|tier|chapter|section|round|v|version)\s*\d",
    re.I,
)

# "4 tabs + 1 action" — a heading may state a sum.
_SUM = re.compile(r"(\d[\d,]*)\s*[a-z][a-z -]{0,20}?(?=\s*\+)", re.I)


def _n(s):
    return int(s.replace(",", ""))


def find_adjacency(text):
    """Return findings: dicts with kind, line (1-indexed), a, b, why."""
    lines = text.split("\n")
    out = []

    for i, line in enumerate(lines):
        if not any(c.isdigit() for c in line):
            continue

        # ── a fraction whose excluded cases are restated right beneath it ──
        frac = _FRACTION.search(line)
        if frac:
            kept, total = _n(frac.group(1)), _n(frac.group(2))
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            parts = [_n(m.group(1)) for m in _PARTS.finditer(nxt)]
            if len(parts) >= 2:
                excluded = sum(parts)
                if excluded > total - kept:
                    out.append({
                        "kind": "DENOMINATOR-EXCLUDES-ITS-FAILURES",
                        "line": i + 1,
                        "a": line.strip(),
                        "b": nxt.strip(),
                        "why": (
                            '"%d of %d" leaves %d unaccounted, and the next line '
                            "names %d. The denominator does not contain the cases "
                            "printed under it — the honest figure is %d of %d."
                            % (kept, total, total - kept, excluded, kept, kept + excluded)
                        ),
                    })

        # ── a count that heads a list of a different length ────────────────
        is_address = (
            _ORDINAL.search(line) or _HEADING_NUM.search(line) or _LABEL_NUM.search(line)
        )
        # THE COUNT MUST BE A COUNT OF SOMETHING, and this rule did not require
        # that. Run over 4,767 real agent reports it fired 131 times at roughly
        # 8% precision — "T2 came back", "4am checkpoint", "the 5x reply lever",
        # "smoke_gemma4.py", "costs 0.4", a bare SHA. Every one a number glued
        # to a word, or a time, or an id.
        #
        # A count is a STANDALONE number followed by a plural noun: "4 repos",
        # "3 artifacts", "12 findings". That is the whole shape, and requiring
        # it is what makes the rule survive contact with prose.
        head = None if is_address else _COUNT_OF.search(line)
        if head and not _LIST_ITEM.search(line):
            claimed = (
                sum(_n(m.group(1)) for m in _INT.finditer(line))
                if _SUM.search(line)
                else _n(head.group(1))
            )
            n, table_rows, j = 0, 0, i + 1
            while j < len(lines) and (_LIST_ITEM.search(lines[j]) or not lines[j].strip()):
                l = lines[j]
                if _LIST_ITEM.search(l):
                    if l.strip().startswith("|"):
                        table_rows += 1
                        # row 1 is the header, row 2 the |---| separator.
                        if table_rows > 2:
                            n += 1
                    else:
                        n += 1
                elif n > 0 or table_rows > 0:
                    break
                j += 1
            # AND THE COUNT MUST BE THE LAST THING SAID BEFORE THE LIST.
            #
            # Measured on 4,775 real agent reports: requiring a plural noun took
            # this from 131 findings at ~8% precision to 34 at ~21%. Still
            # mostly noise, because real prose carries numbers everywhere — "5
            # claims, 2 failed, both ours:" heads a list of the 2, not the 5.
            #
            # A heading that counts its own list ends with the count. Anything
            # earlier in the sentence is a different subject, and this rule
            # cannot tell which. Everything after this filter is a count sitting
            # directly against the list it introduces.
            tail = line.rstrip().rstrip(":—-").rstrip()
            counts_the_list = tail.endswith(head.group(0).strip()) or (
                len(tail) - head.end() <= 12
            )
            if counts_the_list and n >= 2 and claimed != n and abs(claimed - n) <= max(3, n):
                out.append({
                    "kind": "COUNT-IS-NOT-ITS-LIST",
                    "line": i + 1,
                    "a": line.strip(),
                    "b": "%d item%s follow" % (n, "" if n == 1 else "s"),
                    "why": (
                        "The line says %d and the list under it has %d. If they "
                        "are not the same set, the heading has to say which one "
                        "it counts." % (claimed, n)
                    ),
                })

        # ── a total its own breakdown does not reach ───────────────────────
        # A MARKDOWN TABLE ROW IS NOT A TOTAL AND ITS NEIGHBOUR IS NOT A
        # BREAKDOWN. Both false positives this rule produced on the real corpus
        # were adjacent table rows — "| Precision pass | Queue 19 → 16 rows |"
        # read as a total, the row under it read as its parts.
        tot = (
            None
            if line.lstrip().startswith("|")
            else re.search(r"\b(?:total|all|overall)\D{0,12}(\d[\d,]*)", line, re.I)
        )
        if tot:
            total = _n(tot.group(1))
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            parts = [_n(m.group(1)) for m in _PARTS.finditer(nxt)]
            if len(parts) >= 2 and sum(parts) != total:
                out.append({
                    "kind": "PARTS-DO-NOT-SUM",
                    "line": i + 1,
                    "a": line.strip(),
                    "b": nxt.strip(),
                    "why": (
                        "Total says %d; the parts beneath it add to %d. One of "
                        "them is measuring something the other is not."
                        % (total, sum(parts))
                    ),
                })

    return out


def adjacency_checks(events):
    """Rows for the inbox, one per finding, over the agent's own prose.

    Runs on `claim_text` — what the agent WROTE, not what it did — because this
    is a defect of composition. It needs the paragraph, not the sentence, which
    is exactly why no per-claim check can see it.
    """
    rows = []
    for e in events:
        if e.get("kind") != "claim_text":
            continue
        for f in find_adjacency(e.get("text", "")):
            # `witness` is a dict elsewhere in this engine (line + tool). An
            # adjacency finding has no tool call behind it — the whole point is
            # that every tool call succeeded — so it is left absent rather than
            # stuffed with a string the renderer would try to index.
            rows.append({
                "line": e.get("line", 0) + f["line"] - 1,
                "verdict": "ADJACENT-FALSE",
                "text": f["a"],
                "why": "%s — %s [%s]" % (f["b"], f["why"], f["kind"]),
            })
    return rows
