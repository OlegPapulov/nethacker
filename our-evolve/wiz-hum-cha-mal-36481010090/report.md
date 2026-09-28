### our loop — wiz-hum-cha-mal — opencode2/opencode/big-pickle

#### log
```
=== wiz-hum-cha-mal · our loop · 1 iteration(s) ===
seed: seed-bot
arena · running 15 episode(s)…
arena · episode 1/15 (wiz-hum-cha-mal): progress=0.037 completed turns=13697 depth=1
arena · episode 2/15 (wiz-hum-cha-mal): progress=0.037 completed turns=17693 depth=1
arena · episode 3/15 (wiz-hum-cha-mal): progress=0.075 completed turns=20700 depth=5
arena · episode 4/15 (wiz-hum-cha-mal): progress=0.021 completed turns=3052 depth=1
arena · episode 5/15 (wiz-hum-cha-mal): progress=0.179 completed turns=32346 depth=7
arena · episode 6/15 (wiz-hum-cha-mal): progress=0.051 completed turns=14486 depth=1
arena · episode 7/15 (wiz-hum-cha-mal): progress=0.037 completed turns=11919 depth=1
arena · episode 8/15 (wiz-hum-cha-mal): progress=0.075 completed turns=23971 depth=2
arena · episode 9/15 (wiz-hum-cha-mal): progress=0.075 completed turns=23604 depth=5
arena · episode 10/15 (wiz-hum-cha-mal): progress=0.075 completed turns=24295 depth=4
arena · episode 11/15 (wiz-hum-cha-mal): progress=0.024 completed turns=4014 depth=1
arena · episode 12/15 (wiz-hum-cha-mal): progress=0.117 completed turns=27094 depth=5
arena · episode 13/15 (wiz-hum-cha-mal): progress=0.037 completed turns=12509 depth=1
arena · episode 14/15 (wiz-hum-cha-mal): progress=0.024 completed turns=5206 depth=1
arena · episode 15/15 (wiz-hum-cha-mal): progress=0.075 completed turns=22485 depth=1
seed baseline: 0.0624 over 15 seeds

--- iteration 1 ---
brief: 3626 chars -> runs/brief-1.md
Traceback (most recent call last):
  File "/home/runner/work/nethacker/nethacker/evolve.py", line 313, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/runner/work/nethacker/nethacker/evolve.py", line 229, in main
    hypothesis = run_operator(worktree, brief_text, args)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/nethacker/nethacker/evolve.py", line 277, in run_operator
    result = operator.run(worktree, brief_text)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/nethackers/harness/container_operator.py", line 438, in run
    return run_operator(
           ^^^^^^^^^^^^^
  File "/home/runner/.local/lib/python3.12/site-packages/nethackers/harness/operator.py", line 169, in run_operator
    raise OperatorRefused(message) if refused else RuntimeError(message)
RuntimeError: opencode2 operator exited with status 125: Run 'docker run --help' for more information
```
