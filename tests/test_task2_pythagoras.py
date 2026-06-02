"""Завдання 2 — дерево Піфагора: геометрія відрізків і парсинг рівня."""

import pytest


def test_empty_levels(t2):
    # order 0 — порожньо; від'ємний рівень НЕ йде в нескінченну рекурсію (фікс #1)
    assert t2.pythagoras_segments(0, 1.0) == []
    assert t2.pythagoras_segments(-3, 1.0) == []


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_segment_count_is_full_binary_tree(t2, n):
    # на рівні n гілок: 1 + 2 + ... + 2^(n-1) = 2^n - 1
    assert len(t2.pythagoras_segments(n, 1.0)) == 2 ** n - 1


def test_segment_shape_and_root_order(t2):
    segments = t2.pythagoras_segments(4, 1.0)
    assert all(len(s) == 5 for s in segments)       # (x0, y0, x1, y1, order)
    assert segments[0][4] == 4                       # перший відрізок — корінь
    assert max(s[4] for s in segments) == 4
    assert min(s[4] for s in segments) == 1


def test_parse_input(t2):
    assert t2.parse_input("5") == 5
    assert t2.parse_input("0") == 0
    with pytest.raises(ValueError):
        t2.parse_input("-1")
    with pytest.raises(ValueError):
        t2.parse_input("abc")
