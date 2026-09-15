# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""Paper-gate benchmark for evidence-induced decision resolution.

The benchmark tests the part of the framework that must survive before a paper
is written: finite evidence induces an admissible set; decisions are issued only
when all admissible worlds agree; otherwise the method returns an experiment or
an obstruction.

This script deliberately separates statistical validity from planning novelty.
"""

from dataclasses import dataclass
from math import lgamma, log, exp
from random import Random

ALPHA = 0.05
THRESHOLD = 0.80
GRID = tuple(i / 100 for i in range(1, 100))


def log_binom_pmf(k, n, p):
    if p <= 0 or p >= 1:
        return 0.0 if (p == 0 and k == 0) or (p == 1 and k == n) else float('-inf')
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
            + k * log(p) + (n-k) * log(1-p))


def exact_two_sided_pvalue(k, n, p):
    obs = log_binom_pmf(k, n, p)
    vals = [log_binom_pmf(j, n, p) for j in range(n + 1)]
    # Probability-ordering exact two-sided binomial test.
    return min(1.0, sum(exp(v) for v in vals if v <= obs + 1e-12))


def compatible(k, n, alpha=ALPHA):
    return [p for p in GRID if exact_two_sided_pvalue(k, n, p) >= alpha]


def decision_state(worlds, threshold=THRESHOLD):
    if not worlds:
        return 'EMPTY'
    ds = {p >= threshold for p in worlds}
    if len(ds) == 1:
        return 'DEPLOY' if True in ds else 'DO_NOT_DEPLOY'
    return 'UNRESOLVED'


def coverage_trial(true_p, n, rng):
    k = sum(rng.random() < true_p for _ in range(n))
    return true_p in compatible(k, n)


def false_decision_trial(true_p, n, rng):
    k = sum(rng.random() < true_p for _ in range(n))
    state = decision_state(compatible(k, n))
    if state in ('UNRESOLVED', 'EMPTY'):
        return False
    truth = 'DEPLOY' if true_p >= THRESHOLD else 'DO_NOT_DEPLOY'
    return state != truth


def run(seed=20260915, reps=2000):
    rng = Random(seed)
    ps = (0.65, 0.72, 0.78, 0.79, 0.81, 0.82, 0.88, 0.95)
    ns = (20, 50, 100)
    rows = []
    for n in ns:
        for p in ps:
            cov = sum(coverage_trial(p, n, rng) for _ in range(reps)) / reps
            wrong = sum(false_decision_trial(p, n, rng) for _ in range(reps)) / reps
            rows.append((n, p, cov, wrong))
    print('n,true_p,coverage,false_decision_rate')
    for row in rows:
        print(f'{row[0]},{row[1]:.2f},{row[2]:.4f},{row[3]:.4f}')
    print('\nInterpretation:')
    print('* coverage checks whether the evidence-induced world set contains truth;')
    print('* false_decision_rate checks whether unanimity over that set can certify the wrong side;')
    print('* near 0.80, abstention/unresolved outcomes are expected and are a feature, not a failure.')


if __name__ == '__main__':
    run()
