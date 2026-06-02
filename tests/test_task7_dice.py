"""Завдання 7 — Монте-Карло: симетрія ways, аналітика, збіжність симуляції."""

import random

import pytest


def test_ways_symmetry(t7):
    assert t7.ways(7) == 6
    assert sum(t7.ways(s) for s in range(2, 13)) == 36
    for s in range(2, 13):
        assert t7.ways(s) == t7.ways(14 - s)        # симетрія відносно 7


def test_analytical_probabilities(t7):
    exact = t7.analytical_probabilities()
    assert set(exact) == set(range(2, 13))
    assert abs(sum(exact.values()) - 100) < 1e-9
    for s in range(2, 13):
        assert exact[s] == pytest.approx(t7.ways(s) / 36 * 100)


def test_monte_carlo_distribution(t7):
    random.seed(0)
    mc = t7.monte_carlo_dice(10_000)
    assert set(mc) == set(range(2, 13))
    assert sum(mc.values()) == pytest.approx(100)


def test_monte_carlo_converges_to_analytical(t7):
    random.seed(42)
    exact = t7.analytical_probabilities()
    mc = t7.monte_carlo_dice(200_000)
    assert t7.max_deviation(mc, exact) < 1.0        # у межах 1 в.п. на великій вибірці


def test_monte_carlo_invalid_rolls(t7):
    with pytest.raises(ValueError):
        t7.monte_carlo_dice(0)
    with pytest.raises(ValueError):
        t7.monte_carlo_dice(-5)


def test_max_deviation_zero_for_identical(t7):
    exact = t7.analytical_probabilities()
    assert t7.max_deviation(dict(exact), exact) == 0.0
