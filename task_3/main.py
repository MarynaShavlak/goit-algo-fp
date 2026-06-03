"""
goit-algo-fp / Завдання 3 — Алгоритм Дейкстри на бінарній купі.

Зважений граф доріг між містами України. Алгоритм Дейкстри знаходить найкоротші
відстані від початкового міста до всіх інших, використовуючи бінарну мін-купу
(`heapq`) для вибору наступної вершини. Додатково відновлюються самі маршрути.
Візуалізація графа — у пакеті `viz` (`viz/dijkstra_graph.py`).
"""

import argparse
import heapq
from collections.abc import Hashable
from pathlib import Path

import networkx as nx

from viz.dijkstra_graph import draw_graph


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


def dijkstra(graph: nx.Graph, start: Hashable) -> tuple[dict, dict]:
    """Алгоритм Дейкстри на бінарній мін-купі (`heapq`).

    Наступну вершину завжди беремо з купи — ту, до якої відома найменша відстань.

    Повертає (distances, previous):
      * distances[v] — найкоротша відстань від start до v;
      * previous[v]  — попередня вершина на найкоротшому шляху (для відновлення).
    """
    distances = {v: float("inf") for v in graph}
    previous: dict[Hashable, Hashable | None] = {v: None for v in graph}
    distances[start] = 0

    heap: list[tuple[float, Hashable]] = [(0, start)]   # (відстань, вершина)
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


def dijkstra_steps(graph: nx.Graph, start: Hashable) -> list[tuple]:
    """Інструментована Дейкстра: знімок стану після закриття кожної вершини.

    Повертає список кортежів (settled, distances, previous, visited) — по одному
    на кожну вершину, вийняту з купи з остаточною відстанню (застарілі записи
    пропущено). Потрібна лише для покрокової анімації; основний результат дає
    `dijkstra`.
    """
    distances = {v: float("inf") for v in graph}
    previous: dict[Hashable, Hashable | None] = {v: None for v in graph}
    distances[start] = 0
    heap: list[tuple[float, Hashable]] = [(0, start)]
    visited: set[Hashable] = set()
    steps: list[tuple] = []
    while heap:
        current_distance, u = heapq.heappop(heap)
        if current_distance > distances[u]:
            continue
        visited.add(u)
        for v in graph.neighbors(u):
            new_distance = current_distance + graph[u][v]["weight"]
            if new_distance < distances[v]:
                distances[v] = new_distance
                previous[v] = u
                heapq.heappush(heap, (new_distance, v))
        steps.append((u, dict(distances), dict(previous), set(visited)))
    return steps


def reconstruct_path(previous: dict, start: Hashable, target: Hashable) -> list:
    """Відновлює найкоротший шлях start -> target за словником previous."""
    path: list = []
    node: Hashable | None = target
    while node is not None:
        path.append(node)
        if node == start:
            break
        node = previous[node]
    path.reverse()
    return path if path and path[0] == start else []   # [] якщо ціль недосяжна


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Алгоритм Дейкстри + візуалізація.")
    parser.add_argument(
        "--save", nargs="?", const="", metavar="PATH",
        help="зберегти граф у PNG (без значення — у dijkstra.png поруч зі скриптом)",
    )
    parser.add_argument(
        "--animate", action="store_true",
        help="зберегти покрокову GIF-анімацію фронтиру (dijkstra.gif)",
    )
    args = parser.parse_args()

    G = build_graph()
    start = "Київ"

    distances, previous = dijkstra(G, start)

    print(f"Найкоротші відстані від міста {start}:\n")
    for city in sorted(distances, key=lambda c: distances[c]):
        dist = distances[city]
        if dist == float("inf"):                        # недосяжна вершина
            print(f"  {city:<10} {'∞':>4} км   (недосяжно)")
            continue
        route = " -> ".join(reconstruct_path(previous, start, city))
        print(f"  {city:<10} {int(dist):>4} км   ({route})")

    title = f"Алгоритм Дейкстри: найкоротші шляхи від міста {start}"
    if args.animate:
        from viz.dijkstra_graph import animate_dijkstra
        out = Path(__file__).parent / "dijkstra.gif"
        animate_dijkstra(G, start, dijkstra_steps(G, start), title=title, save_path=str(out))
        print(f"\nАнімацію збережено: {out}")
    elif args.save is not None:
        out = args.save or (Path(__file__).parent / "dijkstra.png")
        draw_graph(G, start, distances, previous, title=title, save_path=str(out))
        print(f"\nГраф збережено: {out}")
    else:
        draw_graph(G, start, distances, previous, title=title)
