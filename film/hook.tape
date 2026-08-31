# 15-second hook for X / phone. 4:5 portrait, big type, REAL commands and REAL exit codes.
# Not a crop of the desktop film: that is FontSize 20 at 1920x1080 and is illegible on a
# phone. This re-runs the same gate at phone size.
# Both halves matter. A checker that only ever says no is not a checker, so the hook shows
# the false claim blocked AND the true one passing.
# Rebuild:  cd ~/CODE/hack-fleet-ata && vhs film/hook.tape

Output demo/hook.mp4
Set Shell zsh
Set FontSize 21
Set Width 1080
Set Height 740
Set Padding 28
Set TypingSpeed 30ms

Hide
Type "setopt interactive_comments; cd ~/CODE/hack-fleet-ata; clear" Enter
Sleep 1s
Show

Type "# An agent says it committed the fix."
Enter
Sleep 900ms

Type "echo 'Committed as deadbee.' | python3 -m gate.outcome_gate; echo exit=$?"
Enter
Sleep 3400ms

Type "# Same gate, a claim that is true."
Enter
Sleep 900ms

Type "echo 'Committed as de20d95.' | python3 -m gate.outcome_gate; echo exit=$?"
Enter
Sleep 3400ms
