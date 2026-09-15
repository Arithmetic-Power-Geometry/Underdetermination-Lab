# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from underdetermination.exact_target_dp import DeterministicExperiment, exact_target_dp


def test_resolved_without_experiment():
    r = exact_target_dp(("a", "b"), {"a": 1, "b": 1}, ())
    assert r.status == "RESOLVED"
    assert r.worst_case_cost == 0


def test_conjunction_exact_cost():
    worlds = ("00", "01", "10", "11")
    target = {w: w == "11" for w in worlds}
    exps = (
        DeterministicExperiment("a", 2.0, {"00": 0, "01": 0, "10": 1, "11": 1}),
        DeterministicExperiment("b", 5.0, {"00": 0, "01": 1, "10": 0, "11": 1}),
    )
    r = exact_target_dp(worlds, target, exps)
    assert r.status == "EXPERIMENT"
    assert r.worst_case_cost == 7.0
    assert r.first_experiment == "a"


def test_obstruction_when_worlds_with_different_targets_are_indistinguishable():
    worlds = ("x", "y")
    target = {"x": 0, "y": 1}
    exps = (DeterministicExperiment("same", 1.0, {"x": 0, "y": 0}),)
    r = exact_target_dp(worlds, target, exps)
    assert r.status == "OBSTRUCTION"


def test_cheaper_policy_selected():
    worlds = ("n", "y")
    target = {"n": 0, "y": 1}
    exps = (
        DeterministicExperiment("expensive", 9.0, {"n": 0, "y": 1}),
        DeterministicExperiment("cheap", 3.0, {"n": 0, "y": 1}),
    )
    r = exact_target_dp(worlds, target, exps)
    assert r.worst_case_cost == 3.0
    assert r.first_experiment == "cheap"
