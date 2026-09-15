# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""Decision-oriented planning over statistically admissible worlds.

This module deliberately separates two layers:
1. an evidence layer supplies a set of statistically admissible worlds;
2. a planning layer asks for the cheapest candidate experiment that can
   distinguish every pair of worlds that imply different decisions.

For a finite world set and finite-outcome experiments this is an exact,
transparent one-step criterion. It is not claimed to replace sequential
DRD/ECD methods; it is a reproducible paper-gate baseline.
"""

from dataclasses import dataclass
from math import isclose
from typing import Callable, Hashable, Iterable, Mapping, Optional, Sequence


WorldId = Hashable
Outcome = Hashable


@dataclass(frozen=True)
class CandidateExperiment:
    name: str
    cost: float
    # world -> outcome -> probability
    laws: Mapping[WorldId, Mapping[Outcome, float]]


@dataclass(frozen=True)
class PlanResult:
    status: str  # RESOLVED, EXPERIMENT, or OBSTRUCTION
    experiment: Optional[str]
    cost: Optional[float]
    reason: str


def total_variation_discrete(p: Mapping[Outcome, float], q: Mapping[Outcome, float]) -> float:
    outcomes = set(p) | set(q)
    return 0.5 * sum(abs(p.get(y, 0.0) - q.get(y, 0.0)) for y in outcomes)


def validate_experiment(exp: CandidateExperiment, worlds: Sequence[WorldId]) -> None:
    if exp.cost < 0:
        raise ValueError("experiment cost must be nonnegative")
    for w in worlds:
        if w not in exp.laws:
            raise ValueError(f"missing law for world {w!r} in {exp.name}")
        probs = exp.laws[w]
        if any(v < 0 for v in probs.values()):
            raise ValueError("negative probability")
        if not isclose(sum(probs.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError(f"probabilities for {w!r} do not sum to one")


def cross_decision_pairs(worlds: Sequence[WorldId], decision: Callable[[WorldId], Hashable]):
    for i, a in enumerate(worlds):
        for b in worlds[i + 1 :]:
            if decision(a) != decision(b):
                yield a, b


def cheapest_decisive_experiment(
    worlds: Iterable[WorldId],
    decision: Callable[[WorldId], Hashable],
    experiments: Iterable[CandidateExperiment],
    min_tv: float,
    budget: Optional[float] = None,
) -> PlanResult:
    """Return the cheapest one-step experiment separating all decision conflicts.

    An experiment is admissible when every pair of currently admissible worlds
    with different target decisions has total-variation separation >= min_tv.
    If no cross-decision pair remains, current knowledge is already resolved.
    If no candidate passes, return an explicit obstruction rather than inventing
    a decision.
    """
    if not 0 <= min_tv <= 1:
        raise ValueError("min_tv must lie in [0,1]")

    worlds = list(worlds)
    experiments = list(experiments)
    pairs = list(cross_decision_pairs(worlds, decision))
    if not pairs:
        return PlanResult("RESOLVED", None, 0.0, "all admissible worlds imply the same decision")

    feasible = []
    for exp in experiments:
        validate_experiment(exp, worlds)
        if budget is not None and exp.cost > budget:
            continue
        worst = min(
            total_variation_discrete(exp.laws[a], exp.laws[b])
            for a, b in pairs
        )
        if worst >= min_tv:
            feasible.append((exp.cost, exp.name, worst))

    if not feasible:
        reason = "no candidate experiment separates every cross-decision admissible pair"
        if budget is not None:
            reason += f" within budget {budget}"
        return PlanResult("OBSTRUCTION", None, None, reason)

    cost, name, worst = min(feasible, key=lambda x: (x[0], x[1]))
    return PlanResult(
        "EXPERIMENT",
        name,
        cost,
        f"minimum cost; worst cross-decision TV={worst:.6f}",
    )
