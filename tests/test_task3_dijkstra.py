"""Завдання 3 — Дейкстра: звірка з networkx, відновлення шляхів, недосяжність."""

import networkx as nx


def test_distances_match_networkx(t3):
    graph = t3.build_graph()
    start = "Київ"
    distances, _ = t3.dijkstra(graph, start)
    expected = nx.single_source_dijkstra_path_length(graph, start)
    assert distances == expected


def test_path_reconstruction_is_consistent(t3):
    graph = t3.build_graph()
    start = "Київ"
    distances, previous = t3.dijkstra(graph, start)
    for city in graph:
        path = t3.reconstruct_path(previous, start, city)
        assert path[0] == start
        assert path[-1] == city
        # сума ваг уздовж відновленого шляху дорівнює знайденій відстані
        total = sum(graph[u][v]["weight"] for u, v in zip(path, path[1:]))
        assert total == distances[city]


def test_start_path_is_trivial(t3):
    graph = t3.build_graph()
    _, previous = t3.dijkstra(graph, "Київ")
    assert t3.reconstruct_path(previous, "Київ", "Київ") == ["Київ"]


def test_unreachable_node(t3):
    graph = t3.build_graph()
    graph.add_node("Острів")          # ізольована вершина без ребер
    distances, previous = t3.dijkstra(graph, "Київ")
    assert distances["Острів"] == float("inf")
    assert t3.reconstruct_path(previous, "Київ", "Острів") == []
