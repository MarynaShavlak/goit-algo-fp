"""Завдання 1 — однозв'язний список: reverse, insertion_sort, merge_sorted_ll."""

import pytest


def build(t1, values):
    ll = t1.LinkedList()
    for v in values:
        ll.insert_at_end(v)
    return ll


def test_reverse(t1):
    ll = build(t1, [1, 2, 3, 4])
    ll.reverse()
    assert ll.to_list() == [4, 3, 2, 1]


def test_reverse_empty_and_single(t1):
    empty = build(t1, [])
    empty.reverse()
    assert empty.to_list() == []

    single = build(t1, [7])
    single.reverse()
    assert single.to_list() == [7]


def test_insertion_sort(t1):
    values = [5, 15, 10, 35, 25, 25, 1]
    ll = build(t1, values)
    ll.insertion_sort()
    assert ll.to_list() == sorted(values)


def test_insertion_sort_empty(t1):
    empty = build(t1, [])
    empty.insertion_sort()
    assert empty.to_list() == []


def test_merge_sorted(t1):
    a_vals, b_vals = [1, 3, 4, 9], [0, 2, 2, 8, 10]
    a, b = build(t1, a_vals), build(t1, b_vals)
    merged = t1.merge_sorted_ll(a, b)
    assert merged.to_list() == sorted(a_vals + b_vals)
    # merge копіює значення, тож вихідні списки не змінюються
    assert a.to_list() == a_vals
    assert b.to_list() == b_vals


def test_merge_with_empty(t1):
    a = build(t1, [1, 2, 3])
    assert t1.merge_sorted_ll(a, build(t1, [])).to_list() == [1, 2, 3]
    assert t1.merge_sorted_ll(build(t1, []), a).to_list() == [1, 2, 3]
    assert t1.merge_sorted_ll(build(t1, []), build(t1, [])).to_list() == []


def test_search_and_delete(t1):
    ll = build(t1, [1, 2, 3])
    assert ll.search_element(2).data == 2
    assert ll.search_element(99) is None
    ll.delete_node(2)
    assert ll.to_list() == [1, 3]


def test_insert_after_none_raises(t1):
    ll = build(t1, [1])
    with pytest.raises(ValueError):
        ll.insert_after(None, 99)
