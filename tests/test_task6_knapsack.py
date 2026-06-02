"""Завдання 6 — рюкзак 0/1: оптимальність ДП проти брутфорсу, коректність жадібного."""

import itertools

import pytest

ITEMS = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def brute_force_best(items, budget):
    """Максимальна калорійність будь-якого допустимого набору (повний перебір)."""
    names = list(items)
    best = 0
    for r in range(len(names) + 1):
        for combo in itertools.combinations(names, r):
            cost = sum(items[n]["cost"] for n in combo)
            if cost <= budget:
                best = max(best, sum(items[n]["calories"] for n in combo))
    return best


def calories(names):
    return sum(ITEMS[n]["calories"] for n in names)


def cost(names):
    return sum(ITEMS[n]["cost"] for n in names)


@pytest.mark.parametrize("budget", [0, 10, 25, 40, 55, 75, 100, 140, 200])
def test_dp_is_optimal_and_feasible(t6, budget):
    chosen = t6.dynamic_programming(ITEMS, budget)
    assert cost(chosen) <= budget                     # допустимий набір
    assert len(chosen) == len(set(chosen))            # без дублів (0/1)
    assert calories(chosen) == brute_force_best(ITEMS, budget)  # оптимум


@pytest.mark.parametrize("budget", [0, 10, 25, 50, 100])
def test_greedy_feasible_and_not_above_optimum(t6, budget):
    chosen = t6.greedy_algorithm(ITEMS, budget)
    assert cost(chosen) <= budget
    assert len(chosen) == len(set(chosen))
    assert calories(chosen) <= brute_force_best(ITEMS, budget)


def test_negative_budget_raises(t6):
    with pytest.raises(ValueError):
        t6.dynamic_programming(ITEMS, -1)
    with pytest.raises(ValueError):
        t6.greedy_algorithm(ITEMS, -1)


def test_empty_items(t6):
    assert t6.dynamic_programming({}, 100) == []
    assert t6.greedy_algorithm({}, 100) == []
