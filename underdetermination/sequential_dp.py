# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Exact small-state minimax planner for conjunction decisions.

Each unresolved component has a certification experiment with positive cost.
An experiment returns PASS or FAIL. The global target is DEPLOY iff every
component is PASS; any FAIL immediately resolves DO_NOT_DEPLOY.

For a state S of unresolved components,
    V(S) = min_i [ c_i + max(V(S minus {i}), 0) ] = min_i [c_i + V(S minus {i})].
The explicit recursion is retained because it is the baseline form needed for
later extensions with non-binary outcomes and experiment-dependent successor
states.

This module is an exact finite dynamic-programming baseline, not a novelty
claim about decision-region determination.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Tuple


@dataclass(frozen=True)
class CertificationExperiment:
    name: str
    cost: float


@dataclass(frozen=True)
class SequentialPlan:
    worst_case_cost: float
    first_experiment: str | None
    order: Tuple[str, ...]


def minimax_conjunction_plan(experiments: Iterable[CertificationExperiment]) -> SequentialPlan:
    exps = tuple(experiments)
    if any(e.cost <= 0 for e in exps):
        raise ValueError("all experiment costs must be positive")
    if len({e.name for e in exps}) != len(exps):
        raise ValueError("experiment names must be unique")

    by_name = {e.name: e for e in exps}
    names = tuple(sorted(by_name))

    @lru_cache(maxsize=None)
    def value(state: Tuple[str, ...]) -> tuple[float, Tuple[str, ...]]:
        if not state:
            return 0.0, ()  # all components certified PASS -> DEPLOY

        best_cost = float("inf")
        best_order: Tuple[str, ...] = ()
        for name in state:
            rest = tuple(x for x in state if x != name)
            pass_cost, pass_order = value(rest)
            fail_cost = 0.0  # a FAIL resolves global DO_NOT_DEPLOY immediately
            worst_successor = max(pass_cost, fail_cost)
            candidate = by_name[name].cost + worst_successor
            candidate_order = (name,) + pass_order
            if candidate < best_cost or (
                candidate == best_cost and candidate_order < best_order
            ):
                best_cost = candidate
                best_order = candidate_order
        return best_cost, best_order

    cost, order = value(names)
    return SequentialPlan(cost, order[0] if order else None, order)
