# Cost-to-Resolution Results

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Question

Find the cheapest Bernoulli experiment whose outcome distribution separates two mutually incompatible worlds that remain compatible with current finite evidence.

For a pair of worlds with success probabilities `p < q`, an experiment of cost `m` collects `m` additional independent Bernoulli observations. Separation is measured by total variation distance between `Binomial(m,p)` and `Binomial(m,q)`. The target used here is `TV >= 0.80`.

## Exact discrete search results

| World 1 | World 2 | Minimum m | TV at m-1 | TV at m |
|---:|---:|---:|---:|---:|
| 0.70 | 0.90 | 24 | 0.791284 | 0.803850 |
| 0.75 | 0.85 | 103 | 0.796272 | 0.800264 |
| 0.79 | 0.80 | 10,705 | 0.799965 | 0.800006 |

Thus, under unit cost per new observation, the exact cheapest costs for these three tests are 24, 103, and 10,705 observations respectively.

## What the experiment establishes

The cost is not determined merely by the fact that two worlds disagree. It depends sharply on how close their predictive laws are. Decision-incompatible worlds arbitrarily close to a threshold can require orders of magnitude more evidence than widely separated worlds.

This yields a practical three-regime interpretation once a budget B is specified:

1. **Cheaply resolvable:** `m* << B`.
2. **Expensively resolvable:** `m*` is comparable with `B`.
3. **Unresolved within budget:** `m* > B` or no candidate experiment reaches the required separation.

The third regime is essential: the framework is allowed to return that current ambiguity cannot be resolved at the available experimental cost.

## Novelty boundary

The result above is not claimed as a new theorem: binary hypothesis testing and experimental design already imply that closer distributions require more samples to discriminate. The research candidate is narrower: generate the mutually incompatible worlds from the underdetermination left by observed ML/statistical summaries, then compute the minimum-cost experiment needed to resolve the decision-relevant ambiguity.

## Next falsification test

Replace the hand-selected Bernoulli worlds with worlds automatically induced from an ML classifier's finite validation evidence. Then compare the experiment selected by the underdetermination-driven procedure against standard information-gain / model-discrimination selection. A genuine contribution requires a case where the new formulation adds a capability or guarantee rather than merely renaming classical experimental design.
