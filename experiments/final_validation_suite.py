# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Final validation protocol for evidence-induced decision resolution.

This file freezes the experiments required before manuscript drafting.
It deliberately separates statistical world construction from planning.
"""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Gate:
    name: str
    requirement: str


GATES: Sequence[Gate] = (
    Gate("coverage", "Empirically verify nominal coverage of evidence-induced compatible sets."),
    Gate("decision", "Verify that a decision is returned only when every admissible world agrees."),
    Gate("cost", "Compare total decision-resolution cost under unequal experiment costs."),
    Gate("target-aware-baseline", "Compare against a DRD/ECD-style target-aware planner, not only information gain."),
    Gate("noise", "Repeat with noisy experiment outcomes and report decision error and abstention."),
    Gate("obstruction", "Verify finite-budget and continuous-boundary obstruction certificates."),
    Gate("real-ml", "Run one real classifier deployment-threshold example with subgroup/test-set acquisition costs."),
)


def print_protocol() -> None:
    print("FINAL PAPER GATE")
    for i, gate in enumerate(GATES, 1):
        print(f"{i}. {gate.name}: {gate.requirement}")
    print("\nWrite the paper only after every gate has an executable result artifact.")


if __name__ == "__main__":
    print_protocol()
