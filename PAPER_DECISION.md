# Paper Decision and Claim Boundary

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Decision

**START WRITING THE PAPER NOW.**

The exact target-aware dynamic-programming comparison has been executed in GitHub Actions and passed. On the matched finite deterministic conjunction benchmark, the evidence-first sequential planner and the exact target-aware DP produce the same optimum:

- worst-case cost: `112402.5`;
- first experiment: `moderate`;
- exact comparison: `MATCH=YES`.

Therefore the manuscript must **not claim novelty for the finite planning algorithm**. Once a finite world table, target map, experiment observations, and costs are supplied, the planning layer is subsumed on this benchmark by an established DRD/ECD-style exact target-identification formulation.

## Surviving paper question

Given finite noisy evidence `K`, can we construct a statistically valid admissible-world set `C_alpha(K)`, determine whether those admissible worlds imply incompatible downstream decisions, and expose the result to a cost-aware target-identification layer while returning an explicit statistical obstruction when the requested resolution is impossible under the experiment family, margin, or budget?

The paper studies the interface

`finite noisy evidence -> coverage-controlled admissible worlds -> downstream decision partition -> target-aware planning -> statistical obstruction/abstention`.

## Claim we may make

We present and validate an **evidence-first statistical admission interface for experimental decision resolution**. Finite noisy observations are converted into an admissible-world set with controlled finite-sample coverage semantics. The downstream target is evaluated over that set. If all admissible worlds agree, no further experiment is required. If they disagree, the set is passed to a cost-aware target-identification planner. If the requested separation cannot be achieved under the available experiments, margin, or budget, the procedure returns an explicit obstruction rather than an unsupported decision.

## Claims we must not make

Do not claim as new:

- optimal experimental design;
- cheapest informative experiment selection;
- active learning or disagreement sampling;
- version spaces or confidence sets;
- DRD/ECD/EC2-style target identification;
- cost-sensitive acquisition;
- task-aware or decision-focused experiment design;
- exact binomial confidence/test inversion;
- the fact that zero-margin threshold resolution can require unbounded samples;
- the finite dynamic-programming planner;
- subgroup deployment thresholds;
- obstruction over a user-supplied finite deterministic world table.

## Executed evidence supporting the paper

### Statistical admission

For exact two-sided binomial-test inversion at nominal coverage `0.95`, the deterministic scan over `p=0.001,...,0.999` and `n in {10,20,50,100,200}` achieved minimum observed coverage `0.950009652` at `p=0.175`, `n=200`. The coverage gate passed.

### Evidence-induced disagreement

For `K=17/20`, `alpha=0.05`, the 0.01 planning grid admits 33 worlds from `0.63` through `0.95`, crossing the downstream threshold `0.80`.

### Different resolution notions

The cheapest existential contradiction-exposure witness `0.63` versus `0.95` reaches TV `0.80` with 8 additional Bernoulli observations. The hardest finite-grid boundary pair `0.79` versus `0.80` requires 10,705 observations at the same TV threshold. In the continuous zero-margin setting, uniform fixed-size resolution remains obstructed.

### Cost-aware / obstruction behavior

The executed one-step planner returns an obstruction for a strict cross-decision requirement, chooses a high-fidelity panel at cost 8 for a weak requirement, chooses a standard panel at cost 3 under a declared margin of 0.10, and returns a budget obstruction under budget 2.

### ML deployment example

With a deployment rule requiring every subgroup accuracy to be at least 0.80:

- common: `94/100`, admissible grid `0.88--0.97`, PASS;
- moderate: `45/50`, `0.79--0.95`, UNRESOLVED;
- rare: `17/20`, `0.63--0.95`, UNRESOLVED.

The finite-grid boundary certification costs are `26762.5` for moderate and `85640.0` for rare. Correct global conjunction semantics give a minimax worst-case cost `112402.5`, testing moderate first and rare second if needed.

### Exact target-aware baseline

The matched exact finite target-aware DP returns exactly the same `112402.5` worst-case cost and `moderate` first experiment. This negative novelty result is important: it establishes that the paper should treat target-aware planning as an existing downstream component, not the claimed methodological novelty.

## Manuscript structure

1. Introduction: finite evidence often leaves multiple statistically admissible worlds that imply different downstream decisions.
2. Related work: confidence/test inversion; OED/BOED; active learning; DRD/ECD; decision-focused sequential design; robust/ambiguity-set design; obstruction-aware finite identification.
3. Problem formulation: evidence `K`, admissible set `C_alpha(K)`, target map `d`, experiment family, cost, separation requirement, obstruction types.
4. Statistical admission layer and coverage semantics.
5. Interface to target-aware planning; explicitly position the planner as interchangeable/existing.
6. Continuous decision-boundary obstruction and positive-margin finite resolvability.
7. Controlled experiments: derived worlds, contradiction exposure versus boundary resolution, noise/cost/margin/budget.
8. Exact DP comparison: show planning-layer subsumption rather than hiding it.
9. ML deployment-threshold case with corrected conjunction semantics.
10. Limitations and claim boundary.
11. Conclusion.

## Remaining work while writing

The manuscript can now be drafted. In parallel with drafting, perform only strengthening work that does not change the core claim: freeze the exact DP run in the final results file, correct the legacy phrase `CHEAPEST FINITE-GRID CERTIFYING EXPERIMENT` in `ml_deployment_case.py` to `CHEAPEST NEXT FINITE-GRID SUBGROUP-RESOLUTION EXPERIMENT`, remove the Python escape-sequence warning, replace the abbreviated Apache license with the canonical Apache-2.0 text, and run a final targeted literature search before submission.

These are submission-hardening tasks, not reasons to postpone manuscript drafting.
