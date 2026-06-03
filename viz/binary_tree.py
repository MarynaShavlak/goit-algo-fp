"""Вузол і малювання бінарного дерева — спільні для task_4 і task_5.

`Node` — вузол дерева з атрибутами для візуалізації (`color`, унікальний `id`).
`draw_tree` будує розкладку за рівнями й малює дерево, розфарбовуючи вузли за їх
атрибутом `color`. Алгоритми (побудова купи у task_4, обходи DFS/BFS у task_5)
лежать у відповідних `main.py` і лише оперують цими вузлами.
"""

import uuid

import matplotlib.pyplot as plt
import networkx as nx

from .anim import save_gif


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, key, color: str = "skyblue"):
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key
        self.color = color           # колір вузла
        self.id = str(uuid.uuid4())  # унікальний ідентифікатор для графа


def _hex_or_name_to_rgb(color: str):
    """Повертає (r, g, b) для HEX-кольору або кількох іменованих кольорів."""
    named = {"skyblue": (135, 206, 235), "white": (255, 255, 255), "black": (0, 0, 0)}
    if color in named:
        return named[color]
    h = color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def add_edges(graph, node, pos, x=0.0, y=0.0, layer=1):
    """Рекурсивно додає вузли/ребра та обчислює координати для розкладки."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left is not None:
            graph.add_edge(node.id, node.left.id)
            lx = x - 1 / 2 ** layer
            pos[node.left.id] = (lx, y - 1)
            add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)
        if node.right is not None:
            graph.add_edge(node.id, node.right.id)
            rx = x + 1 / 2 ** layer
            pos[node.right.id] = (rx, y - 1)
            add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root: Node | None,
              title: str | None = None,
              save_path: str | None = None):
    """Малює бінарне дерево, розфарбовуючи вузли за їх атрибутом `color`.

    Якщо передано `save_path` — зберігає зображення у файл, інакше показує вікно.
    Підписи отримують адаптивний колір (білий на темному фоні, чорний на світлому).
    """
    if tree_root is None:
        return

    if save_path:
        plt.switch_backend("Agg")    # рендер у файл без графічного середовища

    tree = nx.DiGraph()
    pos = {tree_root.id: (0.0, 0.0)}
    add_edges(tree, tree_root, pos)

    node_colors = [data["color"] for _, data in tree.nodes(data=True)]

    plt.figure(figsize=(9, 6))
    if title:
        plt.title(title, fontsize=14)

    nx.draw(tree, pos=pos, arrows=False, node_size=2500, node_color=node_colors)

    for node_id, data in tree.nodes(data=True):
        r, g, b = _hex_or_name_to_rgb(data["color"])
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        font_color = "black" if luminance > 140 else "white"
        nx.draw_networkx_labels(
            tree, pos, labels={node_id: data["label"]},
            font_color=font_color, font_weight="bold",
        )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=130)
        plt.close()
    else:
        plt.show()


def animate_traversal(tree_root: Node, order: list, title: str | None = None,
                      save_path: str = "traversal.gif") -> None:
    """Покрокова GIF-анімація обходу дерева.

    `order` — вузли в порядку відвідування (з `task_5.dfs`/`bfs`), уже
    розфарбовані фінальним градієнтом. На кадрі i перші i+1 вузлів показані своїм
    кольором, решта — сірі. Сам обхід лишається в `task_5`.
    """
    tree = nx.DiGraph()
    pos: dict = {tree_root.id: (0.0, 0.0)}
    add_edges(tree, tree_root, pos)
    node_ids = list(tree.nodes())
    labels = {nid: data["label"] for nid, data in tree.nodes(data=True)}
    rank = {node.id: i for i, node in enumerate(order)}
    final_color = {node.id: node.color for node in order}

    def draw_frame(ax, i: int) -> None:
        colors = [
            final_color[nid] if rank.get(nid, len(order)) <= i else "#DDDDDD"
            for nid in node_ids
        ]
        nx.draw(tree, pos=pos, ax=ax, arrows=False, node_size=2200, node_color=colors)
        nx.draw_networkx_labels(tree, pos, ax=ax, labels=labels,
                                font_size=9, font_weight="bold")
        ax.set_title(f"{title or 'Обхід'} — крок {i + 1}/{len(order)}: "
                     f"вузол {order[i].val}", fontsize=12)
        ax.set_axis_off()

    save_gif(draw_frame, len(order), save_path, figsize=(8.0, 6.0), duration=800)
