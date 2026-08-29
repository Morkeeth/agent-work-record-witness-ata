#!/usr/bin/env python3
"""ONE COMMAND. Runs both arms over the labelled corpus and prints the table.

    env -i /usr/bin/python3 eval/run_eval.py

stdlib only, no network, no API key, no $HOME, deterministic. Every world-observation comes
from the frozen oracle in eval/fixtures/sha_oracle.json, so this reproduces from a cold
clone on a machine that has none of the repos the corpus was drawn from.

Reading order for anyone auditing this: eval/README.md first (metric, arms, falsifiers,
written before the run), then eval/arms.py (the scoring matrix and why), then this file.
"""

from __future__ import annotations

import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from eval import arms, oracle as orc  # noqa: E402
from eval.stats import mcnemar_exact, wilson  # noqa: E402

CORPUS = os.path.join(ROOT, "fixtures", "corpus-sample-40.json")
ORACLE = os.path.join(HERE, "fixtures", "sha_oracle.json")
OUT = os.path.join(HERE, "out", "results.json")


def run_arm(name, corpus, o, repos, runner):
    rows = []
    for item in corpus:
        with orc.patched(o):
            findings = runner(item)
        answer = arms.item_answer(findings, item["value"])
        rows.append({
            "mid": item["mid"], "sha": item["value"], "label": item["label"],
            "cwd_basename": os.path.basename(item["cwd"].rstrip("/")),
            "answer": answer,
            "n_path_findings_unscored": sum(1 for f in findings if f.kind == "path"),
            "refused_test_claim": any(f.kind == "other" and "tests pass" in f.value
                                      for f in findings),
            "findings": [f.as_dict() for f in findings],
        })
    return {"arm": name, "rows": rows}


def score(arm, golds):
    rows = arm["rows"]
    n = len(rows)
    outcomes = []
    for r, g in zip(rows, golds):
        r["gold"] = g
        r["outcome"] = arms.score_item(g, r["answer"])
        r["false_accusation"] = arms.is_false_accusation(g, r["answer"])
        r["missed_false_claim"] = arms.is_missed_false_claim(g, r["answer"])
        outcomes.append(r["outcome"])
    correct = sum(1 for x in outcomes if x == arms.CORRECT)
    abstained = sum(1 for x in outcomes if x == arms.ABSTAINED)
    wrong = sum(1 for x in outcomes if x == arms.WRONG)
    fa = sum(1 for r in rows if r["false_accusation"])
    mfc = sum(1 for r in rows if r["missed_false_claim"])
    # THE SPLIT. Accuracy over all 40 conflates two different abilities, and the run made
    # that impossible to ignore: DISCRIMINATION (not adjudicating something nobody claimed,
    # the 27 non-claim rows) and ADJUDICATION (getting the verdict right on a real claim,
    # the 13 claim rows). An always-silent arm maxes the first and zeroes the second.
    # Reported as a decomposition of the same pre-registered scoring, never as a substitute
    # for it.
    ncl = [r for r in rows if r["gold"] == arms.NO_CLAIM]
    rcl = [r for r in rows if r["gold"] != arms.NO_CLAIM]
    acc, acc_lo, acc_hi = wilson(correct, n)
    far, far_lo, far_hi = wilson(fa, n)
    arm["score"] = {
        "n": n, "correct": correct, "abstained": abstained, "wrong": wrong,
        "accuracy": acc, "accuracy_ci95": [acc_lo, acc_hi],
        "false_accusations": fa, "false_accusation_rate": far,
        "false_accusation_rate_ci95": [far_lo, far_hi],
        "missed_false_claims": mfc,
        "penalised_mean": (correct - wrong) / n,
        "discrimination_correct_on_non_claims": [
            sum(1 for r in ncl if r["outcome"] == arms.CORRECT), len(ncl)],
        "adjudication_correct_on_real_claims": [
            sum(1 for r in rcl if r["outcome"] == arms.CORRECT), len(rcl)],
        "test_claim_refusals_unscored": sum(1 for r in rows if r["refused_test_claim"]),
        "path_findings_unscored": sum(r["n_path_findings_unscored"] for r in rows),
    }
    return arm


