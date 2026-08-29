#!/usr/bin/env python3
"""Small-sample statistics. stdlib only, no scipy, no network.

n = 40. A bare point estimate at this n is a decoration, so nothing here returns one
without an interval beside it.
"""

from __future__ import annotations

import math

Z95 = 1.959963984540054


def wilson(k: int, n: int, z: float = Z95):
    """95% Wilson score interval for a binomial proportion.

    Wilson rather than normal-approximation because the normal interval is badly wrong
    near 0 and 1 at small n — and several cells here are expected to sit near 0.
    """
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def mcnemar_exact(b: int, c: int):
    """Exact two-sided McNemar (binomial sign test on the discordant pairs).

    b = A correct and B wrong; c = A wrong and B correct. The arms see identical items, so
    the paired test is the right one — an unpaired chi-square would throw away the pairing
    and widen the test for no reason. Exact rather than the chi-square approximation
    because b + c will be single digits.
    """
    n = b + c
    if n == 0:
        return {"b": b, "c": c, "n_discordant": 0, "p": 1.0,
                "note": "no discordant pairs: the arms agreed on every item"}
    lo = min(b, c)
    tail = sum(math.comb(n, k) for k in range(lo + 1)) * (0.5 ** n)
    p = min(1.0, 2 * tail)
    return {"b": b, "c": c, "n_discordant": n, "p": p}
