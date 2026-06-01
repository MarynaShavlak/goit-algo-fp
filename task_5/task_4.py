"""
Код для побудови та візуалізації бінарного дерева (із Завдання 4).

Містить клас `Node` і функцію `draw_tree`, які повторно використовуються у
Завданні 5 для візуалізації обходів. Розкладка дерева виконується через
networkx; рекурсія тут потрібна лише для ПОБУДОВИ КАРТИНКИ, а не для обходу.
"""

import uuid
from typing import Optional

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, key, color: str = "#CCCCCC"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color           # колір вузла у форматі HEX (#RRGGBB)
        self.id = str(uuid.uuid4())  # унікальний ідентифікатор для графа


def _hex_to_rgb(hex_color: str):
    """'#RRGGBB' -> (r, g, b)."""
    h = hex_color.lstrip("#")
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


def draw_tree(tree_root: Node,
              title: Optional[str] = None,
              save_path: Optional[str] = None):
    """Малює бінарне дерево, розфарбовуючи вузли за їх атрибутом `color`.

    Якщо передано `save_path` — зберігає зображення у файл, інакше показує вікно.
    Підписи вузлів отримують адаптивний колір (білий на темному фоні, чорний на
    світлому) — щоб числа залишалися читабельними на всьому градієнті.
    """
    if tree_root is None:
        return

    tree = nx.DiGraph()
    pos = {tree_root.id: (0.0, 0.0)}
    add_edges(tree, tree_root, pos)

    node_colors = [data["color"] for _, data in tree.nodes(data=True)]

    plt.figure(figsize=(9, 6))
    if title:
        plt.title(title, fontsize=14)

    nx.draw(tree, pos=pos, arrows=False, node_size=2500, node_color=node_colors)

    # Підписи з адаптивним кольором тексту залежно від яскравості вузла.
    for node_id, data in tree.nodes(data=True):
        r, g, b = _hex_to_rgb(data["color"])
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
