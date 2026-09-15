# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

from underdetermination.planner import CandidateExperiment, cheapest_decisive_experiment


def deterministic_laws(worlds, reveal):
    return {w: {reveal(w): 1.0} for w in worlds}


def test_already_resolved():
    worlds = [0, 1]
    result = cheapest_decisive_experiment(
        worlds,
        lambda w: 0,
        [],
        min_tv=1.0,
    )
    assert result.status == "RESOLVED"
    assert result.cost == 0.0


def test_selects_cheapest_decisive_not_most_world_informative():
    worlds = [(y, z1, z2) for y in (0, 1) for z1 in (0, 1) for z2 in (0, 1)]
    decision = lambda w: w[0]

    nuisance = CandidateExperiment(
        "nuisance_two_bits",
        1.0,
        deterministic_laws(worlds, lambda w: (w[1], w[2])),
    )
    target = CandidateExperiment(
        "target_one_bit",
        2.0,
        deterministic_laws(worlds, lambda w: w[0]),
    )

    result = cheapest_decisive_experiment(
        worlds, decision, [nuisance, target], min_tv=1.0
    )
    assert result.status == "EXPERIMENT"
    assert result.experiment == "target_one_bit"
    assert result.cost == 2.0


def test_obstruction_when_no_candidate_resolves_all_conflicts():
    worlds = [0, 1]
    exp = CandidateExperiment(
        "uninformative",
        1.0,
        {0: {0: 0.5, 1: 0.5}, 1: {0: 0.5, 1: 0.5}},
    )
    result = cheapest_decisive_experiment(
        worlds, lambda w: w, [exp], min_tv=0.2
    )
    assert result.status == "OBSTRUCTION"


def test_budget_obstruction():
    worlds = [0, 1]
    exp = CandidateExperiment(
        "perfect_but_expensive",
        5.0,
        deterministic_laws(worlds, lambda w: w),
    )
    result = cheapest_decisive_experiment(
        worlds, lambda w: w, [exp], min_tv=1.0, budget=2.0
    )
    assert result.status == "OBSTRUCTION"
