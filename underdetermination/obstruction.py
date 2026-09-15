# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .core import World, cheapest_experiment


@dataclass(frozen=True)
class ResolutionCertificate:
    status: str
    reason: str
    sample_size: Optional[int] = None
    cost: Optional[float] = None
    tv_distance: Optional[float] = None


def resolution_certificate(
    compatible_low: float,
    compatible_high: float,
    decision_threshold: float,
    tau: float = 0.80,
    margin: float = 0.0,
    max_sample_size: int = 100_000,
    cost_per_observation: float = 1.0,
) -> ResolutionCertificate:
    """Return resolved, finite-resolution, budget-obstruction, or continuous-obstruction certificate.

    The compatible set is represented as a continuous interval [low, high].
    A zero margin with the decision threshold in the interval implies arbitrarily
    close decision-incompatible worlds and hence no finite uniform TV resolver.
    """
    if compatible_high < decision_threshold or compatible_low >= decision_threshold:
        return ResolutionCertificate(
            "RESOLVED",
            "All compatible worlds induce the same threshold decision.",
            sample_size=0,
            cost=0.0,
            tv_distance=1.0,
        )

    if margin <= 0.0:
        return ResolutionCertificate(
            "CONTINUOUS_OBSTRUCTION",
            "Compatible worlds approach the decision threshold from opposite sides; no finite fixed-size experiment uniformly separates every pair at positive TV threshold.",
        )

    p = decision_threshold - margin
    q = decision_threshold + margin
    if p < compatible_low or q > compatible_high:
        return ResolutionCertificate(
            "INVALID_MARGIN",
            "The requested symmetric margin pair is not contained in the compatible interval.",
        )

    result = cheapest_experiment(
        (World(p), World(q)),
        range(1, max_sample_size + 1),
        tau=tau,
        cost_per_observation=cost_per_observation,
    )
    if result is None:
        return ResolutionCertificate(
            "BUDGET_OBSTRUCTION",
            f"No permitted sample size up to {max_sample_size} reaches TV >= {tau} for the declared margin.",
        )

    return ResolutionCertificate(
        "FINITELY_RESOLVABLE",
        "A positive decision margin removes the zero-margin obstruction.",
        sample_size=result.sample_size,
        cost=result.cost,
        tv_distance=result.tv_distance,
    )
