# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from underdetermination.sequential_dp import CertificationExperiment, minimax_conjunction_plan


def test_empty_state_is_resolved():
    p = minimax_conjunction_plan([])
    assert p.worst_case_cost == 0
    assert p.first_experiment is None
    assert p.order == ()


def test_two_unresolved_groups_worst_case_requires_both():
    p = minimax_conjunction_plan([
        CertificationExperiment("moderate", 26762.5),
        CertificationExperiment("rare", 85640.0),
    ])
    assert p.worst_case_cost == 112402.5
    assert set(p.order) == {"moderate", "rare"}


def test_single_failure_can_terminate_but_minimax_counts_all_pass_world():
    p = minimax_conjunction_plan([
        CertificationExperiment("a", 2.0),
        CertificationExperiment("b", 5.0),
        CertificationExperiment("c", 7.0),
    ])
    assert p.worst_case_cost == 14.0
    assert len(p.order) == 3


def test_rejects_nonpositive_cost():
    try:
        minimax_conjunction_plan([CertificationExperiment("bad", 0.0)])
    except ValueError:
        return
    assert False, "expected ValueError"
