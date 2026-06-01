"""
goit-algo-fp / Завдання 5 — Візуалізація обходів бінарного дерева.

Обхід у глибину (DFS) та в ширину (BFS) виконуються ІТЕРАТИВНО — за допомогою
стека та черги (без рекурсії). Кожен вузол при відвідуванні отримує унікальний
колір; кольори йдуть градієнтом від ТЕМНИХ (відвідані раніше) до СВІТЛИХ
(відвідані пізніше).
"""

from collections import deque
from typing import List

from task_4 import Node, draw_tree


def generate_hex_color(step: int, total: int) -> str:
    """HEX-колір для кроку обходу: градієнт темно-синій -> світло-блакитний.

    step  — порядковий номер відвідування (0-based);
    total — загальна кількість вузлів.
    Перший відвіданий вузол — темний, останній — світлий; усі кольори унікальні.
    Діапазон спирається на РЕАЛЬНУ кількість вузлів, тож градієнт завжди
    розтягується на все дерево (а не на фіксовані 10).
    """
    t = 0.0 if total <= 1 else step / (total - 1)   # 0 -> темний, 1 -> світлий
    dark = (8, 48, 107)      # #08306B — темно-синій
    light = (222, 235, 247)  # #DEEBF7 — світло-блакитний
    r = round(dark[0] + (light[0] - dark[0]) * t)
    g = round(dark[1] + (light[1] - dark[1]) * t)
    b = round(dark[2] + (light[2] - dark[2]) * t)
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def _color_in_order(order: List[Node]) -> None:
    """Розфарбовує вузли у порядку їх відвідування."""
    total = len(order)
    for i, node in enumerate(order):
        node.color = generate_hex_color(i, total)


def dfs(root: Node) -> List[Node]:
    """Обхід у глибину (pre-order) за допомогою СТЕКА, без рекурсії.

    У дереві немає циклів, тож множина `visited` не потрібна. Праву дитину
    кладемо у стек ПЕРШОЮ, щоб ліва оброблялася раніше (порядок корінь→ліво→право).
    Повертає список вузлів у порядку відвідування.
    """
    if root is None:
        return []

    order: List[Node] = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)

    _color_in_order(order)
    return order


def bfs(root: Node) -> List[Node]:
    """Обхід у ширину (level-order) за допомогою ЧЕРГИ, без рекурсії.

    Повертає список вузлів у порядку відвідування.
    """
    if root is None:
        return []

    order: List[Node] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

    _color_in_order(order)
    return order


def build_sample_tree() -> Node:
    """Те саме дерево, що у прикладі завдання."""
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    root.right.right = Node(1)
    root.right.left.left = Node(6)
    root.right.left.right = Node(3)
    return root


if __name__ == "__main__":
    # --- DFS ---
    tree = build_sample_tree()
    order = dfs(tree)
    print("DFS (стек): ", [n.val for n in order])
    draw_tree(tree, title="DFS — обхід у глибину (стек)")

    # --- BFS --- (будуємо дерево заново, щоб кольори не змішувалися)
    tree = build_sample_tree()
    order = bfs(tree)
    print("BFS (черга):", [n.val for n in order])
    draw_tree(tree, title="BFS — обхід у ширину (черга)")
