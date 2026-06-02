"""Завдання 4 — побудова дерева з масиву-купи (2i+1 / 2i+2)."""

import heapq
from collections import deque


def bfs_vals(node):
    """Рівневий обхід дерева -> список значень."""
    out, queue = [], deque([node])
    while queue:
        n = queue.popleft()
        out.append(n.val)
        if n.left:
            queue.append(n.left)
        if n.right:
            queue.append(n.right)
    return out


def test_empty_heap(t4):
    assert t4.build_heap_tree([]) is None


def test_levelorder_roundtrip(t4):
    data = [10, 5, 3, 4, 1, 8, 7, 2]
    heapq.heapify(data)
    root = t4.build_heap_tree(data)
    # рівневий обхід повного дерева відтворює масив-купу
    assert bfs_vals(root) == data


def test_children_indices(t4):
    data = [10, 5, 3, 4, 1]
    root = t4.build_heap_tree(data)
    # корінь = data[0]; діти = data[1], data[2]; онуки зліва = data[3], data[4]
    assert root.val == 10
    assert root.left.val == 5 and root.right.val == 3
    assert root.left.left.val == 4 and root.left.right.val == 1


def test_min_heap_property(t4):
    data = [10, 5, 3, 4, 1, 8, 7, 2]
    heapq.heapify(data)
    root = t4.build_heap_tree(data)

    def check(node):
        for child in (node.left, node.right):
            if child is not None:
                assert node.val <= child.val
                check(child)

    check(root)
