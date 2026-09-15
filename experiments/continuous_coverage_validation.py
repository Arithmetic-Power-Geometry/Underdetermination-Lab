# Copyright (C) 2026 Mohammad Amir Khusru Akhtar
# Licensed under the Apache License, Version 2.0.

"""Continuous-point coverage validation for the evidence-admission layer.

This deliberately does not ask whether the true parameter lies on the repository's
0.01 theta grid. For each continuous Bernoulli parameter p, coverage is computed
exactly by summing P_p(K=k) over all observations k for which inversion of the
same exact two-sided binomial test admits p.

Thus
    C_alpha(k,n) = {p : pvalue(k;n,p) >= alpha}
and
    Coverage(p,n) = sum_k P_p(K=k) 1[p in C_alpha(k,n)].

The calculation is deterministic apart from floating-point arithmetic.
"""

from underdetermination.core import binom_pmf, two_sided_exact_pvalue

ALPHA = 0.05
N_VALUES = (10, 20, 50, 100, 200)
# Off-grid as well as boundary-near values. None of the special values below is
# required to coincide with the manuscript's 0.01 admissible-world grid.
P_VALUES = tuple(i / 1000.0 for i in range(1, 1000))


def exact_coverage(p: float, n: int, alpha: float = ALPHA) -> float:
    return sum(
        binom_pmf(k, n, p)
        for k in range(n + 1)
        if two_sided_exact_pvalue(k, n, p) >= alpha
    )


def run() -> None:
    target = 1.0 - ALPHA
    global_min = (1.0, None, None)
    print("continuous exact-test inversion coverage validation")
    print(f"alpha={ALPHA:.3f}; nominal coverage={target:.3f}")
    print("n,min_coverage,p_at_min,coverage_at_0.799,coverage_at_0.801")

    for n in N_VALUES:
        vals = [(p, exact_coverage(p, n)) for p in P_VALUES]
        p_min, cov_min = min(vals, key=lambda x: x[1])
        c_lo = exact_coverage(0.799, n)
        c_hi = exact_coverage(0.801, n)
        print(f"{n},{cov_min:.9f},{p_min:.3f},{c_lo:.9f},{c_hi:.9f}")
        if cov_min < global_min[0]:
            global_min = (cov_min, p_min, n)

    cov, p, n = global_min
    print(f"global_min_coverage={cov:.9f} at p={p:.3f}, n={n}")
    # Exact discrete tests are generally conservative. Numerical tolerance is
    # only for floating-point summation/comparison.
    if cov < target - 1e-10:
        raise AssertionError(
            f"coverage gate failed: {cov:.12f} < nominal {target:.12f}"
        )
    print("COVERAGE_GATE=PASS")


if __name__ == "__main__":
    run()
