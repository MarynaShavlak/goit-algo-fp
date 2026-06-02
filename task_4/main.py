"""
goit-algo-fp / Завдання 4 — Візуалізація бінарної купи.

Купа зберігається як масив. Для елемента з індексом i його діти — це елементи
з індексами 2*i + 1 (лівий) та 2*i + 2 (правий). За цим правилом будуємо
бінарне дерево з масиву. Вузол (`Node`) і малювання дерева (`draw_tree`) — у
пакеті `viz` (`viz/binary_tree.py`), спільні із Завданням 5.
"""

import argparse
import heapq
from pathlib import Path

from viz.binary_tree import Node, draw_tree


def build_heap_tree(heap: list[int], i: int = 0) -> Node | None:
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
    parser = argparse.ArgumentParser(description="Візуалізація бінарної купи (min/max).")
    parser.add_argument(
        "--save", action="store_true",
        help="зберегти min_heap.png і max_heap.png поруч зі скриптом замість показу вікон",
    )
    args = parser.parse_args()

    here = Path(__file__).parent

    # 1) Будуємо МІН-купу з довільних чисел і візуалізуємо дерево з неї.
    data = [10, 5, 3, 4, 1, 8, 7, 2]
    heapq.heapify(data)            # тепер data — валідна бінарна min-купа
    print("Min-heap:", data)
    draw_tree(build_heap_tree(data), title="Бінарна min-купа",
              save_path=str(here / "min_heap.png") if args.save else None)

    # 2) Готова max-купа (як у прикладі завдання).
    max_heap = [10, 5, 3, 4, 1]
    print("Max-heap:", max_heap)
    draw_tree(build_heap_tree(max_heap), title="Бінарна max-купа",
              save_path=str(here / "max_heap.png") if args.save else None)

    if args.save:
        print(f"Збережено: {here / 'min_heap.png'}, {here / 'max_heap.png'}")
