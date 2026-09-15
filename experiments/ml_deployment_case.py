# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""Reproducible ML-style deployment case for the paper gate.

A fixed classifier has three deployment subgroups. Initial validation supplies
finite success/trial counts for each subgroup. Deployment requires every
subgroup accuracy to meet a pre-specified floor. The evidence layer induces
statistically admissible subgroup accuracies; the planning layer asks which
additional labelled evaluation is cheapest among the unresolved subgroups.

This is deliberately a controlled ML deployment benchmark, not a claim that
subgroup thresholding itself is novel. It isolates the evidence-to-planning
question without network/data-license dependencies.
"""

from dataclasses import dataclass
from math import lgamma, log, exp
from typing import List, Tuple

from underdetermination.core import compatible_worlds


ALPHA = 0.05
DEPLOY_FLOOR = 0.80
GRID = [i / 100 for i in range(1, 100)]


@dataclass(frozen=True)
class GroupEvidence:
    name: str
    successes: int
    trials: int
    label_cost: float


def log_binom_pmf(k: int, n: int, p: float) -> float:
    if p <= 0.0:
        return 0.0 if k == 0 else float("-inf")
    if p >= 1.0:
        return 0.0 if k == n else float("-inf")
    return (
        lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
        + k * log(p) + (n - k) * log(1 - p)
    )


def binom_pmf(k: int, n: int, p: float) -> float:
    z = log_binom_pmf(k, n, p)
    return 0.0 if z == float("-inf") else exp(z)


def binomial_tv(n: int, p: float, q: float) -> float:
    return 0.5 * sum(abs(binom_pmf(k, n, p) - binom_pmf(k, n, q)) for k in range(n + 1))


def admissible_interval(g: GroupEvidence) -> Tuple[float, float]:
    worlds = compatible_worlds(g.successes, g.trials, GRID, ALPHA)
    values = [w.theta for w in worlds]
    if not values:
        raise RuntimeError(f"empty admissible set for {g.name}")
    return min(values), max(values)


def state(interval: Tuple[float, float]) -> str:
    lo, hi = interval
    if lo >= DEPLOY_FLOOR:
        return "PASS"
    if hi < DEPLOY_FLOOR:
        return "FAIL"
    return "UNRESOLVED"


def minimum_additional_labels(interval: Tuple[float, float], tau: float = 0.80, max_m: int = 20000):
    """Finite-grid worst cross-decision sample size.

    Uses the closest admissible grid points on opposite sides of the deployment
    floor. This is explicitly a finite-grid certificate, not the continuous
    zero-margin result; the latter remains an obstruction.
    """
    lo, hi = interval
    below = [p for p in GRID if lo <= p < DEPLOY_FLOOR]
    above = [p for p in GRID if DEPLOY_FLOOR <= p <= hi]
    if not below or not above:
        return 0, None
    p, q = max(below), min(above)
    for m in range(1, max_m + 1):
        if binomial_tv(m, p, q) >= tau:
            return m, (p, q)
    return None, (p, q)


def main():
    groups: List[GroupEvidence] = [
        GroupEvidence("common", 94, 100, 1.0),
        GroupEvidence("moderate", 45, 50, 2.5),
        GroupEvidence("rare", 17, 20, 8.0),
    ]

    print("Deployment rule: all subgroup accuracies >=", DEPLOY_FLOOR)
    print("alpha:", ALPHA)
    print()

    unresolved = []
    any_fail = False
    for g in groups:
        interval = admissible_interval(g)
        s = state(interval)
        print(g.name, "evidence=", f"{g.successes}/{g.trials}", "C_alpha=", interval, "state=", s)
        if s == "FAIL":
            any_fail = True
        elif s == "UNRESOLVED":
            unresolved.append((g, interval))

    if any_fail:
        print("\nCurrent evidence already implies DO_NOT_DEPLOY under the conjunction rule.")
        return
    if not unresolved:
        print("\nCurrent evidence certifies DEPLOY.")
        return

    print("\nCurrent evidence leaves mutually incompatible deployment worlds.")
    candidates = []
    for g, interval in unresolved:
        m, pair = minimum_additional_labels(interval)
        if m is None:
            print(g.name, "finite-grid boundary not resolved within search budget", pair)
            continue
        total_cost = m * g.label_cost
        candidates.append((total_cost, g.name, m, pair, g.label_cost))
        print(
            g.name,
            "hardest-grid-pair=", pair,
            "labels=", m,
            "unit_cost=", g.label_cost,
            "total_cost=", total_cost,
        )

    if not candidates:
        print("OBSTRUCTION: no candidate evaluation resolves a finite-grid subgroup boundary within budget.")
        return

    best = min(candidates)
    print("\nCHEAPEST NEXT FINITE-GRID SUBGROUP-RESOLUTION EXPERIMENT:")
    print(
        f"evaluate {best[2]} additional labelled examples from subgroup '{best[1]}' "
        f"at total cost {best[0]:.2f}"
    )
    print("This is a next-step subgroup experiment, not by itself a global deployment certificate under the conjunction rule.")
    print("Continuous zero-margin uniform resolution remains an obstruction; a declared margin is required for a finite continuous guarantee.")


if __name__ == "__main__":
    main()
