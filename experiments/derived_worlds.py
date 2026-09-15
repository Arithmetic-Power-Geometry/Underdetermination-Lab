# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Derive possible worlds from finite evidence, then find the cheapest experiment
that separates decision-incompatible worlds.

This experiment deliberately does NOT hand the algorithm a rival pair.
"""

from underdetermination.core import compatible_worlds, cheapest_experiment, World


def run():
    # Knowledge K: 17 correct predictions among 20 relevant validation cases.
    theta_grid = [i / 100 for i in range(1, 100)]
    worlds = compatible_worlds(17, 20, theta_grid, alpha=0.05)

    # Decision: reliability below 0.80 versus reliability at/above 0.80.
    below = [w for w in worlds if w.theta < 0.80]
    above = [w for w in worlds if w.theta >= 0.80]
    assert below and above, "Current knowledge does not leave a decision contradiction."

    # For the cheapest existence witness, choose the most separated compatible
    # worlds on opposite sides of the decision. The worlds are derived from K.
    pair = (min(below, key=lambda w: w.theta), max(above, key=lambda w: w.theta))
    result = cheapest_experiment(pair, range(1, 1001), tau=0.80)

    print(f"compatible interval on grid: [{worlds[0].theta:.2f}, {worlds[-1].theta:.2f}]")
    print(f"derived incompatible worlds: {pair[0].theta:.2f} vs {pair[1].theta:.2f}")
    if result is None:
        print("no separating experiment within budget")
    else:
        print(f"cheapest additional Bernoulli experiment: n={result.sample_size}")
        print(f"TV={result.tv_distance:.6f}, cost={result.cost:.0f}")


if __name__ == "__main__":
    run()
