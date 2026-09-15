# Continuous Decision-Boundary Obstruction

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Licensed under the Apache License, Version 2.0.

## Setup

Let the current finite evidence K induce a statistically compatible Bernoulli parameter set C(K) subset (0,1). Let d in (0,1) be a decision threshold. Worlds theta<d and theta>=d imply incompatible decisions. An additional experiment consists of m iid Bernoulli observations. For two worlds p,q, define discrimination by total variation TV(Bin(m,p), Bin(m,q)). Fix any required separation tau>0.

## Theorem 1: No finite uniform resolver at an interior decision boundary

If C(K) contains an open neighbourhood of d, then for every finite m and every tau>0 there exist p,q in C(K), with p<d<=q, such that

TV(Bin(m,p), Bin(m,q)) < tau.

Therefore no finite fixed-size iid Bernoulli experiment uniformly separates every decision-incompatible pair left by K at positive TV threshold tau. Equivalently, the worst-case finite resolution cost is infinite.

### Proof

For fixed finite m, the Binomial probability mass function is continuous in its Bernoulli parameter. Hence TV(Bin(m,p),Bin(m,q)) is continuous in (p,q), and equals zero when p=q=d. Since d is an interior point of C(K), choose epsilon>0 sufficiently small that p=d-epsilon and q=d+epsilon both lie in C(K). By continuity, TV(Bin(m,d-epsilon),Bin(m,d+epsilon)) tends to zero as epsilon tends to zero. Thus for every tau>0 one can choose epsilon so that the TV distance is below tau. Since this holds for every finite m, no finite m uniformly resolves all incompatible pairs. QED.

## Corollary 1: The 10,705 result was a grid result, not the continuous worst case

The earlier pair 0.79 versus 0.80 arose because the implementation discretised theta at spacing 0.01. In the continuous compatible set there are pairs arbitrarily closer to the threshold, e.g. 0.7999 versus 0.8000, 0.79999 versus 0.8000, etc. Their required discrimination cost grows without a finite worst-case bound. Therefore the scientifically correct continuous statement is C_resolve(K)=infinity whenever the compatible set crosses the decision boundary with no margin.

## Theorem 2: Margin restores finite resolvability

Suppose instead that admissible incompatible worlds obey a decision margin gamma>0: p<=d-gamma and q>=d+gamma. For a compact compatible parameter set contained in [a,b] subset (0,1), the pair classes are separated by at least 2 gamma. Standard consistency of iid Bernoulli testing implies that for every tau<1 there exists a finite m such that all such margin-separated pairs attain TV at least tau. Thus the obstruction is specifically caused by zero-margin underdetermination at the decision boundary.

## Consequence

This yields a principled three-way output for an underdetermination-aware scientific agent:

1. RESOLVED: current compatible worlds imply the same decision.
2. FINITELY RESOLVABLE: incompatible worlds remain but are separated by a declared positive margin and a finite experiment reaches the requested discrimination level.
3. CONTINUOUS OBSTRUCTION: incompatible compatible worlds approach the decision boundary arbitrarily closely; no finite fixed-size experiment uniformly resolves them at positive discrimination threshold.

## Expose versus resolve

The cheapest experiment that exposes the existence of some strongly separated compatible worlds can remain finite while the worst-case cost of resolving all decision disagreement is infinite. Thus the earlier finite expose/resolve ratio understates the continuous phenomenon. In the zero-margin case the ratio is unbounded/infinite whenever the exposure cost is finite.

## Novelty boundary

The mathematical ingredients (continuity of statistical experiments, hypothesis-testing difficulty for nearby parameters, version spaces, active learning and cost-sensitive experiment selection) are classical. The defensible contribution, if retained after a full literature review, is not the continuity theorem by itself. It is the proposed operational contract that begins from finite evidence, constructs the statistically compatible world set, detects target/decision disagreement, computes the cheapest permitted discriminating experiment when a positive margin makes this possible, and explicitly returns a typed obstruction instead of forcing a decision when no finite uniform resolver exists.
