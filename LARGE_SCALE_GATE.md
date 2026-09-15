# Large-Scale Paper Gate

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Apache-2.0

## Why this stage exists

The project is no longer allowed to gain novelty merely by adding terminology.
The next question is empirical and falsifiable: does the complete chain behave
correctly over many finite-evidence states?

\[
K \to C_\alpha(K) \to \text{target disagreement}
\to \text{cheapest candidate resolver or obstruction}.
\]

`experiments/large_scale_paper_gate.py` creates a fixed-seed benchmark over:

- 11 true Bernoulli worlds around and away from the deployment boundary 0.80;
- initial sample sizes 20, 50, and 100;
- 2,000 replicates per condition (66,000 attempted evidence states);
- eight heterogeneous candidate experiments per replicate;
- unequal costs and noisy measurement channels;
- a target-blind information-gain-per-cost comparator.

The raw output is written to `results/large_scale_paper_gate.csv` when executed.

## What this benchmark can establish

It can test whether:

1. the evidence-induced compatible set has the intended empirical coverage;
2. the method avoids decisions while compatible worlds imply opposite actions;
3. resolved decisions have a low error rate;
4. the experiment planner returns a minimum-cost candidate only when its
   declared separation condition is satisfied;
5. otherwise it returns an obstruction;
6. target-blind information gain can spend resources on world distinctions that
   do not settle the deployment target.

## What this benchmark cannot establish

It does **not** establish superiority to DRD/ECD, goal-oriented Bayesian
experimental design, or other target-aware sequential design methods. A
comparison against a genuinely target-aware planner remains mandatory.

It also does not make the classical ingredients (confidence sets, total
variation, decision regions, experiment costs) novel.

## Paper stopping rule

Do not add a new theoretical object after this benchmark merely because a result
is inconvenient.

Proceed to manuscript drafting only after:

- this simulation is executed and archived;
- CI/tests pass;
- a target-aware DRD/ECD-style comparison is implemented fairly;
- one real ML deployment-threshold case is reproduced;
- a final literature search supports a defensible novelty boundary.

If the target-aware baseline matches the proposed planning layer, the paper must
frame the contribution as the statistically valid evidence-to-planning interface
and obstruction semantics, if those remain novel after literature review.

If prior work covers that complete interface too, do not claim a new method.
