# THE AGENT WORK RECORD WITNESS — terminal segment.
# Real commands, real output, real exit codes. Nothing is typed for the camera that
# is not executed. Sleeps are set to the MEASURED length of each narration paragraph
# (demo/.vo-parts) so the verdict is on screen while the voice describes it.
# Rebuild:  cd ~/CODE/hack-fleet-ata && vhs film/terminal.tape

Output demo/seg-terminal.mp4
Set Shell zsh
Set FontSize 20
Set Width 1920
Set Height 1080
Set Padding 30
Set TypingSpeed 28ms

Hide
Type "setopt interactive_comments; cd ~/CODE/hack-fleet-ata; clear" Enter
Sleep 1s
Show

# --- p00 + p01: the problem, over an empty prompt (14.6s of narration)
Sleep 9s
Type "# An agent says it committed. The gate asks the repository." Enter
Sleep 3s

# --- p02 + p03: deadbee, BLOCK on screen (20.4s)
Type "echo 'Committed as deadbee.' | python3 -m gate.outcome_gate" Enter
Sleep 17s
Type 'echo exit-code=$?' Enter
Sleep 4s

# --- p04: the honest report, PASS (7.1s)
Type "clear" Enter
Sleep 1s
Type "echo 'Fixed the auth check. Committed as 7c95a4f. Wrote README.md.' | python3 -m gate.outcome_gate" Enter
Sleep 4s

# --- p05: the claim it refuses to guess at, HOLD (12s)
Type "clear" Enter
Sleep 1s
Type "# And the claim it refuses to guess at." Enter
Sleep 1s
Type "echo 'Committed as 7c95a4f. All 14 tests pass.' | python3 -m gate.outcome_gate" Enter
Sleep 7s

# --- p06: Google Cloud, the deployed service (14s)
Type "clear" Enter
Sleep 1s
Type "gcloud run services describe fleet-wedge --region us-central1 --format='table[box](metadata.name:label=SERVICE, status.url:label=URL, status.latestReadyRevisionName:label=REVISION)'" Enter
Sleep 2s
Type "curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health | python3 -m json.tool | head -14" Enter
Sleep 3s

# --- p07: eligibility CALLS all three (16.7s of narration; the script itself runs ~10s)
Type "clear" Enter
Sleep 1s
Type "python3 contract/eligibility.py 2>&1 | tail -12" Enter
Sleep 18s