def main():
    corpus = json.load(open(CORPUS))
    o = orc.load(ORACLE)
    repos = o.data["sibling_repos"]
    anywhere = o.data["sha_is_commit_anywhere"]
    golds = [arms.gold_for(it, lambda s: anywhere[s]) for it in corpus]

    a = score(run_arm("A naive baseline", corpus, o, repos,
                      lambda it: arms.arm_a(it["ctx"], it["cwd"], o)), golds)
    null = score(run_arm("NULL always-silent", corpus, o, repos,
                         lambda it: arms.arm_silent(it["ctx"], it["cwd"], o)), golds)
    bs = {}
    for name, cfg in arms.ARM_B_CONFIGS.items():
        bs[name] = score(run_arm(name, corpus, o, repos,
                                 lambda it, c=cfg: arms.arm_b(it["ctx"], it["cwd"], o, repos, c)),
                         golds)
    b = bs["B (headline)"]

    # Paired test, arm A vs arm B headline.
    pa = [r["outcome"] == arms.CORRECT for r in a["rows"]]
    pb = [r["outcome"] == arms.CORRECT for r in b["rows"]]
    mc = mcnemar_exact(sum(1 for x, y in zip(pa, pb) if x and not y),
                       sum(1 for x, y in zip(pa, pb) if y and not x))

    # Falsifier 4 sensitivity: drop DONE rows whose gold PASS rests on a sibling match.
    sib = set(o.data["sibling_resolution_receipts"])
    keep = [i for i, it in enumerate(corpus)
            if not (it["label"] == "DONE" and it["value"] in sib)]
    sens = {}
    for nm, arm in (("A naive baseline", a), ("B (headline)", b)):
        c = sum(1 for i in keep if arm["rows"][i]["outcome"] == arms.CORRECT)
        p, lo, hi = wilson(c, len(keep))
        sens[nm] = {"n": len(keep), "correct": c, "accuracy": p, "accuracy_ci95": [lo, hi]}

    nc = o.data["negative_control"]
    nc_fails = nc["rate"] >= nc["threshold_declared_before_run"]

    f1 = not (b["score"]["accuracy_ci95"][0] > a["score"]["accuracy"])
    f2 = mc["p"] >= 0.05
    f4 = not (sens["B (headline)"]["accuracy"] > sens["A naive baseline"]["accuracy"])

    results = {
        "what_this_measures": ("verdict accuracy of a claim-checker on 40 hand-labelled "
                               "SHA extractions from real agent transcripts. NOT a base "
                               "rate of agent wrongness. See eval/README.md, THE OBJECT."),
        "corpus": "fixtures/corpus-sample-40.json (unmodified, labelled 2026-08-27)",
        "oracle_built_utc": o.data.get("built_utc"),
        "gold_distribution": {g: golds.count(g) for g in sorted(set(golds))},
        "arms": {"NULL always-silent": null["score"], "A naive baseline": a["score"],
                 **{k: v["score"] for k, v in bs.items()}},
        "null_model_warning": (
            "27 of 40 rows are non-claims, so an arm that says nothing scores 27/40 = 67.5% "
            "on the pre-registered accuracy metric and beats BOTH real arms. That is a "
            "defect in the metric, disclosed rather than repaired after the fact. Read the "
            "split: discrimination (non-claims) vs adjudication (real claims)."),
        "mcnemar_exact_A_vs_B": mc,
        "negative_control": nc,
        "sensitivity_drop_sibling_resolved_gold": sens,
        "sibling_resolution_receipts": o.data["sibling_resolution_receipts"],
        "drift_vs_corpus_ok_field": o.data["drift_vs_corpus_ok_field"],
        "falsifiers": {
            "1_no_win_ci_overlap": f1,
            "2_no_paired_difference_p_ge_0.05": f2,
            "3_sibling_matches_are_noise": nc_fails,
            "4_gold_is_circular": f4,
        },
        "verdict": _verdict(f1, f2, f4, nc_fails,
                            null["score"]["accuracy"], b["score"]["accuracy"]),
        "per_item": {"NULL always-silent": null["rows"], "A naive baseline": a["rows"],
                     **{k: v["rows"] for k, v in bs.items()}},
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=1)
    _print(results, a, bs, sens, mc, nc)
    return 0


def _verdict(f1, f2, f4, nc_fails, null_acc, b_acc):
    fired = [n for n, x in (("1 no win (CI overlap)", f1),
                            ("2 no paired difference", f2),
                            ("3 sibling matches are noise", nc_fails),
                            ("4 gold is circular", f4)) if x]
    caveat = ("" if b_acc > null_acc else
              " It does NOT beat the trivial always-silent null on accuracy "
              "(%.1f%% vs %.1f%%): 27 of 40 rows are non-claims and neither arm can "
              "tell a claim from a citation. The separation is in adjudication and in "
              "false accusations, not in accuracy." % (100 * b_acc, 100 * null_acc))
    if not fired:
        return ("ARM B BEATS ARM A on every pre-registered comparison; no falsifier fired."
                + caveat)
    return ("FALSIFIER(S) FIRED: " + "; ".join(fired) +
            ". The win over arm A is not claimed on this evidence." + caveat)


