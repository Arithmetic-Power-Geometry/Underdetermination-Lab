# Final Validation Results

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Reproducibility snapshot

This file freezes results actually executed by GitHub Actions on commit `76a9da42f7f0d3ffb7c0db4f02d10d5265ac6ec1`, workflow run `34964785661`. The complete job concluded successfully. Numerical values below are copied from that executed run, not inferred from unexecuted scripts.

## 1. Software gate

`python -m pytest -q`: **13 passed**.

## 2. Continuous statistical-admission coverage gate

The compatible set is obtained by inversion of the exact two-sided binomial test using probability ordering. Coverage was evaluated directly at 999 continuous Bernoulli parameter values `p=0.001,...,0.999`; it was not evaluated by asking whether the truth belongs to the repository's 0.01 planning grid.

Nominal coverage: `0.950`.

| n | minimum coverage | p at minimum | coverage at p=0.799 | coverage at p=0.801 |
|---:|---:|---:|---:|---:|
| 10 | 0.950030201 | 0.150 | 0.966541349 | 0.967862573 |
| 20 | 0.950141303 | 0.896 | 0.955717625 | 0.956914044 |
| 50 | 0.950095252 | 0.201 | 0.950095252 | 0.951236567 |
| 100 | 0.950075652 | 0.214 | 0.954715417 | 0.954453082 |
| 200 | 0.950009652 | 0.175 | 0.957837144 | 0.958905643 |

Global minimum observed coverage: **0.950009652** at `p=0.175`, `n=200`.

Result: **COVERAGE_GATE = PASS**.

Important scope: this is a dense deterministic continuous-parameter scan for the tested sample sizes, not an analytic proof over every real p and every n.

## 3. Evidence-induced incompatible worlds

Observed knowledge: `K = 17/20` successes. At `alpha=0.05`, the 0.01 planning grid admits 33 worlds from `theta=0.63` through `theta=0.95`. The deployment threshold `d=0.80` therefore remains underdetermined.

The closest grid pair with opposite decisions is `0.79` versus `0.80`.

For the existential contradiction-exposure objective, the derived compatible endpoints are `0.63` versus `0.95`. The cheapest additional Bernoulli experiment reaching total variation at least `0.80` uses **8 observations**, with `TV=0.801346` and cost `8` at unit observation cost.

These are different objectives and must not be conflated.

## 4. Robust planning / obstruction gate

For the 33 admissible grid worlds and threshold `0.80`:

- strict requested cross-decision separation: **OBSTRUCTION**;
- weak target: `high_fidelity_panel`, cost **8**, worst cross-decision TV `0.010000`;
- declared margin `0.10`: `standard_panel`, cost **3**, worst cross-decision TV `0.150000`;
- budget `2`: **OBSTRUCTION**.

In the continuous zero-margin setting, uniform finite fixed-size resolution remains obstructed because compatible worlds can approach the decision boundary arbitrarily closely.

## 5. Target-aware adversarial comparison

Executed adversarial benchmark:

- robust minimum-worst-pair criterion selected `robust_decision_test`, cost **3**, worst cross-decision TV **0.600000**;
- the implemented ECD-style average edge-separation-per-cost surrogate selected `average_good_but_boundary_weak`, cost **1**, score **0.1175**.

This demonstrates a separation between the two implemented one-step objectives on the constructed instance. It does **not** establish superiority over full sequential DRD/ECD/EC2 algorithms and must not be described that way.

## 6. ML deployment-threshold case

Deployment rule: all subgroup accuracies must be at least `0.80`.

| subgroup | evidence | grid-compatible set | state | label unit cost |
|---|---:|---:|---|---:|
| common | 94/100 | 0.88--0.97 | PASS | 1.0 |
| moderate | 45/50 | 0.79--0.95 | UNRESOLVED | 2.5 |
| rare | 17/20 | 0.63--0.95 | UNRESOLVED | 8.0 |

Thus current evidence leaves mutually incompatible global deployment worlds.

For the hardest finite-grid pair `0.79` versus `0.80`, the executed calculation requires 10,705 additional labels to reach TV 0.80. This corresponds to:

- moderate subgroup: `10,705 x 2.5 = 26,762.50`;
- rare subgroup: `10,705 x 8.0 = 85,640.00`.

The moderate subgroup is therefore the **cheapest next finite-grid boundary experiment among these two subgroup experiments**.

### Critical semantic limitation

It must **not** be called a globally certifying single experiment under the conjunction deployment rule. Both moderate and rare groups are unresolved. If the moderate experiment returns evidence sufficient for PASS, the rare group can still leave the global DEPLOY decision unresolved. A FAIL in any subgroup can terminate with DO-NOT-DEPLOY, whereas a PASS may require continued testing of the remaining unresolved groups. A sequential global policy is therefore required for a genuine minimum-cost global certification claim.

## 7. Paper gate

| gate | status | reason |
|---|---|---|
| Unit/reproducibility tests | PASS | 13/13 tests passed in CI |
| Coverage-controlled statistical admission | PASS for tested n,p grid | minimum scanned coverage 0.950009652 |
| Evidence-induced target disagreement | PASS | compatible worlds cross 0.80 |
| Cost-aware experiment selection | PASS at one-step prototype level | finite costs and obstruction returned |
| Noise / stochastic observations | PASS at prototype level | Bernoulli/binomial stochastic laws used |
| Explicit obstruction semantics | PASS | strict and budget obstruction cases executed |
| Target-aware comparison | PARTIAL | adversarial ECD-style surrogate executed; not full DRD/ECD/EC2 |
| ML deployment case | PARTIAL | end-to-end evidence induction works, but global conjunction requires sequential policy |
| Large-scale benchmark | NOT YET FROZEN | existing script has not been accepted as final benchmark |
| Final novelty claim | HOLD | nearby DRD/ECD, decision-focused design and obstruction-aware identification require conservative framing |

## Decision

**HOLD THE FINAL MANUSCRIPT CLAIM; CONTINUE THE VALIDATION, NOT THE CONCEPT GENERATION.**

The evidence-to-planning pipeline is now reproducible and statistically much stronger, but two issues should be closed before calling the manuscript submission-ready:

1. implement an exact small-state sequential global deployment planner for conjunction decisions, so the ML example optimizes a true global target rather than a single unresolved subgroup; and
2. compare that planner against an exact finite target-aware dynamic-programming baseline on matched small benchmarks. If the planning layer is subsumed, frame the contribution as the coverage-controlled statistical evidence-to-planning interface plus obstruction semantics, not as a new planning algorithm.

No new broad theory should be introduced before these two gates are resolved.
