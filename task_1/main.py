"""
goit-algo-fp / Завдання 1 — Однозв'язний список: реверс, сортування, злиття.

Реалізовано:
  * reverse         — реверсування списку зміною посилань між вузлами;
  * insertion_sort  — сортування вставками перез'єднанням вузлів (O(n²));
  * merge_sort      — сортування злиттям перез'єднанням вузлів (O(n log n));
  * merge_sorted_ll — злиття двох відсортованих списків в один відсортований.
"""

import argparse
import random
import time
from pathlib import Path


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next: Node | None = None


class LinkedList:
    def __init__(self):
        self.head: Node | None = None

    # базові операції списку

    def insert_at_beginning(self, data) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def insert_after(self, prev_node: Node | None, data) -> None:
        if prev_node is None:
            raise ValueError("попереднього вузла не існує (prev_node is None)")
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key) -> None:
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        assert prev is not None  # голову відсіяно вище, тож prev задано в циклі
        prev.next = cur.next

    def search_element(self, data) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def to_list(self) -> list:
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def print_list(self) -> None:
        print(" -> ".join(map(str, self.to_list())) or "(порожній)")

    # операції Завдання 1

    def reverse(self) -> None:
        """Реверсування списку зміною посилань між вузлами.

        Йдемо списком і для кожного вузла розвертаємо його посилання `next` на
        попередній. Жодних нових вузлів і жодного видалення за значенням.
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next   # запам'ятати наступний вузол
            current.next = prev        # розвернути посилання
            prev = current             # зсунути prev уперед
            current = next_node        # зсунути current уперед
        self.head = prev               # новим head стає колишній хвіст

    def insertion_sort(self) -> None:
        """Сортування вставками перез'єднанням вузлів.

        Будуємо новий відсортований ланцюг `sorted_head`, вставляючи кожен
        ІСНУЮЧИЙ вузол на потрібне місце. Оскільки оперуємо самими вузлами, а не
        їх значеннями, сортування коректне й за наявності однакових значень.
        """
        sorted_head: Node | None = None
        current = self.head
        while current:
            next_node = current.next
            # Вставка на початок, якщо ланцюг порожній або вузол найменший.
            if sorted_head is None or current.data < sorted_head.data:
                current.next = sorted_head
                sorted_head = current
            else:
                # Шукаємо місце: останній вузол із значенням <= поточного.
                search = sorted_head
                while search.next and search.next.data <= current.data:
                    search = search.next
                current.next = search.next
                search.next = current
            current = next_node
        self.head = sorted_head

    def merge_sort(self) -> None:
        """Сортування злиттям (O(n log n), O(log n) пам'яті на стек рекурсії).

        Рекурсивно ділить список навпіл і зливає відсортовані половини,
        перез'єднуючи вузли. На відміну від `insertion_sort` (O(n²)), лишається
        ефективним і на довгих списках.
        """
        self.head = _merge_sort_nodes(self.head)


def _split_middle(head: Node) -> Node | None:
    """Розриває ланцюг на дві половини; повертає голову другої (slow/fast)."""
    slow: Node = head
    fast: Node | None = head.next
    while fast is not None and fast.next is not None:
        assert slow.next is not None  # fast попереду, тож наступний у slow існує
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None              # розриваємо список рівно посередині
    return mid


def _merge_nodes(a: Node | None, b: Node | None) -> Node | None:
    """Зливає два відсортовані ланцюги вузлів в один (перез'єднанням, без копій)."""
    dummy = Node()
    tail = dummy
    while a is not None and b is not None:
        if a.data <= b.data:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        assert tail.next is not None
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def _merge_sort_nodes(head: Node | None) -> Node | None:
    """Рекурсивне сортування злиттям ланцюга вузлів. O(n log n)."""
    if head is None or head.next is None:
        return head
    mid = _split_middle(head)
    return _merge_nodes(_merge_sort_nodes(head), _merge_sort_nodes(mid))


def merge_sorted_ll(l1: LinkedList, l2: LinkedList) -> LinkedList:
    """Зливає два ВІДСОРТОВАНІ списки в один відсортований.

    Зберігаємо вказівник на хвіст `tail`, щоб вставка була миттєва, інакше довелося
    б щоразу проходити весь зібраний список. Вихідні списки не змінюються: у новий
    список копіюються значення.
    """
    merged = LinkedList()
    tail: Node | None = None

    def append(value) -> None:
        nonlocal tail
        node = Node(value)
        if merged.head is None:
            merged.head = node
        else:
            assert tail is not None  # гілка else означає, що список уже непорожній
            tail.next = node
        tail = node

    a, b = l1.head, l2.head
    while a and b:
        if a.data <= b.data:
            append(a.data)
            a = a.next
        else:
            append(b.data)
            b = b.next

    # Дозбираємо залишок того списку, що ще не вичерпався.
    remaining = a or b
    while remaining:
        append(remaining.data)
        remaining = remaining.next

    return merged


def benchmark_sorts(sizes: tuple[int, ...] = (200, 400, 800, 1600, 3200),
                    seed: int = 42) -> dict:
    """Час insertion_sort vs merge_sort (секунди) за розміром списку.

    Для кожного n будується однаковий випадковий список і замірюються обидва
    сортування. Лише для графіка `--bench`; на коректність не впливає.
    """
    rng = random.Random(seed)
    insertion: list[float] = []
    merge: list[float] = []
    for n in sizes:
        data = [rng.randint(0, 10_000) for _ in range(n)]

        ll1 = LinkedList()
        for v in data:
            ll1.insert_at_end(v)
        start = time.perf_counter()
        ll1.insertion_sort()
        insertion.append(time.perf_counter() - start)

        ll2 = LinkedList()
        for v in data:
            ll2.insert_at_end(v)
        start = time.perf_counter()
        ll2.merge_sort()
        merge.append(time.perf_counter() - start)
    return {"sizes": list(sizes), "insertion": insertion, "merge": merge}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Однозв'язний список: демо або бенчмарк сортувань (--bench)."
    )
    parser.add_argument(
        "--bench", action="store_true",
        help="зберегти графік часу insertion_sort vs merge_sort (sort_timing.png)",
    )
    args = parser.parse_args()

    if args.bench:
        from viz.bench import draw_sort_timing
        data = benchmark_sorts()
        out = Path(__file__).parent / "sort_timing.png"
        draw_sort_timing(data["sizes"], data["insertion"], data["merge"],
                         save_path=str(out))
        print(f"Графік збережено: {out}")
        raise SystemExit

    llist = LinkedList()
    for value in (5, 15, 10, 35, 25):
        llist.insert_at_end(value)

    print("Зв'язний список:")
    llist.print_list()

    print("\nОбернений список:")
    llist.reverse()
    llist.print_list()

    print("\nВідсортований список (вставками):")
    llist.insertion_sort()
    llist.print_list()

    print("\nТой самий набір, відсортований злиттям (O(n log n)):")
    ll_ms = LinkedList()
    for value in (5, 15, 10, 35, 25):
        ll_ms.insert_at_end(value)
    ll_ms.merge_sort()
    ll_ms.print_list()

    llist2 = LinkedList()
    for value in (5, 12, 13, 14, 14, 23, 35, 37, 39, 41):
        llist2.insert_at_end(value)
    print("\nДругий (вже відсортований) список:")
    llist2.print_list()

    print("\nЗлиття двох відсортованих списків:")
    merge_sorted_ll(llist, llist2).print_list()
