# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""A transparent target-aware ECD-style one-step comparator.

This is not presented as a reimplementation of every detail of EC^2/ECED.
It instantiates their central comparison principle for our finite admissible
world set: put weighted edges only between worlds with different target
values, and score a test by expected cross-target edge separation per cost.

The purpose is adversarial: our proposed planner must be compared against a
baseline that already knows the target partition, not merely information gain.
"""

from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Optional

from .planner import CandidateExperiment, total_variation_discrete, validate_experiment


@dataclass(frozen=True)
class ECDChoice:
    experiment: Optional[str]
    cost: Optional[float]
    score: float


def ecd_edge_score(exp, worlds, decision, weights=None):
    worlds = list(worlds)
    validate_experiment(exp, worlds)
    if weights is None:
        weights = {w: 1.0 / len(worlds) for w in worlds}
    score = 0.0
    for i, a in enumerate(worlds):
        for b in worlds[i + 1:]:
            if decision(a) == decision(b):
                continue
            # Cross-target edge weight times observable separation.
            score += weights[a] * weights[b] * total_variation_discrete(
                exp.laws[a], exp.laws[b]
            )
    return score


def choose_ecd_style(worlds, decision, experiments, weights=None, budget=None):
    worlds = list(worlds)
    best = None
    for exp in experiments:
        if budget is not None and exp.cost > budget:
            continue
        raw = ecd_edge_score(exp, worlds, decision, weights)
        value = raw / exp.cost if exp.cost > 0 else float("inf")
        candidate = (value, -exp.cost, exp.name, exp)
        if best is None or candidate[:3] > best[:3]:
            best = candidate
    if best is None:
        return ECDChoice(None, None, 0.0)
    value, _, _, exp = best
    return ECDChoice(exp.name, exp.cost, value)
