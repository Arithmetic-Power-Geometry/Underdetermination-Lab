# ML Deployment Paper Gate

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
Licensed under the Apache License, Version 2.0.

## Purpose

This is the final application-level gate for the research question:

> Find the cheapest experiment for which current knowledge leaves mutually incompatible possible worlds.

The controlled deployment benchmark represents a fixed classifier evaluated on three deployment subgroups. Initial finite validation evidence induces statistically admissible subgroup-accuracy worlds. Deployment is permitted only if every required subgroup accuracy is at least the pre-specified floor.

The experiment therefore does **not** ask which subgroup has the largest uncertainty or which measurement maximizes generic information. It asks which unresolved deployment-relevant evaluation can be purchased at minimum cost while satisfying the chosen resolution criterion.

## Pipeline

K -> C_alpha(K) -> deployment disagreement -> candidate subgroup evaluations -> cheapest certifying evaluation or obstruction.

The implementation is in `experiments/ml_deployment_case.py`.

## Important validity boundary

The finite-grid calculation and the continuous problem must not be conflated.

On a 0.01 parameter grid, the hardest opposite-decision pair can be searched and assigned a finite sample requirement. In a continuous parameter space with no positive margin around the deployment floor, parameters can approach the floor arbitrarily closely. Consequently, uniform finite fixed-size resolution at a positive discrimination threshold is obstructed.

A paper must therefore report the finite-grid result as a benchmark result, not as a continuous guarantee. Any finite continuous guarantee requires an explicit scientifically justified margin or another regularity condition.

## What this application establishes

If the benchmark behaves as designed, it demonstrates an end-to-end interface:

1. finite noisy evidence generates admissible worlds;
2. a downstream deployment target partitions those worlds;
3. disagreement triggers experiment planning rather than premature deployment;
4. heterogeneous acquisition costs are respected;
5. the output is either a cheapest certifying experiment or an explicit obstruction.

It does **not**, by itself, establish that subgroup validation, confidence intervals, cost-sensitive active learning, DRD/ECD, or experimental design are novel.

## Literature boundary

Existing ML validation work already emphasizes deployment thresholds, subgroup performance, uncertainty, and the cost or difficulty of obtaining additional labels. Existing active-learning and decision-region literature already studies cost-sensitive acquisition and target identification. Therefore the manuscript must frame novelty, if retained after the final literature attack, around the evidence-to-planning interface and its statistical admission/obstruction semantics rather than around those ingredients individually.

## Stop rule

After this application is executed and CI passes, do not add another theory merely to increase apparent novelty.

Perform one final targeted prior-art search for the exact composition:

finite-sample confidence/compatibility set -> downstream decision disagreement -> minimum-cost experiment -> certified abstention/obstruction.

If an exact prior formulation is found, narrow or stop. If no exact formulation is found and the benchmark plus DRD/ECD comparison remain valid, freeze the repository and begin the manuscript.
