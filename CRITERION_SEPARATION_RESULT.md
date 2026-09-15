# Criterion-Separation Result

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Question
Can a standard information-gain objective prefer an experiment that is irrelevant to the unresolved decision, while a decision-resolution objective selects a different, cheaper decisive experiment?

## Construction
Current knowledge leaves eight compatible worlds `(y,z1,z2)`, with `y` the unresolved binary decision and `z1,z2` nuisance coordinates.

- Experiment A, cost 1: observes `(z1,z2)` exactly.
- Experiment B, cost 1: observes `y` exactly.

Under a uniform distribution over compatible worlds:

- `IG(A)=2 bits` because A identifies two nuisance bits.
- `IG(B)=1 bit` because B identifies the decision bit.
- A leaves both values of `y` possible after every outcome, so it cannot resolve the decision.
- B resolves `y` after one observation.

Therefore an expected-information-gain selector chooses A, while the cheapest decision resolver chooses B.

## Proposition: objective separation
There exist finite compatible-world sets and equal-cost experiments A and B such that

`IG(A) > IG(B)`

but A has zero ability to resolve the target decision whereas B resolves it completely.

### Proof
Take independent uniform bits `y,z1,z2`. Let A reveal `(z1,z2)` and B reveal `y`. Because the observations are deterministic, mutual information equals observation entropy. Thus `I(W;A)=H(z1,z2)=2` bits and `I(W;B)=H(y)=1` bit. However conditioning on any A outcome leaves `y` uniform on `{0,1}`, whereas conditioning on B fixes `y`. Hence maximizing information about the full world and resolving the target decision are distinct objectives. QED.

## Important novelty boundary
This proposition is mathematically elementary and is NOT, by itself, claimed as a new theorem. Bayesian decision-theoretic experimental design already permits utility functions targeted to downstream decisions, and cost-sensitive active learning is established. The contribution to test is therefore not "information gain can be task-irrelevant" alone.

The stronger candidate contribution is an operational, prior-free/frequentist pipeline in which:

1. finite evidence induces a statistically compatible world set;
2. a decision map partitions those worlds into mutually incompatible decision classes;
3. candidate experiments are evaluated for whether they eliminate cross-decision ambiguity;
4. the least-cost decisive experiment is returned when one exists; and
5. otherwise the system returns a typed impossibility certificate (resolved already, budget obstruction, or continuous zero-margin obstruction).

## Paper-readiness decision
Do NOT write the full paper yet. One final validation layer is needed: run the pipeline over a nontrivial family of generated finite-evidence problems and at least one ML-style case, compare against information gain and a cost-normalized information-gain baseline, and report frequencies/cost ratios plus obstruction rates. If those results are stable and the literature search finds no exact prior-free compatible-world + typed-obstruction formulation, then freeze the method and write the paper.
