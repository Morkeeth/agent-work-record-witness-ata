# Gemma: it was the transport, not the model

Written 31 Aug. The first version of this file said Gemma could not do the job. That was
wrong, and the way it was wrong is the point.

## The claim I nearly shipped

Eight configurations against `generativelanguage.googleapis.com`, two Gemma models, every
one unusable:

| Configuration | Result |
|---|---|
| constraint list, no prefill | restated the constraints as a bulleted plan, one captioned "Draft 1" / "Draft 2" |
| terse completion framing | same bulleted plan |
| roleplay continuation | same bulleted plan |
| prefilled model turn, t=0.2 | clean on two findings; on ONE finding collapsed to `own own own`, with Korean characters |
| prefilled, t=0.7 | collapsed harder, **210 non-latin characters** |
| prefilled, t=0.7, 26b model | `ownces-ownces-ownces` |
| `<note>` delimiters | tags nested inside themselves, or empty |
| no prefill + prose extraction | no prose paragraph in any of 4 runs |

Six guarded runs after that: **6 refused, 0 usable.** The conclusion written at that point
was "this model is not reliable enough for a compliance record". It named the wrong object.

## The control that overturned it

Same module. Same model. Same prompt. One thing changed: an OpenAI-compatible
`/chat/completions` transport, which carries a real `system` role and a real chat template.

    openai transport (OpenRouter)   6 runs   6 USABLE   0.55s to 1.31s
    google transport (generateContent, control, same code)   3 runs   3 REFUSED
        repetition loop: '*' appears 13 times

**It was never the model. It was the chat template.** `generateContent` has no system role,
so the instruction goes into the user turn and Gemma answers the instruction instead of the
question. Prefilling a `model` turn to force the shape is what triggered the degenerate
decoding, which is where the Korean characters came from.

That is this repository's own thesis landing on its own author for the second time in one
week: a measurement that was correct about the wrong object. The eight rows above are kept
rather than deleted, because the wrong conclusion is the useful half.

## What ships

`cloud/gemma_explainer.py`, two transports, `openai` by default.

- **Self-hosting is the same code path.** vLLM, Ollama and LM Studio all speak
  `/chat/completions`. Set `GEMMA_BASE_URL=http://localhost:11434/v1` and no claim text
  leaves the network. That closes a real hole in our own pitch: we say only the verdict
  crosses the network, and the Gemini explainer posts finding text to a hosted endpoint.
- **The receipt reports `left_the_network` from the URL actually called**, never from
  configuration intent. On a hosted endpoint that boolean is `true` and it says so.
- **The guard stays.** It caught the real failure, it was watched going red before it was
  trusted green, and it is the reason the wrong conclusion was visible rather than silent.

Probes decide. Gemma explains. It never overturns a verdict.
