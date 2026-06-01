"""
goit-algo-fp / Завдання 4 — Візуалізація бінарної купи.

Купа зберігається як масив. Для елемента з індексом i його діти — це елементи
з індексами 2*i + 1 (лівий) та 2*i + 2 (правий). За цим правилом будуємо
бінарне дерево з масиву й малюємо його через networkx.
"""

import uuid
from typing import List, Optional

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, key, color: str = "skyblue"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
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


def draw_tree(tree_root: Node,
              title: Optional[str] = None,
              save_path: Optional[str] = None):
    """Малює бінарне дерево, розфарбовуючи вузли за їх атрибутом `color`.

    Якщо передано `save_path` — зберігає зображення у файл, інакше показує вікно.
    Підписи отримують адаптивний колір (білий на темному фоні, чорний на світлому).
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


def build_heap_tree(heap: List[int], i: int = 0) -> Optional[Node]:
    """Будує бінарне дерево з масиву-купи.

    Для елемента з індексом i його діти — 2*i + 1 (лівий) та 2*i + 2 (правий).
    Кожен виклик створює власний вузол і повертає його; за межами масиву —
    повертає None. Повертає корінь дерева (або None для порожньої купи).
    """
    if i >= len(heap):
        return None
    node = Node(heap[i])
    node.left = build_heap_tree(heap, 2 * i + 1)
    node.right = build_heap_tree(heap, 2 * i + 2)
    return node


if __name__ == "__main__":
    import heapq

    # 1) Будуємо МІН-купу з довільних чисел і візуалізуємо дерево з неї.
    data = [10, 5, 3, 4, 1, 8, 7, 2]
    heapq.heapify(data)            # тепер data — валідна бінарна min-купа
    print("Min-heap:", data)
    draw_tree(build_heap_tree(data), title="Бінарна min-купа")

    # 2) Готова max-купа (як у прикладі завдання).
    max_heap = [10, 5, 3, 4, 1]
    print("Max-heap:", max_heap)
    draw_tree(build_heap_tree(max_heap), title="Бінарна max-купа")
