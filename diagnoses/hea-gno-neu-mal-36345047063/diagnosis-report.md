tree:    ./tree
identity: hea-gno-neu-mal

published mean:  0.0995
validation mean: 0.1280

turn-1 deaths: published 0, validation 0

### published (seeds 0-14)
```
 seed status       turns  depth    prog  death
    0 completed    24883      7  0.0745  killed by an owlbear
    1 completed    17860      1  0.0508  killed by a gnome zombie
    2 completed    11815      1  0.0242  died of starvation
    3 completed    13048      1  0.0369  killed by a cave spider
    4 completed    33190      6  0.0745  killed by a Woodland-elf
    5 completed     2388      1  0.0208  killed by a brown mold
    6 completed     5909      1  0.0291  killed by a cave spider
    7 completed    22712     25  0.4664  killed by a raven
    8 completed    21384     19  0.3655  killed by an ogre king
    9 completed     9746      1  0.0369  killed by a wererat
   10 completed    22390      8  0.0696  killed by a Woodland-elf
   11 completed    39844     11  0.1613  killed by a killer bee
   12 completed     4743      1  0.0242  killed by a hobbit
   13 completed    13864      1  0.0369  killed by a little dog
   14 completed     2936      1  0.0208  killed by a hobbit
```

### validation (seeds 1000+)
```
 seed status       turns  depth    prog  death
 1000 completed    29318      1  0.0508  died of starvation
 1001 completed    18184     16  0.3249  killed by a giant mummy
 1002 completed     6952      1  0.0291  killed by a werejackal
 1003 completed    22480      1  0.0291  killed by a brown mold
 1004 completed    24850     12  0.2061  killed by a sergeant
```

VERDICT baseline never dies at turn 1, so a turn-1 mutant is a real regression in the mutation.
