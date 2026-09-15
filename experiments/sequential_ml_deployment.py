# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Correct global conjunction semantics for the controlled ML deployment case."""

from experiments.ml_deployment_case import (
    GroupEvidence,
    admissible_interval,
    minimum_additional_labels,
    state,
)
from underdetermination.sequential_dp import CertificationExperiment, minimax_conjunction_plan


def main():
    groups = [
        GroupEvidence("common", 94, 100, 1.0),
        GroupEvidence("moderate", 45, 50, 2.5),
        GroupEvidence("rare", 17, 20, 8.0),
    ]

    certs = []
    print("GLOBAL TARGET: DEPLOY iff every subgroup passes the 0.80 floor")
    for g in groups:
        interval = admissible_interval(g)
        s = state(interval)
        print(g.name, interval, s)
        if s == "FAIL":
            print("GLOBAL DECISION=DO_NOT_DEPLOY; no further experiment required")
            return
        if s == "UNRESOLVED":
            m, pair = minimum_additional_labels(interval)
            if m is None:
                print("GLOBAL OBSTRUCTION: unresolved subgroup not certifiable in finite-grid budget", g.name)
                return
            cost = m * g.label_cost
            certs.append(CertificationExperiment(g.name, cost))
            print(" certification experiment:", g.name, "pair=", pair, "labels=", m, "cost=", cost)

    if not certs:
        print("GLOBAL DECISION=DEPLOY; all subgroups already certified")
        return

    plan = minimax_conjunction_plan(certs)
    print("MINIMAX GLOBAL PLAN:", plan)
    print("Interpretation: a FAIL at any tested subgroup stops with DO_NOT_DEPLOY; the worst case is the all-PASS world, in which every unresolved subgroup must be certified.")


if __name__ == "__main__":
    main()
