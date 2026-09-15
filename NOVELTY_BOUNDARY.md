# Novelty Boundary and Paper Gate

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
Licensed under the Apache License, Version 2.0.

## Result of targeted prior-art attack

The broad problem of selecting low-cost experiments to determine a target decision is already established. In particular, Decision Region Determination (DRD) seeks a minimum-cost policy whose resulting version space lies inside a decision region; Equivalence Class Determination is a special case. Bayesian decision-theoretic experimental design can also optimize experiment-specific downstream utility rather than generic information gain. Cost-aware active learning and recent obstruction-aware exact finite identification are additional close neighbors.

Therefore the project MUST NOT claim novelty for any of the following alone:

1. choosing a cheaper decision-relevant experiment instead of a higher-information experiment;
2. maintaining a version space / compatible hypothesis set;
3. minimum-cost decision-region identification;
4. returning an over-budget or indistinguishable pair for a supplied finite world set;
5. the fact that arbitrarily close Bernoulli parameters require unbounded samples for uniform fixed-confidence separation.

## Remaining candidate contribution

The defensible candidate contribution is an evidence-first statistical admission layer:

K -> statistically induced compatible set C_alpha(K) -> target-disagreement test -> cheapest admissible experiment or typed statistical obstruction.

The important distinction is that the admissible world set is generated from finite-sample statistical compatibility with observed data, rather than supplied as a finite hypothesis/version space. This layer can be placed before an existing DRD/ECD/decision-theoretic planner.

## Formal paper gate

Do not begin the manuscript until the repository demonstrates all of the following:

- finite-sample coverage/compatibility is controlled at the advertised alpha level;
- the selector is compared with a DRD/ECD-style target-aware baseline, not only information gain;
- a benchmark includes noisy observations, unequal experiment costs, and multiple candidate experiments;
- obstruction certificates are empirically checked (no false finite-resolution claim under the stated assumptions);
- at least one real ML deployment-threshold example is reproduced end-to-end;
- claims are framed as an evidence-to-planning interface unless a stronger separation theorem from DRD/ECD is proved.

## Current manuscript status

Theory prototype: complete enough for validation.
Novelty: narrowed, not yet established as a new planning problem.
Paper: NOT YET. Run the final benchmark against target-aware baselines first.
