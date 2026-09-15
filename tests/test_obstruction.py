# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from underdetermination.obstruction import resolution_certificate


def test_same_decision_is_already_resolved():
    r = resolution_certificate(0.83, 0.95, 0.80)
    assert r.status == "RESOLVED"
    assert r.sample_size == 0


def test_crossing_without_margin_is_continuous_obstruction():
    r = resolution_certificate(0.63, 0.95, 0.80, tau=0.80)
    assert r.status == "CONTINUOUS_OBSTRUCTION"
    assert r.sample_size is None


def test_positive_margin_is_finitely_resolvable():
    r = resolution_certificate(0.63, 0.95, 0.80, tau=0.80, margin=0.05, max_sample_size=1000)
    assert r.status == "FINITELY_RESOLVABLE"
    assert r.sample_size is not None
    assert 1 <= r.sample_size <= 1000
    assert r.tv_distance is not None and r.tv_distance >= 0.80


def test_tiny_margin_can_hit_budget_obstruction():
    r = resolution_certificate(0.63, 0.95, 0.80, tau=0.80, margin=0.001, max_sample_size=100)
    assert r.status == "BUDGET_OBSTRUCTION"
