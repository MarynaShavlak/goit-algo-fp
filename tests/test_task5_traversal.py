"""Завдання 5 — ітеративні DFS/BFS і градієнт розфарбування."""


def vals(nodes):
    return [n.val for n in nodes]


def test_dfs_preorder(t5):
    assert vals(t5.dfs(t5.build_sample_tree())) == [0, 4, 5, 10, 1, 3, 6, 3, 1]


def test_bfs_levelorder(t5):
    assert vals(t5.bfs(t5.build_sample_tree())) == [0, 4, 1, 5, 10, 3, 1, 6, 3]


def test_empty_traversals(t5):
    assert t5.dfs(None) == []
    assert t5.bfs(None) == []


def test_colors_gradient_and_unique(t5):
    order = t5.bfs(t5.build_sample_tree())
    colors = [n.color for n in order]
    assert colors[0] == "#08306B"          # перший відвіданий — темний
    assert colors[-1] == "#DEEBF7"         # останній — світлий
    assert len(set(colors)) == len(colors)  # усі кольори унікальні


def test_generate_hex_color_endpoints(t5):
    assert t5.generate_hex_color(0, 9) == "#08306B"
    assert t5.generate_hex_color(8, 9) == "#DEEBF7"
    assert t5.generate_hex_color(0, 1) == "#08306B"   # total <= 1 -> темний
