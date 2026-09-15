# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Matched small benchmark against an exact target-aware DP baseline.

The benchmark deliberately separates two questions:
1. once a finite world table is supplied, what is the exact target-identification
   policy?  The DP answers this and represents established planning structure;
2. where did the admissible worlds come from?  In the proposed pipeline they
   are induced from finite statistical evidence before planning.

If the evidence-first planning layer reduces to the same finite DP after world
construction, the paper must not claim a new planner.
"""

from underdetermination.exact_target_dp import DeterministicExperiment, exact_target_dp


def main():
    # Two unresolved subgroup target bits after the evidence layer:
    # M = moderate subgroup passes threshold, R = rare subgroup passes threshold.
    # Global deployment target is conjunction M AND R.
    worlds = ("00", "01", "10", "11")
    target = {w: (w == "11") for w in worlds}

    experiments = (
        DeterministicExperiment(
            "moderate",
            26762.5,
            {"00": 0, "01": 0, "10": 1, "11": 1},
        ),
        DeterministicExperiment(
            "rare",
            85640.0,
            {"00": 0, "01": 1, "10": 0, "11": 1},
        ),
    )

    result = exact_target_dp(worlds, target, experiments)
    print("EXACT TARGET-AWARE DP:", result)
    print("Expected finite-table worst case: all-PASS world requires both subgroup certificates.")
    print("Evidence-first sequential result: cost=112402.5, first_experiment=moderate")

    assert result.status == "EXPERIMENT"
    assert result.worst_case_cost == 112402.5
    assert result.first_experiment == "moderate"

    print("MATCH=YES")
    print("INTERPRETATION: on this supplied finite deterministic planning problem, the planner is subsumed by the exact target-aware DP. Do not claim planner novelty. The surviving contribution must be tested/framed at the statistical evidence-to-admissible-world interface and obstruction semantics.")


if __name__ == "__main__":
    main()
