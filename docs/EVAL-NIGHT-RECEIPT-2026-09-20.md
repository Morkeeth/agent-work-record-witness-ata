# Eval night receipt · 2026-09-20

Re-ran the committed eval. Numbers below come from this process, not from an older README table.

```bash
python3 eval/run_eval.py
```

| Arm | Accuracy (Wilson 95%) | False accusations | Notes |
|-----|----------------------:|------------------:|-------|
| NULL always-silent | 27/40 **67.5%** [52.0, 79.9] | 0/40 | beats both arms on accuracy |
| A naive baseline | 9/40 **22.5%** [12.3, 37.5] | 18/40 45.0% | two-hour competent alternative |
| B (headline) | 18/40 **45.0%** [30.7, 60.2] | 2/40 5.0% | our gate |
| B0 defaults | 10/40 25.0% | 17/40 | ablation |
| B + scope | 27/40 67.5% | 0/40 | ties NULL; disclosed, not swapped in |

Paired McNemar A vs B: b=0 c=9 n=9 **p=0.0039**. Falsifiers 1–4 did not fire.

**Finding that could embarrass us (kept):** the always-silent null beats our headline arm
on the pre-registered accuracy metric. Separation is adjudication (12/13 vs 7/13) and false
accusations (5.0% vs 45.0%), not accuracy. Full transcript: `/tmp/eval-run.out` on the
runner; durable copy is `eval/out/results.json` rewritten by this run.
