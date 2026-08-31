# If you re-record: exactly what changes, and nothing else

Written 31 Aug after the deploy landed. **The diagram redesign does NOT touch the film** —
the architecture image is never on camera (`grep -i architecture demo/demo-final.srt` → 0 hits),
so it is a Devpost attachment only.

**Only two spoken lines are wrong in the shipped cut.** Both say the record is append-only.
It is not: the API never deletes, but closing a hold rewrites that clearance in place. Every
text surface now says the true thing; only the narration still says the false one.

## Cue 33 — 00:01:40.494 → 00:01:43.242 (2.75s)

Now says:
Firestore holds every clearance as an append only document.

Say instead:
Firestore holds every clearance as its own document.

## Cue 47 — 00:02:28.642 → 00:02:30.556 (1.91s)

Now says:
And the record, exportable, append only.

Say instead:
And the record, exportable, every verdict kept.

## Two other things the shot list flags, both picture not voice

- **2:22 to 2:52** — the narration names the Google-stack tab, the queue and the audit while the
  picture stays on the record detail. Cause was the `?record=` console loop, since fixed. A
  re-capture now follows the words.
- **2:52** — the Policy panel shows `report-only` for about a second because the box had not
  finished loading, while the narrator says "Enforce mode" and live `/policy` returns `enforce`.
  A re-capture against the deployed revision shows `enforce`.

## The ruling this replaces

If you do NOT re-record, ship as-is. That was the standing recommendation and it is still sound:
the console corrects itself in public, which is the thesis. This file exists only so that a
re-record fixes the right four things and changes nothing else.

**Re-capture against the CURRENT revision.** Live `/hold/` must hash to
`12e0db0982ed91c53c0c0c9ae9e492482bb536b83bfde2f68939f5c032e99eec` before you roll.
