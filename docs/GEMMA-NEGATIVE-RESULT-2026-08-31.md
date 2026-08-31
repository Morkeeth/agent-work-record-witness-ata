# Gemma as the sovereign explainer: built, measured, NOT enabled

Written 31 Aug. **Read this before claiming Gemma anywhere on the submission.**

## Why we wanted it

The pitch says the probe runs inside the customer's checkout and that "only the verdict
and a session pointer cross the network". That is true of the PROBE and was quietly false
of the EXPLANATION: the Gemini path posts finding text — file paths, commit shas, claim
prose — to a hosted endpoint. Gemma is open-weights, so the same model runs on the
customer's own hardware. `cloud/gemma_explainer.py` takes `GEMMA_BASE_URL`, so pointing it
at a local vLLM or Ollama keeps every byte inside the network, and the receipt reports
`left_the_network` computed from the URL actually called rather than from intent.

That is a real gap in our own claim and this is the right shape of fix.

## What actually happened

`gemma-4-31b-it` and `gemma-4-26b-a4b-it`, via `generativelanguage.googleapis.com`,
measured 2026-08-31. Eight configurations:

| Configuration | Result |
|---|---|
| constraint list, no prefill | restated the constraints as a bulleted plan, one run captioned "Draft 1" / "Draft 2" |
| terse completion framing | same bulleted plan |
| roleplay continuation | same bulleted plan |
| prefilled model turn, t=0.2 | clean on two findings; on ONE finding collapsed to `own own own` with Korean characters |
| prefilled, t=0.7 | collapsed harder, **210 non-latin characters** |
| prefilled, t=0.7, 26b model | `ownces-ownces-ownces` |
| `<note>` delimiters, no prefill | tags nested inside themselves, or returned empty |
| no prefill + last-prose extraction | no prose paragraph present in any of 4 runs |

Six consecutive guarded runs after that: **6 refused, 0 usable.**

## What we shipped anyway, and what we did not claim

**Shipped:** the module, the wiring (`EXPLAINER=gemma`), and a guard that names the defect
rather than passing gibberish into a compliance record. The guard was watched going red on
the real collapse before being trusted:

    repetition loop: 'own' appears 189 times
    210 non-latin characters in an English note
    too short to be an explanation (1 words)

A degenerate explanation is treated exactly as the gate treats an unverifiable claim:
refused, with the reason recorded. `EXPLAINER` defaults to `gemini`, so nothing about the
live demo changed.

**Not claimed:** Gemma is **not** listed as an integrated model on the submission. It is
called, and it is guarded, and it produces nothing usable, so calling it an integration
would be the exact overclaim this product exists to catch. The bonus point is worth 0.2 of
6. It is not worth being the thing a judge greps and finds.

## What would make it work

A self-hosted Gemma behind vLLM with a proper chat template, which is the deployment this
module was written for and the one we could not stand up before the deadline. The API path
is the fallback, and the fallback is what failed. That is a statement about this endpoint,
not about the model.
