"""Пакет viz — спільний lerp_color (база градієнтів task_2 і task_5)."""

from viz.colors import lerp_color


def test_endpoints():
    assert lerp_color((0, 0, 0), (10, 20, 30), 0.0) == (0, 0, 0)
    assert lerp_color((0, 0, 0), (10, 20, 30), 1.0) == (10, 20, 30)


def test_midpoint():
    assert lerp_color((0, 0, 0), (10, 10, 10), 0.5) == (5, 5, 5)


def test_works_on_float_scale():
    brown = (0.40, 0.26, 0.13)
    green = (0.13, 0.55, 0.13)
    assert lerp_color(brown, green, 0.0) == brown
    assert lerp_color(brown, green, 1.0) == green
