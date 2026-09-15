# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""Compare minimum-cost robust resolution with a target-aware ECD-style rule.

This experiment is intentionally small and inspectable. Both selectors receive
exactly the same admissible worlds, target partition, experiment laws and costs.
The proposed one-step robust rule asks for the cheapest test whose *worst*
cross-decision TV reaches tau. The ECD-style comparator maximizes weighted
cross-decision edge separation per unit cost.

A difference is a difference in objective, not automatically a novelty claim.
"""

from underdetermination.ecd_baseline import choose_ecd_style
from underdetermination.planner import CandidateExperiment, cheapest_decisive_experiment


def law(p):
    return {1: p, 0: 1-p}


def main():
    # Four admissible worlds; first two imply NO, last two YES.
    worlds = ["N_far", "N_near", "Y_near", "Y_far"]
    decision = lambda w: "NO" if w.startswith("N") else "YES"

    # Test A is cheap and performs well on most cross-target edges, but leaves
    # the near-boundary pair almost indistinguishable.
    A = CandidateExperiment(
        "average_good_but_boundary_weak", 1.0,
        {
            "N_far": law(0.05),
            "N_near": law(0.48),
            "Y_near": law(0.52),
            "Y_far": law(0.95),
        },
    )

    # Test B costs more but guarantees substantial separation for every
    # cross-target pair.
    B = CandidateExperiment(
        "robust_decision_test", 3.0,
        {
            "N_far": law(0.20),
            "N_near": law(0.20),
            "Y_near": law(0.80),
            "Y_far": law(0.80),
        },
    )

    experiments = [A, B]
    robust = cheapest_decisive_experiment(
        worlds, decision, experiments, min_tv=0.50
    )
    ecd = choose_ecd_style(worlds, decision, experiments)

    print("robust resolution:", robust)
    print("ECD-style choice:", ecd)

    assert robust.experiment == "robust_decision_test"
    # The ECD-style cost-normalized average-edge objective can prefer A.
    assert ecd.experiment == "average_good_but_boundary_weak"


if __name__ == "__main__":
    main()
