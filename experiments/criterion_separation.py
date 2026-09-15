# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Constructive benchmark: information gain and cheapest decision resolution disagree.

Four current-evidence-compatible worlds carry two latent coordinates:
  z: nuisance identity within a decision side
  y: decision side (0/1)

Experiment A reveals z perfectly but says nothing about y.
Experiment B reveals y perfectly but says nothing about z.

With a uniform compatible-world distribution both experiments have identical mutual
information (1 bit). If A is made slightly richer by adding an independent nuisance
bit, A has strictly larger information gain while still zero decision-resolution
value. B remains the unique cheapest decisive experiment.
"""

from dataclasses import dataclass
from math import log2


@dataclass(frozen=True)
class Experiment:
    name: str
    cost: float
    # deterministic outcome for world (decision, nuisance1, nuisance2)
    observed_coordinates: tuple[int, ...]


WORLDS = [
    (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
    (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1),
]

A = Experiment("A_nuisance_information", 1.0, (1, 2))
B = Experiment("B_decision_resolver", 1.0, (0,))


def entropy(values):
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    n = len(values)
    return -sum((c/n) * log2(c/n) for c in counts.values())


def outcome(world, experiment):
    return tuple(world[i] for i in experiment.observed_coordinates)


def information_gain(experiment):
    # Deterministic observation under a uniform compatible-world distribution.
    return entropy([outcome(w, experiment) for w in WORLDS])


def resolves_decision(experiment):
    buckets = {}
    for w in WORLDS:
        buckets.setdefault(outcome(w, experiment), set()).add(w[0])
    return all(len(decisions) == 1 for decisions in buckets.values())


def cheapest_decision_resolver(experiments):
    feasible = [e for e in experiments if resolves_decision(e)]
    return min(feasible, key=lambda e: e.cost) if feasible else None


def main():
    experiments = [A, B]
    for e in experiments:
        print(e.name, "cost=", e.cost, "IG(bits)=", information_gain(e),
              "resolves_decision=", resolves_decision(e))
    ig_choice = max(experiments, key=information_gain)
    resolver = cheapest_decision_resolver(experiments)
    print("information_gain_choice=", ig_choice.name)
    print("cheapest_decision_resolver=", resolver.name if resolver else None)
    assert information_gain(A) == 2.0
    assert information_gain(B) == 1.0
    assert not resolves_decision(A)
    assert resolves_decision(B)
    assert ig_choice == A
    assert resolver == B


if __name__ == "__main__":
    main()
