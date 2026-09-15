# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from __future__ import annotations

from dataclasses import dataclass
from math import exp, lgamma, log
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class World:
    theta: float


@dataclass(frozen=True)
class ExperimentResult:
    sample_size: int
    cost: float
    theta_low: float
    theta_high: float
    tv_distance: float


def _log_binom_coeff(n: int, k: int) -> float:
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def binom_pmf(k: int, n: int, p: float) -> float:
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return exp(
        _log_binom_coeff(n, k)
        + k * log(p)
        + (n - k) * log(1.0 - p)
    )


def two_sided_exact_pvalue(s: int, n: int, theta: float) -> float:
    """Exact two-sided binomial p-value by probability ordering."""
    observed = binom_pmf(s, n, theta)
    probs = [binom_pmf(k, n, theta) for k in range(n + 1)]
    return min(1.0, sum(prob for prob in probs if prob <= observed + 1e-15))


def compatible_worlds(
    successes: int,
    trials: int,
    theta_grid: Iterable[float],
    alpha: float = 0.05,
) -> List[World]:
    worlds: List[World] = []
    for theta in theta_grid:
        if two_sided_exact_pvalue(successes, trials, theta) >= alpha:
            worlds.append(World(float(theta)))
    return worlds


def incompatible_pair(
    worlds: Iterable[World], decision_threshold: float = 0.80
) -> Optional[Tuple[World, World]]:
    below = [w for w in worlds if w.theta < decision_threshold]
    above = [w for w in worlds if w.theta >= decision_threshold]
    if not below or not above:
        return None
    return max(below, key=lambda w: w.theta), min(above, key=lambda w: w.theta)


def total_variation_binomial(n: int, p: float, q: float) -> float:
    return 0.5 * sum(
        abs(binom_pmf(k, n, p) - binom_pmf(k, n, q)) for k in range(n + 1)
    )


def cheapest_experiment(
    pair: Tuple[World, World],
    candidate_sample_sizes: Iterable[int],
    tau: float = 0.80,
    cost_per_observation: float = 1.0,
) -> Optional[ExperimentResult]:
    low, high = pair
    for m in sorted(candidate_sample_sizes):
        tv = total_variation_binomial(m, low.theta, high.theta)
        if tv >= tau:
            return ExperimentResult(
                sample_size=m,
                cost=m * cost_per_observation,
                theta_low=low.theta,
                theta_high=high.theta,
                tv_distance=tv,
            )
    return None
