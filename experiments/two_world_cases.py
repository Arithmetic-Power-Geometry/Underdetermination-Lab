# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from underdetermination.core import World, cheapest_experiment


def run_case(name: str, low: float, high: float, tau: float, budget: int) -> None:
    result = cheapest_experiment(
        (World(low), World(high)),
        candidate_sample_sizes=range(1, budget + 1),
        tau=tau,
    )
    print(f"{name}: theta={low:.2f} vs {high:.2f}, tau={tau:.2f}, budget={budget}")
    if result is None:
        print("  obstruction: no separating experiment within budget")
    else:
        print(
            f"  cheapest m={result.sample_size}, "
            f"cost={result.cost:.0f}, TV={result.tv_distance:.4f}"
        )


def main() -> None:
    run_case("near-boundary", 0.79, 0.80, tau=0.80, budget=5000)
    run_case("clear-conflict", 0.70, 0.90, tau=0.80, budget=500)
    run_case("moderate-conflict", 0.75, 0.85, tau=0.80, budget=2000)


if __name__ == "__main__":
    main()
