# ATA — film in 10 minutes, then submit. Everything is live and ready.
# Line: "Run your agents. Check the math." · ≤4:00 unedited · say the full product name twice.
# Live: https://fleet-wedge-33kamss2jq-uc.a.run.app  (deployed + verified 2026-08-30)

## Before you hit record (2 min)
- Open the flipbook `demo/flipbook.html` once to see the flow; play `demo/voiceover.mp3` as your pace.
- Open two browser tabs: (A) /hold/?record=H-a6151a95ac  (B) a terminal for the curls.
- Cold-start: hit /health once first so the container is warm before you record.

## Teleprompter — click + say (each row ≈ the VO beat)
| t | CLICK / SHOW | SAY (from the voiceover) |
|---|--------------|--------------------------|
| 0:00 | Title card / flipbook frame 0 | "Run your agents. Check the math." |
| 0:10 | A vendor dashboard (or the flipbook problem frame) | "Companies see seats and tokens. Not whether the work the agents said they did, they did." |
| 0:30 | Tab A — the held record open, resolving to its session | "This is the Agent Work Record Witness. It starts at month four. A held claim resolves to the session that produced it." |
| 1:10 | Scroll the record: PASS/BLOCK/UNVERIFIABLE/HOLD | "The gate reads the object, never the report. Did that commit land. Does that file exist." |
| 1:35 | The real PR row (H-a6151a95ac), verify-claims red | "A false-done PR. verify-claims goes red, it's blocked, a row opens. The one true claim still passes; the false ones are held." |
| 2:15 | Break-glass reason + Export JSON | "Every hold opens with a reason, and the reason is recorded. The whole record exports as JSON your CI fills itself." |
| 2:40 | Tab B — curl /health ; curl /audit | "Live on Cloud Run. Eligibility three of three with creds, one of three cold. Gemini three-five via the ADK explains a verdict; it never overrules it." |
| 3:05 | /audit agent_run invoked:true | "One real agent PR went through. It failed on purpose — record H, a six one five one. Nothing has cleared. The product working, not breaking." |
| 3:30 | Install snippet + the line | "Install is a policy URL and one GitHub action. The Agent Work Record Witness. Run your agents. Check the math." |

Do NOT show: the Seed button · /healthz · the words "required check" · the names Witness/Claims Inbox/hack-fleet-ata · the CLI as the product.

## Upload the video FIRST (their processing lag is the real risk)
- Export ≤4:00, unedited. Upload to YouTube/Vimeo now. Set PUBLIC. Check in an incognito window.

## Devpost submit checklist (paste from SUBMISSION-PACK.md)
1. Project name + Tagline (§1) · Track: Fortified Enterprise Fleet
2. Video URL (public, incognito-checked)
3. Hosted URL: https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
4. Repo URL — if private, confirm shared with testing@devpost.com AND cloudhackathons@google.com
5. What it does / How we built it (§1) · Built with (§6, incl. secret-manager, vertex-ai, google-adk)
6. Testing instructions: paste SUBMISSION-PACK.md §5 (the no-login eval path)
7. Architecture image: docs/architecture.png
8. Select category, add teammates (confirm they accepted), then SUBMIT.
9. After deadline: do not touch the repo/video until winners announced.
