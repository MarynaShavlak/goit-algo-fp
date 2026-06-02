"""
goit-algo-fp / Завдання 1 — Однозв'язний список: реверс, сортування, злиття.

Реалізовано:
  * reverse         — реверсування списку зміною посилань між вузлами;
  * insertion_sort  — сортування вставками перез'єднанням вузлів;
  * merge_sorted_ll — злиття двох відсортованих списків в один відсортований.
"""


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


def merge_sorted_ll(l1: LinkedList, l2: LinkedList) -> LinkedList:
    """Зливає два ВІДСОРТОВАНІ списки в один відсортований.

    Тримаємо вказівник на хвіст `tail`, щоб вставка була миттєва, інакше довелося
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


if __name__ == "__main__":
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

    llist2 = LinkedList()
    for value in (5, 12, 13, 14, 14, 23, 35, 37, 39, 41):
        llist2.insert_at_end(value)
    print("\nДругий (вже відсортований) список:")
    llist2.print_list()

    print("\nЗлиття двох відсортованих списків:")
    merge_sorted_ll(llist, llist2).print_list()
