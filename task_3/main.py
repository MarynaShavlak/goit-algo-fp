"""
goit-algo-fp / Завдання 3 — Алгоритм Дейкстри на бінарній купі.

Зважений граф доріг між містами України. Алгоритм Дейкстри знаходить найкоротші
відстані від початкового міста до всіх інших, використовуючи бінарну мін-купу
(`heapq`) для вибору наступної вершини. Додатково відновлюються самі маршрути.
"""

import heapq
from typing import Dict, Hashable, List, Optional, Tuple

import networkx as nx
import matplotlib.pyplot as plt

# Приблизна географічна розкладка міст (схід-захід / північ-південь),
# щоб граф нагадував карту України.
CITY_POS = {
    "Львів": (-3.4, 1.2),
    "Київ": (-0.3, 1.8),
    "Вінниця": (-1.9, 0.4),
    "Одеса": (-1.2, -2.6),
    "Полтава": (1.4, 1.4),
    "Харків": (3.2, 1.6),
    "Дніпро": (1.9, -0.4),
    "Запоріжжя": (2.6, -1.9),
}


def build_graph() -> nx.Graph:
    """Зважений граф доріг між містами України (відстані в км, приблизні)."""
    roads = [
        ("Київ", "Вінниця", 270),
        ("Київ", "Полтава", 340),
        ("Київ", "Одеса", 475),
        ("Київ", "Львів", 540),
        ("Вінниця", "Львів", 360),
        ("Вінниця", "Одеса", 430),
        ("Полтава", "Харків", 140),
        ("Полтава", "Дніпро", 190),
        ("Дніпро", "Запоріжжя", 85),
        ("Дніпро", "Харків", 215),
        ("Запоріжжя", "Харків", 290),
    ]
    graph = nx.Graph()
    for u, v, weight in roads:
        graph.add_edge(u, v, weight=weight)
    return graph


def dijkstra(graph: nx.Graph, start: Hashable) -> Tuple[Dict, Dict]:
    """Алгоритм Дейкстри на бінарній мін-купі (`heapq`).

    `heapq` підтримує саме бінарну купу, тож вибір вершини з найменшою відстанню
    коштує O(log V). Загальна складність — O((V + E) · log V).

    Повертає (distances, previous):
      * distances[v] — найкоротша відстань від start до v;
      * previous[v]  — попередня вершина на найкоротшому шляху (для відновлення).
    """
    distances = {v: float("inf") for v in graph}
    previous: Dict[Hashable, Optional[Hashable]] = {v: None for v in graph}
    distances[start] = 0

    heap: List[Tuple[float, Hashable]] = [(0, start)]   # (відстань, вершина)
    while heap:
        current_distance, u = heapq.heappop(heap)
        # Застарілий запис у купі — для цієї вершини вже знайдено коротший шлях.
        if current_distance > distances[u]:
            continue
        for v in graph.neighbors(u):
            new_distance = current_distance + graph[u][v]["weight"]
            if new_distance < distances[v]:
                distances[v] = new_distance
                previous[v] = u
                heapq.heappush(heap, (new_distance, v))

    return distances, previous


def reconstruct_path(previous: Dict, start: Hashable, target: Hashable) -> List:
    """Відновлює найкоротший шлях start -> target за словником previous."""
    path: List = []
    node: Optional[Hashable] = target
    while node is not None:
        path.append(node)
        if node == start:
            break
        node = previous[node]
    path.reverse()
    return path if path and path[0] == start else []   # [] якщо ціль недосяжна


def draw_graph(graph: nx.Graph,
               start: Hashable,
               distances: Dict,
               previous: Dict,
               title: Optional[str] = None,
               save_path: Optional[str] = None):
    """Малює граф і ВИДІЛЯЄ дерево найкоротших шляхів від `start`.

    Звичайні дороги — сірі; ребра дерева найкоротших шляхів — помаранчеві й
    товсті. Підпис кожного міста містить назву та відстань від start.
    """
    pos = {c: CITY_POS[c] for c in graph} if set(graph).issubset(CITY_POS) \
        else nx.spring_layout(graph, seed=42)

    # Ребра дерева найкоротших шляхів: (previous[v], v).
    tree_set = {frozenset((previous[v], v)) for v in graph if previous[v] is not None}
    tree_edges = [(u, v) for u, v in graph.edges if frozenset((u, v)) in tree_set]
    other_edges = [(u, v) for u, v in graph.edges if frozenset((u, v)) not in tree_set]

    plt.figure(figsize=(12, 8))
    if title:
        plt.title(title, fontsize=15)

    nx.draw_networkx_nodes(graph, pos, node_size=2200, node_color="#1296F0")
    nx.draw_networkx_nodes(graph, pos, nodelist=[start],
                           node_size=2600, node_color="#E8590C")

    nx.draw_networkx_edges(graph, pos, edgelist=other_edges,
                           edge_color="#C9CDD4", width=1.5)
    nx.draw_networkx_edges(graph, pos, edgelist=tree_edges,
                           edge_color="#E8590C", width=3.0)

    labels = {
        v: (f"{v}\n{int(distances[v])} км" if distances[v] != float("inf")
            else f"{v}\n∞")
        for v in graph
    }
    nx.draw_networkx_labels(graph, pos, labels=labels,
                            font_size=8, font_color="white", font_weight="bold")

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    plt.axis("off")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=130)
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    G = build_graph()
    start = "Київ"

    distances, previous = dijkstra(G, start)

    print(f"Найкоротші відстані від міста {start}:\n")
    for city in sorted(distances, key=distances.get):
        path = reconstruct_path(previous, start, city)
        route = " -> ".join(path)
        print(f"  {city:<10} {int(distances[city]):>4} км   ({route})")

    draw_graph(G, start, distances, previous,
               title=f"Алгоритм Дейкстри: найкоротші шляхи від міста {start}")