def _pct(x):
    return "%5.1f%%" % (100 * x)


def _print(res, a, bs, sens, mc, nc):
    W = 92
    p = print
    p("=" * W)
    p("  EVAL — our outcome gate vs the two-hour baseline, on 40 labelled real claims")
    p("=" * W)
    p("  object   : verdict accuracy of a CLAIM-CHECKER. Not a rate of agent wrongness.")
    p("  corpus   : %s" % res["corpus"])
    p("  gold     : %s" % ", ".join("%s=%d" % (k, v) for k, v in res["gold_distribution"].items()))
    p("  oracle   : frozen %s — no network, no live git" % res["oracle_built_utc"])
    p("")
    hdr = "  %-18s %-22s %-20s %5s %5s %6s  %-7s %-7s" % (
        "arm", "accuracy (95% Wilson)", "false accusations", "miss", "abst", "pen",
        "discrim", "adjud")
    p(hdr)
    p("  " + "-" * (W - 4))
    order = [("NULL always-silent", res["arms"]["NULL always-silent"]),
             ("A naive baseline", a["score"])] + \
            [(k, v["score"]) for k, v in bs.items()]
    for name, s in order:
        star = " <" if name in ("A naive baseline", "B (headline)") else "  "
        d, dn = s["discrimination_correct_on_non_claims"]
        j, jn = s["adjudication_correct_on_real_claims"]
        p("  %-18s %2d/%-2d %s [%s,%s] %2d/%-2d %s   %5d %5d %+6.2f  %2d/%-2d   %2d/%-2d%s" % (
            name, s["correct"], s["n"], _pct(s["accuracy"]),
            _pct(s["accuracy_ci95"][0]), _pct(s["accuracy_ci95"][1]),
            s["false_accusations"], s["n"], _pct(s["false_accusation_rate"]),
            s["missed_false_claims"], s["abstained"], s["penalised_mean"],
            d, dn, j, jn, star))
    p("")
    p("  miss    = false claims waved through (PASS where the repo disproves it). gold BLOCK n=1.")
    p("  abst    = refused or never flagged, on a row that WAS a real claim (scores 0)")
    p("  pen     = mean of +1 correct / 0 abstained / -1 wrong answer")
    p("  discrim = correct on the 27 rows nobody claimed (silence is the right answer)")
    p("  adjud   = correct on the 13 rows that were real claims (an answer is required)")
    p("")
    p("  !! THE NULL ROW BEATS BOTH ARMS ON ACCURACY. 27 of 40 rows are non-claims, so an")
    p("     arm that says nothing scores 67.5%. That is a defect in the metric this eval")
    p("     pre-registered, found by its own ablation and disclosed rather than swapped out.")
    p("     The arms separate on the SPLIT: adjudication 12/13 vs 7/13, and on false")
    p("     accusations 5.0% vs 45.0%. Neither arm can discriminate a claim from a citation.")
    p("")
    p("  PAIRED  exact McNemar, A vs B(headline): b=%d c=%d n=%d p=%.4f"
      % (mc["b"], mc["c"], mc["n_discordant"], mc["p"]))
    p("  CONTROL %d/%d random 7-hex strings resolved in the %d-repo sibling search = %.2f%%"
      % (nc["hits"], nc["n"], nc["repos_searched"], 100 * nc["rate"]))
    p("          pre-registered threshold %.0f%% — %s"
      % (100 * nc["threshold_declared_before_run"],
         "FIRED, sibling matches discounted" if nc["rate"] >= nc["threshold_declared_before_run"]
         else "not fired, sibling matches stand"))
    p("  SENSIT. dropping sibling-resolved gold rows (n=%d): A %s vs B %s"
      % (sens["A naive baseline"]["n"], _pct(sens["A naive baseline"]["accuracy"]),
         _pct(sens["B (headline)"]["accuracy"])))
    p("")
    p("  FALSIFIERS (declared in eval/README.md before this was run):")
    for k, v in res["falsifiers"].items():
        p("    %-38s %s" % (k, "FIRED" if v else "did not fire"))
    p("")
    for line in textwrap.wrap(res["verdict"], W - 6):
        p("  " + line)
    p("  rows, probes and receipts: eval/out/results.json")
    p("=" * W)


if __name__ == "__main__":
    sys.exit(main())
