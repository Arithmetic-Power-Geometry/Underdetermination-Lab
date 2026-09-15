# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from underdetermination.core import compatible_worlds, incompatible_pair, cheapest_experiment


def main() -> None:
    # Current knowledge: 17 successes in 20 Bernoulli trials.
    successes, trials = 17, 20
    alpha = 0.05
    decision_threshold = 0.80
    tau = 0.80

    theta_grid = [i / 100 for i in range(1, 100)]
    worlds = compatible_worlds(successes, trials, theta_grid, alpha=alpha)
    pair = incompatible_pair(worlds, decision_threshold=decision_threshold)

    print(f"Observed knowledge K: {successes}/{trials} successes")
    print(f"Compatible theta range on grid: {worlds[0].theta:.2f} to {worlds[-1].theta:.2f}")

    if pair is None:
        print("No mutually incompatible worlds remain across the decision threshold.")
        return

    print(
        "Boundary-straddling incompatible worlds: "
        f"theta_low={pair[0].theta:.2f}, theta_high={pair[1].theta:.2f}"
    )

    result = cheapest_experiment(
        pair,
        candidate_sample_sizes=range(1, 5001),
        tau=tau,
        cost_per_observation=1.0,
    )

    if result is None:
        print("No candidate experiment separates the worlds at the requested strength.")
        return

    print("Cheapest separating experiment:")
    print(f"  additional observations = {result.sample_size}")
    print(f"  cost                    = {result.cost:.0f}")
    print(f"  total-variation distance= {result.tv_distance:.4f}")
    print("  minimality verified by exhaustive increasing-cost search")


if __name__ == "__main__":
    main()
