# Paper Gate

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Current research question

Given finite evidence K, construct a statistically valid compatible set C_alpha(K). If C_alpha(K) contains worlds inducing mutually incompatible target decisions, choose the minimum-cost admissible experiment that resolves the target disagreement; otherwise return a typed obstruction/abstention certificate.

## Important novelty boundary

Do **not** claim novelty for any component in isolation:

- confidence sets from finite evidence;
- adaptive/sequential experimental design;
- active/composite hypothesis testing;
- information gain or cost-sensitive acquisition;
- version spaces / disagreement;
- Decision Region Determination (DRD) or Equivalence Class Determination (ECD);
- the fact that arbitrarily close alternatives require unbounded uniform fixed-sample resolution.

The paper must instead test the value of the *composition*: statistically valid evidence-induced admissible sets feeding a target-aware minimum-cost planner, with explicit abstention/obstruction when the evidence does not support finite resolution.

## Final validation matrix

1. **Coverage:** repeated simulation verifies the advertised coverage of C_alpha(K).
2. **Decision validity:** output a decision only if all remaining admissible worlds induce that decision.
3. **Cost:** use heterogeneous experiment costs and report total acquisition cost.
4. **Strong baseline:** compare against a target-aware DRD/ECD-style planner as well as generic information gain.
5. **Noise:** include noisy experiment outcomes; report decision error, abstention and cost.
6. **Obstruction:** validate budget obstruction and zero-margin/continuous obstruction cases.
7. **Real ML:** one classifier deployment-threshold task with realistic test/subgroup acquisition choices.
8. **Reproducibility:** fixed seeds, tables, raw CSV/JSON results, one-command reproduction, CI.

## Stop rule

Start manuscript drafting immediately when all eight items above have reproducible outputs and the target-aware baseline does not subsume the proposed method.

If the target-aware baseline matches the method exactly after the same statistically valid world construction, do not claim a new planning algorithm. Reframe the contribution as a statistically valid interface/protocol between uncertainty-set construction and decision-oriented experiment planning, or stop if even that interface is already established.

## Paper claim to test, not yet claim as fact

> Finite evidence can be converted into a statistically valid set of admissible worlds; when those worlds disagree on a downstream decision, experiment acquisition should target the disagreement at minimum cost, while returning an explicit obstruction when no admissible finite-cost experiment can provide the requested resolution.
