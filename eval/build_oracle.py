#!/usr/bin/env python3
"""Build the frozen probe oracle. Run ONCE, on the machine that has the repos.

    python3 eval/build_oracle.py [--code-root ~/CODE]

This is the only machine-bound step in the eval. It records what `git cat-file -t` and
`stat` actually returned for every probe either arm makes over the 40-row corpus, plus:

  * the sibling repo list (machine state, frozen so replay searches the same 82 repos);
  * for every sha, whether it is a commit ANYWHERE on this disk — the gold existence rule;
  * `git log -1` for each sibling-resolved DONE sha, so a human can judge whether the
    resolved commit plausibly is the work the agent claimed. The SUBJECT is redacted to a
    sha256 commitment in the shipped file (private-repo content); the plaintext stays in
    the uncommitted map, so the reader who has the map still gets the judgement;
  * the pre-registered NEGATIVE CONTROL: 200 seeded random 7-hex strings pushed through the
    identical 82-repo search. If those resolve at a real rate, sibling resolution is noise
    and our arm's advantage is an artifact. Falsifier 3 in eval/README.md.
  * a drift check against the `ok` field recorded in the corpus on 2026-08-27 — two days of
    rebasing can move it, and inheriting either number silently would be the defect this
    repo is about.

`eval/run_eval.py` never calls this. The table reproduces from the committed JSON alone.

PSEUDONYMISATION. This repository is public and the 82 sibling repos are not, so nothing
here writes a real directory name. Every repo path becomes a stable opaque label
(`/code/repo-07`), the label is what keys the oracle and what the shipped corpus carries,
and the real path is used only as the working directory of a live probe. The real -> label
table (and the plaintext of the redacted commit subjects) is written OUTSIDE the repo, to
`~/.claude/ata-eval-repo-map.json` or `$ATA_EVAL_REPO_MAP`, and is never committed:
committing it would undo the whole point. See eval/README.md.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from eval import arms, oracle as orc  # noqa: E402

CORPUS = os.path.join(ROOT, "fixtures", "corpus-sample-40.json")
ORACLE = os.path.join(HERE, "fixtures", "sha_oracle.json")
EQUIV = os.path.join(HERE, "out", "equivalence.txt")

NEG_CONTROL_N = 200
NEG_CONTROL_SEED = 20260829

LABEL_ROOT = "/code"
MAP_PATH = os.environ.get("ATA_EVAL_REPO_MAP") or os.path.expanduser(
    "~/.claude/ata-eval-repo-map.json")


class RepoMap:
    """real path <-> opaque label. Lives outside the repo; never committed.

    Labels are assigned once and never reused, so a rebuild that sees the same repos
    produces byte-identical keys and the committed corpus keeps resolving.
    """

    def __init__(self, path=MAP_PATH):
        self.path = path
        try:
            self.data = json.load(open(path))
        except (OSError, ValueError):
            self.data = {}
        self.data.setdefault("what", "real path -> opaque label for the ATA eval "
                                     "artifacts. NOT COMMITTED: the repo is public and "
                                     "these names include private repositories.")
        self.data.setdefault("repo", "Morkeeth/agent-work-record-witness-ata")
        self.data.setdefault("code_root", {})
        self.data.setdefault("labels", {})
        self.data.setdefault("redacted_commit_subjects_sha256_16", {})

    def label(self, real):
        lab = self.data["labels"].get(real)
        if lab is None:
            n = len(self.data["labels"]) + 1
            lab = "%s/repo-%02d" % (LABEL_ROOT, n)
            self.data["labels"][real] = lab
        return lab

    def note_code_root(self, real):
        self.data["code_root"][real] = LABEL_ROOT

    def real(self, s):
        """Translate a label (or a path under one) back to the real directory."""
        for real, lab in sorted(self.data["labels"].items(), key=lambda kv: -len(kv[1])):
            if lab in s:
                s = s.replace(lab, real)
        return s

    def redact_subject(self, subject):
        digest = hashlib.sha256(subject.encode("utf-8")).hexdigest()[:16]
        self.data["redacted_commit_subjects_sha256_16"][digest] = subject
        return "[subject redacted \u2014 sha256:%s]" % digest

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as fh:
            json.dump(self.data, fh, indent=1, sort_keys=True)
        os.chmod(self.path, 0o600)


def git_repos(code_root):
    root = os.path.expanduser(code_root)
    return [os.path.join(root, d) for d in sorted(os.listdir(root))
            if os.path.exists(os.path.join(root, d, ".git"))]


def _cat(sha, repo, rmap):
    try:
        r = subprocess.run(["git", "cat-file", "-t", sha], cwd=rmap.real(repo),
                           capture_output=True, text=True)
        return r.stdout.strip() == "commit"
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-root", default="~/CODE")
    a = ap.parse_args()

    corpus = json.load(open(CORPUS))
    rmap = RepoMap()
    rmap.note_code_root(os.path.expanduser(a.code_root))
    real_repos = git_repos(a.code_root)
    repos = [rmap.label(r) for r in real_repos]
    rmap.save()
    print("repos on disk: %d (labels %s .. %s)" % (len(repos), repos[0], repos[-1]))
    for it in corpus:
        if not re.fullmatch(r"/code/repo-\d+", it["cwd"]):
            raise SystemExit("corpus cwd %r is not a pseudonym label. The shipped corpus "
                             "must carry labels; see eval/README.md." % it["cwd"])
        if it["cwd"] not in repos:
            raise SystemExit("corpus cwd %r has no entry in %s" % (it["cwd"], rmap.path))

    data = {
        "built_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "built_by": "eval/build_oracle.py",
        "code_root": LABEL_ROOT,
        "sibling_repos": repos,
        "corpus": "fixtures/corpus-sample-40.json",
        "git_probes": {},
        "path_probes": {},
    }
    o = orc.Oracle(data, record=True, realpath=rmap.real)

    # 1. Record every probe both arms make, in every configuration reported.
    with orc.patched(o):
        for item in corpus:
            arms.arm_a(item["ctx"], item["cwd"], o)
            for cfg in arms.ARM_B_CONFIGS.values():
                arms.arm_b(item["ctx"], item["cwd"], o, repos, cfg)
    print("recorded %d git probes, %d path probes"
          % (len(data["git_probes"]), len(data["path_probes"])))

    # 2. Gold existence: is this sha a commit anywhere on this disk?
    anywhere, receipts, drift = {}, {}, []
    for item in corpus:
        sha = item["value"]
        if sha in anywhere:
            continue
        in_cwd = _cat(sha, item["cwd"], rmap)
        found_in = item["cwd"] if in_cwd else None
        if not in_cwd:
            for r in repos:
                if _cat(sha, r, rmap):
                    found_in = r
                    break
        anywhere[sha] = found_in is not None
        if found_in and found_in != item["cwd"]:
            log = subprocess.run(["git", "log", "-1", "--format=%H %cI %s", sha],
                                 cwd=rmap.real(found_in), capture_output=True,
                                 text=True).stdout.strip()[:220]
            # The commit SUBJECT is private-repo content. Several of these shas resolve
            # into private repositories, and one of them into a repository whose commit
            # messages are personal material that must never reach a public repo. Keep
            # the sha and the date, commit to the subject with a hash so the redaction is
            # verifiable rather than a rewrite, and keep the plaintext in the uncommitted
            # map so a human with the map can still read it.
            m = re.match(r"^([0-9a-f]{7,40}) (\S+) (.*)$", log)
            if m:
                log = "%s %s %s" % (m.group(1), m.group(2), rmap.redact_subject(m.group(3)))
            receipts[sha] = {"label": item["label"], "recorded_cwd": item["cwd"],
                             "resolved_in": found_in, "prefix_len": len(sha),
                             "git_log_1": log}
        if in_cwd != bool(item["ok"]):
            drift.append({"sha": sha, "cwd": item["cwd"],
                          "ok_recorded_2026_08_27": item["ok"], "in_cwd_today": in_cwd})
    data["sha_is_commit_anywhere"] = anywhere
    data["sibling_resolution_receipts"] = receipts
    data["drift_vs_corpus_ok_field"] = drift
    print("gold: %d/%d shas resolve somewhere; %d sibling-resolved; %d drifted since 08-27"
          % (sum(anywhere.values()), len(anywhere), len(receipts), len(drift)))

    # 3. Negative control (falsifier 3).
    rng = random.Random(NEG_CONTROL_SEED)
    hits = []
    for _ in range(NEG_CONTROL_N):
        fake = "".join(rng.choice("0123456789abcdef") for _ in range(7))
        for r in repos:
            if _cat(fake, r, rmap):
                hits.append({"sha": fake, "repo": r})
                break
    data["negative_control"] = {
        "n": NEG_CONTROL_N,
        "seed": NEG_CONTROL_SEED,
        "prefix_len": 7,
        "repos_searched": len(repos),
        "hits": len(hits),
        "rate": len(hits) / NEG_CONTROL_N,
        "hit_examples": hits[:10],
        "threshold_declared_before_run": 0.05,
        "rule": ("if rate >= 0.05, a 7-hex sibling match is noise-dominated, every "
                 "sibling-resolved item is discounted and arm B's edge is reported "
                 "as unsupported (eval/README.md falsifier 3)"),
    }
    print("negative control: %d/%d random 7-hex strings resolved (%.2f%%)"
          % (len(hits), NEG_CONTROL_N, 100 * len(hits) / NEG_CONTROL_N))

    rmap.save()
    os.makedirs(os.path.dirname(ORACLE), exist_ok=True)
    with open(ORACLE, "w") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
    print("wrote %s" % ORACLE)

    # 4. Equivalence receipt: replay must equal live, verdict for verdict.
    cfg = arms.ARM_B_CONFIGS["B (headline)"]
    live_o = orc.Oracle({"git_probes": {}, "path_probes": {}}, record=True,
                        realpath=rmap.real)
    live, replay = [], []
    with orc.patched(live_o):
        for item in corpus:
            live.append(arms.item_answer(
                arms.arm_b(item["ctx"], item["cwd"], live_o, repos, cfg), item["value"]))
    frozen = orc.load(ORACLE)
    with orc.patched(frozen):
        for item in corpus:
            replay.append(arms.item_answer(
                arms.arm_b(item["ctx"], item["cwd"], frozen, repos, cfg), item["value"]))
    same = live == replay
    os.makedirs(os.path.dirname(EQUIV), exist_ok=True)
    with open(EQUIV, "w") as fh:
        fh.write("ORACLE-vs-LIVE EQUIVALENCE RECEIPT\n")
        fh.write("built %s on %s\n\n" % (data["built_utc"], data["code_root"]))
        fh.write("Arm B (headline config) was run twice over the same 40 rows: once against\n"
                 "live git on this disk, once against the frozen oracle. If these disagree,\n"
                 "the oracle substituted a RULE and not merely an EFFECT, and the eval is void.\n\n")
        for it, l, r in zip(corpus, live, replay):
            fh.write("%-42s %-8s live=%-8s replay=%-8s %s\n"
                     % (it["value"][:40], it["label"], l, r, "OK" if l == r else "MISMATCH"))
        fh.write("\nRESULT: %s (%d/%d identical)\n"
                 % ("IDENTICAL" if same else "MISMATCH",
                    sum(1 for l, r in zip(live, replay) if l == r), len(corpus)))
    print("equivalence: %s -> %s" % ("IDENTICAL" if same else "MISMATCH", EQUIV))
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
