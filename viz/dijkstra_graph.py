"""Малювання зваженого графа з деревом найкоротших шляхів — task_3.

`draw_graph` отримує граф і результат Дейкстри (`distances`, `previous`) і
підсвічує дерево найкоротших шляхів від стартової вершини. Сам алгоритм — у
`task_3/main.py`.
"""

from collections.abc import Hashable

import matplotlib.pyplot as plt
import networkx as nx

from .anim import save_gif

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


def draw_graph(graph: nx.Graph,
               start: Hashable,
               distances: dict,
               previous: dict,
               title: str | None = None,
               save_path: str | None = None):
    """Малює граф і ВИДІЛЯЄ дерево найкоротших шляхів від `start`.

    Звичайні дороги — сірі; ребра дерева найкоротших шляхів — помаранчеві й
    товсті. Підпис кожного міста містить назву та відстань від start.
    Якщо передано `save_path` — зберігає PNG (без дисплея), інакше показує вікно.
    """
    if save_path:
        plt.switch_backend("Agg")    # рендер у файл без графічного середовища

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


def animate_dijkstra(graph: nx.Graph, start: Hashable, steps: list,
                     title: str | None = None,
                     save_path: str = "dijkstra.gif") -> None:
    """Покрокова GIF-анімація фронтиру Дейкстри.

    `steps` — знімки (settled, distances, previous, visited) із
    `task_3.dijkstra_steps`: по кадру на кожну закриту вершину. Червона — щойно
    закрита, помаранчеві — закриті раніше, сині — ще ні; помаранчеві ребра —
    дерево найкоротших шляхів, що росте.
    """
    pos = {c: CITY_POS[c] for c in graph} if set(graph).issubset(CITY_POS) \
        else nx.spring_layout(graph, seed=42)
    edge_labels = nx.get_edge_attributes(graph, "weight")

    def draw_frame(ax, i: int) -> None:
        settled, distances, previous, visited = steps[i]
        tree_set = {frozenset((previous[v], v)) for v in graph if previous[v] is not None}
        tree_edges = [e for e in graph.edges if frozenset(e) in tree_set]
        other_edges = [e for e in graph.edges if frozenset(e) not in tree_set]
        colors = [
            "#E03131" if v == settled else "#E8590C" if v in visited else "#1296F0"
            for v in graph
        ]
        nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=2000, node_color=colors)
        nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=other_edges,
                               edge_color="#C9CDD4", width=1.5)
        nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=tree_edges,
                               edge_color="#E8590C", width=3.0)
        node_labels = {
            v: (f"{v}\n{int(distances[v])}" if distances[v] != float("inf")
                else f"{v}\n∞")
            for v in graph
        }
        nx.draw_networkx_labels(graph, pos, ax=ax, labels=node_labels,
                                font_size=7, font_color="white", font_weight="bold")
        nx.draw_networkx_edge_labels(graph, pos, ax=ax, edge_labels=edge_labels,
                                     font_size=7)
        ax.set_title(f"{title or 'Дейкстра'} — крок {i + 1}/{len(steps)}: "
                     f"закрито {settled}", fontsize=12)
        ax.set_axis_off()

    save_gif(draw_frame, len(steps), save_path, figsize=(11.0, 7.0), duration=1000)
