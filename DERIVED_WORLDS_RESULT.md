# Derived-World Cheapest Experiment

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Question

Find the cheapest experiment for which current finite statistical knowledge leaves mutually incompatible possible worlds, without supplying the rival worlds by hand.

## Current knowledge K

Observed 17 successes in 20 Bernoulli trials. Using a 0.01 parameter grid and an exact two-sided binomial compatibility test at alpha=0.05, the compatible worlds are theta = 0.63,...,0.95.

For a decision threshold theta=0.80, K therefore leaves both decision classes possible:

- unreliable world class: theta < 0.80
- reliable world class: theta >= 0.80

Thus K itself induces mutually incompatible worlds.

## Cheapest existence-witness experiment

To answer the existential question at minimum cost, select the most separated compatible worlds across the decision boundary: theta=0.63 and theta=0.95. These are not hand-specified rivals; they are endpoints derived from K.

For m additional iid Bernoulli observations, define successful discrimination as total-variation distance TV(Bin(m,0.63), Bin(m,0.95)) >= 0.80.

Exact enumeration gives:

- m=7: TV = 0.754294 < 0.80
- m=8: TV = 0.801346 >= 0.80

Therefore, among this candidate experiment family,

**m* = 8 additional observations**

is the cheapest experiment that strongly separates at least one pair of decision-incompatible worlds left possible by K.

## Important distinction

This is an existence witness, not a robust resolution guarantee. If the goal is to distinguish the hardest worlds straddling the 0.80 decision boundary (0.79 versus 0.80 on this grid), the required cost is 10,705 observations for the same TV threshold. Hence existential ambiguity exposure and guaranteed decision resolution are radically different optimization problems.

## New gap exposed by the experiment

The same knowledge state K has two different experiment costs:

1. **Contradiction exposure cost:** cheapest experiment separating some incompatible worlds: 8.
2. **Boundary resolution cost:** experiment separating the hardest decision-incompatible worlds: 10,705.

The ratio is 10,705 / 8 = 1,338.125.

This demonstrates a large distinction between proving that current knowledge is underdetermined and resolving that underdetermination robustly. Whether this distinction yields a novel general theory must be checked against active testing, optimal experimental design, robust hypothesis testing, and version-space/query complexity literature before making a novelty claim.
