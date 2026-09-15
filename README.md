# Underdetermination Lab

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Licensed under the Apache License, Version 2.0.

## Research question

> Find the cheapest experiment for which the current knowledge leaves mutually incompatible possible worlds.

This repository tests a narrow version of that principle for machine learning, probability, and statistics.

The key restriction is important: the competing worlds are **not supplied in advance**. They are generated from the set of latent Bernoulli worlds that remain statistically compatible with observed knowledge.

Given observed evidence `K=(s,n)` from `s` successes in `n` Bernoulli trials, define the compatible-world set

`W(K) = { theta in Theta : K is not rejected under theta at level alpha }`.

Candidate experiments add `m` new Bernoulli observations at a specified cost. For each candidate experiment, we ask whether there are two worlds in `W(K)` whose predictive distributions for that experiment are sufficiently separated. The search returns the minimum-cost such experiment.

## What this does *not* claim

The general idea of minimum-cost experiment selection is classical in active learning, optimal experimental design, and model discrimination. This repository tests a narrower question: whether partial statistical evidence can itself induce unresolved, decision-relevant worlds and whether we can compute the cheapest additional observation budget needed to separate them.

## First falsifiable experiment

1. Start with finite evidence `s/n`.
2. Build the set of Bernoulli parameters still statistically compatible with that evidence.
3. Choose mutually incompatible worlds from opposite sides of a decision threshold.
4. For each candidate additional sample size `m`, compute the total-variation distance between the predictive Binomial distributions under those worlds.
5. Return the smallest `m` whose separation exceeds a chosen threshold `tau`.
6. Verify that no cheaper candidate succeeds.

Run:

```bash
python experiments/cheapest_experiment.py
pytest -q
```

## Interpretation

A positive result does **not** establish a new general theory. It establishes an executable proof-of-concept for the narrower pipeline:

`partial knowledge -> compatible worlds -> incompatible decisions -> minimum-cost separating experiment`.

A negative result is equally useful: if no affordable experiment separates the compatible worlds at the required strength, the program reports that obstruction instead of inventing an answer.
