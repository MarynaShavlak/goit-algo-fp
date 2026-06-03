"""Property-based перевірки (hypothesis) поверх прикладних тестів.

Інваріанти для БУДЬ-ЯКИХ входів: сортування дає відсортований список, злиття
зберігає порядок, ДП не гірше за жадібний і збігається з 1D-варіантом за
значенням, а Дейкстра дає ті самі відстані, що й networkx.
"""

import networkx as nx
from hypothesis import given
from hypothesis import strategies as st

_ints = st.lists(st.integers())
_items = st.dictionaries(
    keys=st.text("abcdefgh", min_size=1, max_size=4),
    values=st.fixed_dictionaries(
        {"cost": st.integers(1, 30), "calories": st.integers(1, 100)}
    ),
    max_size=6,
)


@given(values=_ints)
def test_insertion_sort_matches_builtin(t1, values):
    ll = t1.LinkedList()
    for v in values:
        ll.insert_at_end(v)
    ll.insertion_sort()
    assert ll.to_list() == sorted(values)


@given(values=_ints)
def test_merge_sort_matches_builtin(t1, values):
    ll = t1.LinkedList()
    for v in values:
        ll.insert_at_end(v)
    ll.merge_sort()
    assert ll.to_list() == sorted(values)


@given(a=_ints, b=_ints)
def test_merge_sorted_ll_matches_builtin(t1, a, b):
    la, lb = t1.LinkedList(), t1.LinkedList()
    for v in sorted(a):
        la.insert_at_end(v)
    for v in sorted(b):
        lb.insert_at_end(v)
    assert t1.merge_sorted_ll(la, lb).to_list() == sorted(a + b)


@given(items=_items, budget=st.integers(0, 60))
def test_dp_optimal_and_one_row_agree(t6, items, budget):
    dp_set = t6.dynamic_programming(items, budget)
    dp_cost = sum(items[n]["cost"] for n in dp_set)
    dp_cal = sum(items[n]["calories"] for n in dp_set)
    greedy_cal = sum(items[n]["calories"] for n in t6.greedy_algorithm(items, budget))

    assert dp_cost <= budget  # набір не перевищує бюджет
    assert dp_cal >= greedy_cal  # ДП не гірше за жадібний
    assert t6.dynamic_programming_value(items, budget) == dp_cal  # 1D == 2D


@given(data=st.data())
def test_dijkstra_matches_networkx(t3, data):
    n = data.draw(st.integers(2, 6))
    edges = data.draw(
        st.lists(
            st.tuples(st.integers(0, n - 1), st.integers(0, n - 1), st.integers(1, 20)),
            max_size=15,
        )
    )
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for u, v, w in edges:
        if u != v:
            graph.add_edge(u, v, weight=w)

    distances, _ = t3.dijkstra(graph, 0)
    reference = nx.single_source_dijkstra_path_length(graph, 0)
    for node in graph:
        assert distances[node] == reference.get(node, float("inf"))
