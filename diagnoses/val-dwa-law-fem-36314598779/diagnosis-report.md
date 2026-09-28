tree:    ./tree
identity: val-dwa-law-fem

published mean:  0.1122
validation mean: 0.1088

turn-1 deaths: published 0, validation 0

### published (seeds 0-14)
```
 seed status       turns  depth    prog  death
    0 completed    39767      4   0.117  -
    1 completed    35249      4   0.117  killed by a watch captain
    2 completed    16295      1  0.0508  -
    3 completed    17593      1  0.0508  died of starvation
    4 completed    33478     11  0.1613  -
    5 completed    28998      5   0.117  petrified by touching a cockatrice corpse bare-handed
    6 completed    20978      1  0.0508  killed by a hill orc
    7 completed    35134      9  0.1791  poisoned by a rotted garter snake corpse
    8 completed     9079      1  0.0291  killed by a sewer rat
    9 completed    15572      1  0.0369  killed by a wererat
   10 completed    53644      7  0.2548  killed by a death ray
   11 completed     8419      1  0.0291  killed by a garter snake
   12 completed    28923      3   0.117  killed by an orc zombie
   13 completed    27487      5   0.117  killed by a tengu
   14 completed    40533     11  0.2548  -
```

### validation (seeds 1000+)
```
 seed status       turns  depth    prog  death
 1000 completed    12479      1  0.0369  killed by a fox
 1001 completed    28809      6  0.1791  -
 1002 completed    25241      2  0.0745  killed by a giant rat
 1003 completed    30176      3  0.0745  killed by a rabid rat
 1004 completed    35119      8  0.1791  -
```

VERDICT baseline never dies at turn 1, so a turn-1 mutant is a real regression in the mutation.
