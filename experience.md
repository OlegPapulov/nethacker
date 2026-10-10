# Playthrough

Identity: `wiz-hum-cha-mal`

## The games

The wizard farms the first Doom level. It melees the harmless monsters (lichen,
newt, shrieker, grid bug), eats their corpses, and — in the parent — waits for
experience level 12 before it takes the stairs down. Every point of score comes
from a new experience level, so the games that end early are the ones that never
eat, never heal, or fight on the first floor with more monsters than the wizard
can handle. The worst games score 0.018, 0.024, 0.029 and 0.037 — experience
levels 2, 4, 5 and 6 — and they are gone within the first few thousand turns.

## Why the early games stop

The early games stop the way the rules say: food and a weak melee. In the played
games the wizard faints from lack of food while a kobold hits, and misses a
hobbit twice before her thrown dagger cuts him down. The wizard reaches that
monster at melee range, at low experience level, with a quarterstaff and a
handful of hit points.

## What the edit answers

`force bolt` is the ranged attack a wizard has, and this wizard knows it from the
first turn: the cast menu lists it with a zero failure chance next to
`clairvoyance`. The parent only offered the bolt from experience level 10, so
the games above — which die at levels 2, 4, 5 and 6 — never got to use it. The
edit offers the same bolt from the first levels instead, so the wizard can
soften the kobold or the hobbit from two to eight squares away instead of walking
into the dagger. The energy reserve, the known-spell test, the failure test, the
first-Doom-level test and the ranged (2..8, clear line, non-pet, non-weak)
targeting are all unchanged; an adjacent target is still handled by the melee
heuristics.

## What might solve it

See `experiments.md`.
