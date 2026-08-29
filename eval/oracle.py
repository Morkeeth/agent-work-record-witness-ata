#!/usr/bin/env python3
"""The frozen probe oracle — how this eval runs offline without lying about it.

Both arms answer "is this sha a commit here?" and "does this path exist here?". Those are
OBSERVATIONS OF THE WORLD, and the world in question is 82 git repositories on one laptop.
Running them live would make the eval unreproducible for anyone else; running them against
a synthetic repo would make it measure a repo nobody has.

So the observation is recorded once (`build_oracle.py`) and replayed forever. What is
substituted is the EFFECT — what `git cat-file -t` returned — and never a RULE: every
regex, every scoping decision, the sibling-search policy and the refusal categories all run
for real, in `gate/outcome_gate.py`, unmodified. `eval/out/equivalence.txt` is the receipt
that replay and live agree verdict-for-verdict on the machine where the recording was made.

A replay miss RAISES. A probe oracle that returns a default for an unknown key would grade
whatever default it happened to pick, silently.
"""

from __future__ import annotations

import json
import os
import subprocess

SEP = " ||| "


class _Result:
    """The shape gate/outcome_gate.py::_sh returns. returncode 127 is reserved by that
    module for 'the probe binary is missing' and changes the verdict, so replay must never
    invent it."""

    def __init__(self, stdout: str = "", returncode: int = 0, stderr: str = ""):
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = stderr


class Oracle:
    def __init__(self, data: dict, record: bool = False):
        self.data = data
        self.record = record
        self.data.setdefault("git_probes", {})
        self.data.setdefault("path_probes", {})

    def sh(self, args, repo):
        key = repo + SEP + " ".join(args)
        hit = self.data["git_probes"].get(key)
        if hit is None:
            if not self.record:
                raise KeyError(
                    "probe not in the frozen oracle: " + repr(key) +
                    ". Rebuild with eval/build_oracle.py on a machine that has these "
                    "repos; a missing probe is never defaulted.")
            r = _live(args, repo)
            hit = {"stdout": r.stdout, "returncode": r.returncode}
            self.data["git_probes"][key] = hit
        return _Result(hit["stdout"], hit["returncode"])

    def exists(self, path: str) -> bool:
        hit = self.data["path_probes"].get(path)
        if hit is None:
            if not self.record:
                raise KeyError("path probe not in the frozen oracle: " + repr(path))
            hit = os.path.exists(path)
            self.data["path_probes"][path] = hit
        return bool(hit)


def _live(args, repo):
    try:
        return subprocess.run(args, cwd=repo, capture_output=True, text=True)
    except (FileNotFoundError, NotADirectoryError) as e:
        return _Result("", 127, "probe binary missing: %s" % (getattr(e, "filename", args[0]),))


class _OsShim:
    """Stands in for the `os` name inside gate/outcome_gate.py for the duration of a call.

    Only `path.exists` is redirected. `path.join` is the real one; `environ` is empty
    because nothing in check_report reads it and an eval must not inherit the shell.
    """

    class _Path:
        def __init__(self, oracle):
            self._o = oracle
            self.join = os.path.join

        def exists(self, p):
            return self._o.exists(p)

    def __init__(self, oracle):
        self.path = _OsShim._Path(oracle)
        self.environ = {}


class patched:
    """`with patched(oracle):` — outcome_gate observes the oracle instead of the disk."""

    def __init__(self, oracle):
        self.oracle = oracle

    def __enter__(self):
        from gate import outcome_gate as og
        self._og = og
        self._sh, self._os = og._sh, og.os
        og._sh = self.oracle.sh
        og.os = _OsShim(self.oracle)
        return self.oracle

    def __exit__(self, *exc):
        self._og._sh, self._og.os = self._sh, self._os
        return False


def load(path: str) -> Oracle:
    with open(path) as fh:
        return Oracle(json.load(fh), record=False)
