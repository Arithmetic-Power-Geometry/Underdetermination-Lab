# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Exact finite deterministic target-identification dynamic program.

This is a transparent DRD/ECD-style baseline for small benchmarks. Candidate
worlds, their target labels, experiment costs, and deterministic observations
are supplied explicitly. The solver minimizes worst-case remaining experiment
cost until all worlds in the surviving version space have the same target.

No novelty is claimed for this dynamic program.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import Hashable, Mapping, Tuple


World = Hashable
Outcome = Hashable


@dataclass(frozen=True)
class DeterministicExperiment:
    name: str
    cost: float
    observations: Mapping[World, Outcome]


@dataclass(frozen=True)
class ExactDPResult:
    status: str
    worst_case_cost: float | None
    first_experiment: str | None
    reason: str


def exact_target_dp(
    worlds: Tuple[World, ...],
    target: Mapping[World, Hashable],
    experiments: Tuple[DeterministicExperiment, ...],
) -> ExactDPResult:
    if not worlds:
        raise ValueError("world set must be nonempty")
    if any(w not in target for w in worlds):
        raise ValueError("target missing for a world")
    if any(e.cost <= 0 for e in experiments):
        raise ValueError("experiment costs must be positive")
    if len({e.name for e in experiments}) != len(experiments):
        raise ValueError("experiment names must be unique")
    for e in experiments:
        if any(w not in e.observations for w in worlds):
            raise ValueError(f"experiment {e.name} missing world observation")

    exp_by_name = {e.name: e for e in experiments}
    exp_names = tuple(sorted(exp_by_name))

    @lru_cache(maxsize=None)
    def solve(state: Tuple[World, ...], remaining: Tuple[str, ...]):
        labels = {target[w] for w in state}
        if len(labels) <= 1:
            return 0.0, None
        if not remaining:
            return float("inf"), None

        best = float("inf")
        best_name = None
        for name in remaining:
            e = exp_by_name[name]
            cells = {}
            for w in state:
                cells.setdefault(e.observations[w], []).append(w)
            # An experiment that does not shrink this state cannot help here.
            if len(cells) == 1:
                continue
            next_remaining = tuple(x for x in remaining if x != name)
            worst = 0.0
            feasible = True
            for cell in cells.values():
                child = tuple(sorted(cell, key=repr))
                child_cost, _ = solve(child, next_remaining)
                if child_cost == float("inf"):
                    feasible = False
                    break
                worst = max(worst, child_cost)
            if not feasible:
                continue
            candidate = e.cost + worst
            if candidate < best or (candidate == best and (best_name is None or name < best_name)):
                best = candidate
                best_name = name
        return best, best_name

    initial = tuple(sorted(worlds, key=repr))
    cost, first = solve(initial, exp_names)
    if cost == float("inf"):
        return ExactDPResult("OBSTRUCTION", None, None, "no supplied experiment policy resolves the target in every world")
    if first is None:
        return ExactDPResult("RESOLVED", 0.0, None, "target already constant on the admissible world set")
    return ExactDPResult("EXPERIMENT", cost, first, "exact minimum worst-case cost over the supplied finite deterministic benchmark")
