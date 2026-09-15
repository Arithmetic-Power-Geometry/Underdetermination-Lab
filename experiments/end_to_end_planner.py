# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""End-to-end paper-gate example.

Current finite evidence induces admissible Bernoulli worlds. Candidate future
experiments have heterogeneous costs/noise. We ask for the cheapest experiment
that separates every currently admissible world implying DEPLOY from every one
implying DO-NOT-DEPLOY. If none can do so, we report an obstruction.
"""

from underdetermination.core import World, compatible_worlds
from underdetermination.planner import CandidateExperiment, cheapest_decisive_experiment


def binary_law(theta: float, sensitivity: float):
    # A deliberately simple noisy measurement channel whose positive probability
    # is pulled toward 1/2 as sensitivity decreases.
    p = 0.5 + sensitivity * (theta - 0.5)
    return {1: p, 0: 1.0 - p}


def main():
    grid = [i / 100 for i in range(1, 100)]
    worlds = compatible_worlds(successes=17, trials=20, theta_grid=grid, alpha=0.05)
    ids = [w.theta for w in worlds]
    threshold = 0.80
    decision = lambda theta: "DEPLOY" if theta >= threshold else "DO_NOT_DEPLOY"

    # Same admissible worlds; candidate measurements differ in cost and fidelity.
    # Repetition is represented by sharper channels here only as a controlled
    # finite-outcome benchmark. Real applications should supply empirical laws.
    candidates = [
        CandidateExperiment(
            "cheap_noisy_panel",
            1.0,
            {t: binary_law(t, 0.35) for t in ids},
        ),
        CandidateExperiment(
            "standard_panel",
            3.0,
            {t: binary_law(t, 0.75) for t in ids},
        ),
        CandidateExperiment(
            "high_fidelity_panel",
            8.0,
            {t: binary_law(t, 1.00) for t in ids},
        ),
    ]

    print(f"compatible worlds: {min(ids):.2f}..{max(ids):.2f} ({len(ids)} grid worlds)")
    print(f"decision threshold: {threshold:.2f}")

    # First show that demanding strong one-step separation is impossible for
    # these near-boundary worlds.
    strict = cheapest_decisive_experiment(ids, decision, candidates, min_tv=0.20)
    print("strict target:", strict)

    # A weaker target may still be impossible: this is useful because the
    # planner must abstain rather than select a superficially informative test.
    weak = cheapest_decisive_experiment(ids, decision, candidates, min_tv=0.01)
    print("weak target:", weak)

    # Restrict to a scientifically declared margin, not a hidden grid artifact.
    margin = 0.10
    margin_ids = [t for t in ids if t <= threshold - margin or t >= threshold + margin]
    margin_plan = cheapest_decisive_experiment(
        margin_ids, decision, candidates, min_tv=0.10
    )
    print(f"margin={margin:.2f} plan:", margin_plan)

    # Budget obstruction is separately certified.
    budget_plan = cheapest_decisive_experiment(
        margin_ids, decision, candidates, min_tv=0.10, budget=2.0
    )
    print("budget=2 plan:", budget_plan)


if __name__ == "__main__":
    main()
