"""
goit-algo-fp / Завдання 5 — Візуалізація обходів бінарного дерева.

Обхід у глибину (DFS) та в ширину (BFS) виконуються ІТЕРАТИВНО — за допомогою
стека та черги (без рекурсії). Спільний кістяк обходу — у `_traverse`; `dfs` і
`bfs` лише задають, чи фронтир працює як стек (LIFO), чи як черга (FIFO). Кожен
вузол при відвідуванні отримує унікальний колір; кольори йдуть градієнтом від
ТЕМНИХ (відвідані раніше) до СВІТЛИХ (відвідані пізніше). Вузол (`Node`) і
малювання дерева (`draw_tree`) — у пакеті `viz` (`viz/binary_tree.py`), спільні
із Завданням 4.
"""

import argparse
from collections import deque
from pathlib import Path

from viz.binary_tree import Node, animate_traversal, draw_tree
from viz.colors import lerp_color


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
    r, g, b = (round(c) for c in lerp_color(dark, light, t))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def _color_in_order(order: list[Node]) -> None:
    """Розфарбовує вузли у порядку їх відвідування."""
    total = len(order)
    for i, node in enumerate(order):
        node.color = generate_hex_color(i, total)


def _traverse(root: Node | None, use_stack: bool) -> list[Node]:
    """Ітеративний обхід дерева зі спільним кістяком для DFS і BFS.

    use_stack=True  -> DFS: фронтир працює як стек (LIFO), беремо з кінця;
    use_stack=False -> BFS: фронтир працює як черга (FIFO), беремо з початку.
    У дереві немає циклів, тож множина `visited` не потрібна. Повертає список
    вузлів у порядку відвідування й розфарбовує їх градієнтом за цим порядком.
    """
    if root is None:
        return []

    order: list[Node] = []
    frontier = deque([root])
    while frontier:
        node = frontier.pop() if use_stack else frontier.popleft()
        order.append(node)
        # Для стека (DFS) кладемо праву дитину ПЕРШОЮ, щоб ліва оброблялась
        # раніше (корінь→ліво→право); для черги (BFS) — порядок зліва направо.
        children = (node.right, node.left) if use_stack else (node.left, node.right)
        for child in children:
            if child is not None:
                frontier.append(child)

    _color_in_order(order)
    return order


def dfs(root: Node | None) -> list[Node]:
    """Обхід у глибину (pre-order) ІТЕРАТИВНО — через стек (LIFO), без рекурсії."""
    return _traverse(root, use_stack=True)


def bfs(root: Node | None) -> list[Node]:
    """Обхід у ширину (level-order) ІТЕРАТИВНО — через чергу (FIFO), без рекурсії."""
    return _traverse(root, use_stack=False)


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
    parser = argparse.ArgumentParser(description="Візуалізація обходів дерева (DFS/BFS).")
    parser.add_argument(
        "--save", action="store_true",
        help="зберегти dfs.png і bfs.png поруч зі скриптом замість показу вікон",
    )
    parser.add_argument(
        "--animate", action="store_true",
        help="зберегти покрокові GIF-анімації обходів (dfs.gif, bfs.gif)",
    )
    args = parser.parse_args()

    here = Path(__file__).parent

    # DFS
    tree = build_sample_tree()
    order = dfs(tree)
    print("DFS (стек): ", [n.val for n in order])
    if args.animate:
        animate_traversal(tree, order, title="DFS — обхід у глибину (стек)",
                          save_path=str(here / "dfs.gif"))
    else:
        draw_tree(tree, title="DFS — обхід у глибину (стек)",
                  save_path=str(here / "dfs.png") if args.save else None)

    # BFS (будуємо дерево заново, щоб кольори не змішувалися)
    tree = build_sample_tree()
    order = bfs(tree)
    print("BFS (черга):", [n.val for n in order])
    if args.animate:
        animate_traversal(tree, order, title="BFS — обхід у ширину (черга)",
                          save_path=str(here / "bfs.gif"))
    else:
        draw_tree(tree, title="BFS — обхід у ширину (черга)",
                  save_path=str(here / "bfs.png") if args.save else None)

    if args.save:
        print(f"Збережено: {here / 'dfs.png'}, {here / 'bfs.png'}")
    if args.animate:
        print(f"GIF збережено: {here / 'dfs.gif'}, {here / 'bfs.gif'}")
