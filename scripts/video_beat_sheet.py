#!/usr/bin/env python3
"""Video / judge beat sheet — GCP-visible one-take path.

Oscar owns the recording. This file is the checklist so the take cannot miss a
mandatory beat (Devpost: backend proof on Google Cloud in the video).
"""

BEATS = [
    ("0:00–0:20", "Problem", "GEAP governs agents; nothing governs prompts. Companies see seats, not practice."),
    ("0:20–0:50", "Eligibility", "Terminal: python3 contract/eligibility.py → 3 OF 3 MET (Gemini · ADK · Firestore)."),
    ("0:50–1:20", "Cloud Run", "Browser: open Cloud Run service fleet-wedge · URL *.run.app · curl /health JSON."),
    ("1:20–2:10", "M3 delta", "POST /prove or fleet_cli.py prove · surface shows A=0 corrective vs B=2 · VERIFIED-BY-REPO."),
    ("2:10–2:40", "Literal", "Show skill file text = winner opener (no LLM rewrite). org_claim UNMEASURED_FOR_ORG_CLAIM on field of 2."),
    ("2:40–3:20", "Architecture", "docs/ARCHITECTURE.md mermaid · ADK supervisor · Firestore log · Cloud Run."),
    ("3:20–3:50", "Honest limit", "Population lift = day-two customer corpus; C1 red → no 8/8 seal."),
    ("3:50–4:00", "Close", "Repo + spin-up in README."),
]

SMOKE = """
export PATH="$HOME/google-cloud-sdk/bin:$PATH"
URL=$(cat .cloud_run_url)
curl -s "$URL/health"
curl -s -X POST "$URL/prove" -H 'Content-Type: application/json' -d '{}'
open "surface/org-lift-live.html?api=$URL"
"""

if __name__ == "__main__":
    for t, name, body in BEATS:
        print(f"{t}  [{name}]  {body}")
    print("\n# smoke\n" + SMOKE)
