# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from underdetermination.core import (
    compatible_worlds,
    incompatible_pair,
    cheapest_experiment,
    total_variation_binomial,
)


def test_compatible_worlds_nonempty():
    grid = [i / 100 for i in range(1, 100)]
    worlds = compatible_worlds(17, 20, grid, alpha=0.05)
    assert worlds
    assert min(w.theta for w in worlds) < 0.80
    assert max(w.theta for w in worlds) >= 0.80


def test_incompatible_pair_straddles_threshold():
    grid = [i / 100 for i in range(1, 100)]
    worlds = compatible_worlds(17, 20, grid, alpha=0.05)
    pair = incompatible_pair(worlds, decision_threshold=0.80)
    assert pair is not None
    assert pair[0].theta < 0.80 <= pair[1].theta


def test_tv_increases_for_more_samples_on_fixed_worlds():
    p, q = 0.70, 0.90
    assert total_variation_binomial(50, p, q) > total_variation_binomial(5, p, q)


def test_cheapest_experiment_is_minimal_over_candidates():
    pair = type("PairHolder", (), {})
    from underdetermination.core import World
    worlds = (World(0.70), World(0.90))
    result = cheapest_experiment(worlds, range(1, 501), tau=0.80)
    assert result is not None
    for m in range(1, result.sample_size):
        assert total_variation_binomial(m, 0.70, 0.90) < 0.80


def test_returns_none_when_budget_cannot_separate():
    from underdetermination.core import World
    worlds = (World(0.79), World(0.80))
    result = cheapest_experiment(worlds, range(1, 5), tau=0.99)
    assert result is None
