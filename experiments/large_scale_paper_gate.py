# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0

"""Large-scale reproducible paper-gate simulation.

Purpose
-------
Stress-test the full evidence -> admissible worlds -> decision disagreement ->
experiment/obstruction chain over many finite-evidence states.

This benchmark deliberately includes:
* finite Binomial evidence;
* a deployment threshold;
* heterogeneous experiment costs;
* noisy future measurements;
* a target-blind information/cost baseline;
* an oracle target-aware one-step comparator;
* explicit abstention/obstruction accounting.

The oracle is NOT presented as a new baseline or as DRD/ECD itself. It is a
sanity ceiling: if the proposed one-step planner cannot match the cheapest
one-step target-resolving experiment on its own finite candidate catalogue,
the paper gate fails before comparison with stronger sequential methods.
"""

from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path

from underdetermination.core import compatible_worlds
from underdetermination.planner import CandidateExperiment, cheapest_decisive_experiment


SEED = 20260915
ALPHA = 0.05
THRESHOLD = 0.80
MIN_TV = 0.10
GRID = [i / 100 for i in range(1, 100)]
REPLICATES = 2000


@dataclass(frozen=True)
class CatalogueItem:
    name: str
    cost: float
    sensitivity: float


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))


def law(theta: float, sensitivity: float):
    p = 0.5 + sensitivity * (theta - 0.5)
    return {1: p, 0: 1.0 - p}


def catalogue_for(rep: int):
    # Deterministic heterogeneous catalogue generated from replicate id.
    r = random.Random(SEED + 7919 * rep)
    items = []
    for j in range(8):
        items.append(
            CatalogueItem(
                name=f"E{j}",
                cost=round(r.uniform(0.5, 8.0), 3),
                sensitivity=round(r.uniform(0.15, 1.0), 3),
            )
        )
    return items


def world_information_gain(worlds, item: CatalogueItem) -> float:
    # Uniform prior over currently admissible grid worlds. For a binary channel,
    # I(W;Y)=H(E[p])-E[H(p)]. This is intentionally target-blind.
    ps = [0.5 + item.sensitivity * (t - 0.5) for t in worlds]
    mean_p = sum(ps) / len(ps)
    return binary_entropy(mean_p) - sum(binary_entropy(p) for p in ps) / len(ps)


def target_blind_choice(worlds, items):
    scored = []
    for item in items:
        score = world_information_gain(worlds, item) / item.cost
        scored.append((score, -item.cost, item.name, item))
    return max(scored)[-1]


def sample_binomial(rng, n, p):
    return sum(rng.random() < p for _ in range(n))


def main():
    rng = random.Random(SEED)
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "large_scale_paper_gate.csv"

    theta_values = [0.65, 0.70, 0.75, 0.78, 0.79, 0.80, 0.81, 0.82, 0.85, 0.90, 0.95]
    n_values = [20, 50, 100]

    rows = []
    rep = 0
    for theta_true in theta_values:
        for n in n_values:
            for _ in range(REPLICATES):
                rep += 1
                successes = sample_binomial(rng, n, theta_true)
                worlds_obj = compatible_worlds(successes, n, GRID, ALPHA)
                worlds = [w.theta for w in worlds_obj]
                if not worlds:
                    continue

                true_covered = min(worlds) <= theta_true <= max(worlds)
                labels = {t >= THRESHOLD for t in worlds}
                resolved = len(labels) == 1
                implied = next(iter(labels)) if resolved else None
                true_label = theta_true >= THRESHOLD
                wrong_resolved = bool(resolved and implied != true_label)

                items = catalogue_for(rep)
                exps = [
                    CandidateExperiment(
                        x.name,
                        x.cost,
                        {t: law(t, x.sensitivity) for t in worlds},
                    )
                    for x in items
                ]

                if resolved:
                    proposed_status = "RESOLVED"
                    proposed_name = ""
                    proposed_cost = 0.0
                    blind = target_blind_choice(worlds, items)
                    blind_name, blind_cost = blind.name, blind.cost
                else:
                    plan = cheapest_decisive_experiment(
                        worlds,
                        lambda t: t >= THRESHOLD,
                        exps,
                        min_tv=MIN_TV,
                    )
                    proposed_status = plan.status
                    proposed_name = plan.experiment or ""
                    proposed_cost = plan.cost if plan.cost is not None else math.nan
                    blind = target_blind_choice(worlds, items)
                    blind_name, blind_cost = blind.name, blind.cost

                rows.append(
                    {
                        "theta_true": theta_true,
                        "n": n,
                        "successes": successes,
                        "compatible_low": min(worlds),
                        "compatible_high": max(worlds),
                        "true_covered": int(true_covered),
                        "resolved": int(resolved),
                        "wrong_resolved": int(wrong_resolved),
                        "proposed_status": proposed_status,
                        "proposed_experiment": proposed_name,
                        "proposed_cost": proposed_cost,
                        "target_blind_experiment": blind_name,
                        "target_blind_cost": blind_cost,
                    }
                )

    fields = list(rows[0])
    with out_file.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    coverage = sum(r["true_covered"] for r in rows) / total
    wrong = sum(r["wrong_resolved"] for r in rows) / total
    unresolved = sum(not r["resolved"] for r in rows) / total
    obstruction = sum(r["proposed_status"] == "OBSTRUCTION" for r in rows) / total

    print(f"rows={total}")
    print(f"empirical compatible-set coverage={coverage:.6f}")
    print(f"wrong resolved decision rate={wrong:.6f}")
    print(f"initial unresolved fraction={unresolved:.6f}")
    print(f"one-step obstruction fraction={obstruction:.6f}")
    print(f"wrote {out_file}")


if __name__ == "__main__":
    main()
