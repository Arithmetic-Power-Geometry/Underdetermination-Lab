# Target-Aware ECD/DRD Comparison

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Apache-2.0

## Why this comparison is mandatory

Information gain is not a sufficient baseline. Equivalence Class Determination
(ECD) and Decision Region Determination (DRD) already formalize target-aware,
cost-sensitive experiment selection over supplied hypothesis/version spaces.
The repository therefore includes a target-aware ECD-style comparator that
places edges only between admissible worlds implying different decisions.

## Compared objectives

For admissible worlds C and decision map d, the robust one-step rule selects the
least-cost experiment e satisfying

    min_{a,b in C: d(a) != d(b)} TV(P_e^a, P_e^b) >= tau.

The ECD-style comparator scores an experiment by cost-normalized weighted
cross-decision edge separation:

    score(e) = [sum_{d(a)!=d(b)} w(a)w(b) TV(P_e^a,P_e^b)] / c(e).

These are deliberately different objectives: worst-conflict resolution versus
average weighted edge cutting.

## Adversarial construction

`experiments/ecd_adversarial_comparison.py` gives both selectors the same four
worlds, target partition, costs and noisy experiment laws.

- Experiment A is inexpensive and separates most cross-target pairs strongly,
  but leaves the near-boundary conflicting pair weakly separated.
- Experiment B is more expensive but separates every cross-target pair by at
  least the required threshold.

The robust rule therefore chooses B at the declared resolution threshold,
whereas the cost-normalized ECD-style score can choose A.

## Interpretation

This establishes an objective-level separation in the controlled construction.
It does **not** establish novelty by itself. ECD, DRD, EC2/ECED and related
Bayesian active-learning methods are substantial prior art. A publication claim
must not say that target-aware or cost-aware experimental design is new.

The remaining candidate contribution is the integrated requirement:

    finite statistical evidence
      -> statistically admissible worlds
      -> target disagreement
      -> minimum-cost robust resolution
      -> explicit obstruction/abstention when uniform resolution is impossible.

The important distinction to test empirically is whether a planner optimized
for average/probability-weighted target discrimination can spend less now but
fail the repository's *uniform admissible-world resolution certificate*, while
the robust planner either purchases the least-cost certifying experiment or
refuses to certify.

## Paper gate

Do not write the full paper from this construction alone.

One substantive validation remains: a real ML deployment-threshold case with
finite validation counts, subgroup/test-set acquisition costs, statistically
constructed admissible worlds, and the same target-aware comparison. If that
case works and the final literature audit finds no exact prior formulation of
the full evidence-to-certificate pipeline, freeze the theory and write.
