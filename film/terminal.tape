# THE AGENT WORK RECORD WITNESS — terminal segment.
# Real commands, real output, real exit codes. Nothing is typed for the camera that
# is not executed. Rebuild with:  cd ~/CODE/hack-fleet-ata && vhs film/terminal.tape

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

Sleep 2s
Type "# An agent says it committed. The gate asks the repository." Enter
Sleep 2s
Type "echo 'Committed as deadbee.' | python3 -m gate.outcome_gate" Enter
Sleep 6s
Type 'echo exit-code=$?' Enter
Sleep 4s

Type "clear" Enter
Sleep 1s
Type "# A check that only ever says no is not a check. An honest report:" Enter
Sleep 2s
Type "echo 'Fixed the auth check. Committed as 7c95a4f. Wrote README.md.' | python3 -m gate.outcome_gate" Enter
Sleep 7s

Type "clear" Enter
Sleep 1s
Type "# And the claim it refuses to guess at." Enter
Sleep 2s
Type "echo 'Committed as 7c95a4f. All 14 tests pass.' | python3 -m gate.outcome_gate" Enter
Sleep 8s

Type "clear" Enter
Sleep 1s
Type "# The backend is on Google Cloud. Not a diagram — the deployed service." Enter
Sleep 2s
Type "gcloud run services describe fleet-wedge --region us-central1 --format='table[box](metadata.name:label=SERVICE, status.url:label=URL, status.latestReadyRevisionName:label=REVISION)'" Enter
Sleep 8s
Type "curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health | python3 -m json.tool | head -14" Enter
Sleep 8s
