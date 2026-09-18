#!/usr/bin/env python3
from __future__ import annotations
import math, sys
from pathlib import Path
import numpy as np

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))
from oracle import oracle
from verifier import build_K, build_U

def test_shift_periodicity():
    m, k, s = 5, 4, 7
    n = m * k
    assert np.array_equal(build_K(m, k, s), build_K(m, k, s + n))

def test_zero_remainder():
    m, k, s = 6, 3, 3
    r = oracle(m, k, s)
    assert r.r == 0 and r.alpha_squared == 0.0 and r.trace == 0.0 and r.norm == 0.0

def test_r_reflection():
    m, k = 6, 7
    a = oracle(m, k, 2)
    b = oracle(m, k, k - 2)
    assert math.isclose(a.alpha_squared, b.alpha_squared, rel_tol=1e-15, abs_tol=1e-15)
    assert math.isclose(a.trace, b.trace, rel_tol=1e-15, abs_tol=1e-15)
    assert math.isclose(a.norm, b.norm, rel_tol=1e-15, abs_tol=1e-15)

def test_U_columns_orthonormal():
    U = build_U(5, 4)
    assert np.allclose(U.T @ U, np.eye(5), atol=1e-12)

def main():
    for test in (test_shift_periodicity, test_zero_remainder,
                 test_r_reflection, test_U_columns_orthonormal):
        test()
        print(f"{test.__name__}=PASS")
    print("status=PASS")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""SV-001-V2 metamorphic tests."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

from oracle import oracle
from verifier import build_K, build_U


def test_shift_periodicity():
    m, k, s = 5, 4, 7
    n = m * k
    assert np.array_equal(build_K(m, k, s), build_K(m, k, s + n))


def test_zero_remainder():
    m, k, s = 6, 3, 3
    r = oracle(m, k, s)
    assert r.r == 0
    assert r.alpha_squared == 0.0
    assert r.trace == 0.0
    assert r.norm == 0.0


def test_r_reflection():
    m, k = 6, 7
    a = oracle(m, k, 2)
    b = oracle(m, k, k - 2)
    assert math.isclose(a.alpha_squared, b.alpha_squared, rel_tol=1e-15, abs_tol=1e-15)
    assert math.isclose(a.trace, b.trace, rel_tol=1e-15, abs_tol=1e-15)
    assert math.isclose(a.norm, b.norm, rel_tol=1e-15, abs_tol=1e-15)


def test_U_columns_orthonormal():
    U = build_U(5, 4)
    assert np.allclose(U.T @ U, np.eye(5), atol=1e-12)


def main():
    tests = (
        test_shift_periodicity,
        test_zero_remainder,
        test_r_reflection,
        test_U_columns_orthonormal,
    )
    for test in tests:
        test()
        print(f"{test.__name__}=PASS")
    print("status=PASS")


if __name__ == "__main__":
    main()
