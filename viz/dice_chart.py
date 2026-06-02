"""Стовпчиковий графік «Монте-Карло vs аналітика» — task_7.

Симуляція та аналітичні ймовірності рахуються у `task_7/main.py`; тут лише
малювання. matplotlib імпортується ВСЕРЕДИНІ функції («м'яка» залежність), тож
без бібліотеки task_7 усе одно виведе таблицю в консоль.
"""

def draw_chart(mc: dict[int, float], exact: dict[int, float],
               n_rolls: int, save_path: str | None = None) -> None:
    """Стовпчиковий графік: Монте-Карло поряд з аналітикою (потрібен matplotlib).

    Якщо передано `save_path` — зберігає PNG (без дисплея), інакше показує вікно.
    """
    import matplotlib
    if save_path:
        matplotlib.use("Agg")        # рендер у файл без графічного середовища
    import matplotlib.pyplot as plt

    sums = list(range(2, 13))
    x = list(range(len(sums)))
    width = 0.4

    plt.figure(figsize=(10, 6))
    plt.bar([i - width / 2 for i in x], [mc[s] for s in sums], width,
            label="Монте-Карло", color="#1296F0")
    plt.bar([i + width / 2 for i in x], [exact[s] for s in sums], width,
            label="Аналітично", color="#E8590C")
    plt.xticks(x, sums)
    plt.xlabel("Сума на двох кубиках")
    plt.ylabel("Імовірність, %")
    plt.title(f"Метод Монте-Карло vs аналітика ({n_rolls:,} кидків)".replace(",", " "))
    plt.legend()
    plt.grid(axis="y", ls="--", alpha=0.4)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=130)
        plt.close()
    else:
        plt.show()
