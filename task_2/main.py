"""
goit-algo-fp / Завдання 2 — Фрактал «дерево Піфагора» (рекурсія + turtle).

Користувач задає рівень рекурсії; програма малює дерево Піфагора (гілчастий
варіант). Довжина гілок скорочується з кожним рівнем, а колір змінюється
градієнтом від коричневого (стовбур) до зеленого (верхівки).
"""

import turtle
from typing import Tuple

ANGLE = 45      # кут розгалуження (градуси)
SHRINK = 0.75   # коефіцієнт скорочення довжини гілки на кожному рівні


def _branch_color(order: int, max_order: int) -> Tuple[float, float, float]:
    """Колір гілки: від коричневого (біля кореня) до зеленого (на верхівках)."""
    t = 0.0 if max_order <= 0 else 1 - order / max_order
    brown, green = (0.40, 0.26, 0.13), (0.13, 0.55, 0.13)
    return tuple(b + (g - b) * t for b, g in zip(brown, green))


def pythagoras_tree(t: "turtle.Turtle", order: int, size: float, max_order: int) -> None:
    """Рекурсивно малює дерево Піфагора.

    Базовий випадок — `order == 0` (нічого не малюємо). Інакше малюємо гілку
    завдовжки `size`, далі рекурсивно ліве піддерево (поворот на +ANGLE) і праве
    (поворот на -ANGLE) з коротшою гілкою `size * SHRINK`.
    """
    if order == 0:
        return

    t.width(max(1, order))                 # товщі гілки ближче до кореня
    t.pencolor(_branch_color(order, max_order))
    t.forward(size)

    # Запам'ятовуємо точку розгалуження та поточний напрямок.
    x, y = t.position()
    heading = t.heading()

    # Ліве піддерево.
    t.left(ANGLE)
    pythagoras_tree(t, order - 1, size * SHRINK, max_order)

    # Повертаємось у точку розгалуження БЕЗ малювання й малюємо праве піддерево.
    # (penup/goto/pendown — портативна заміна t.teleport, доступного лише з 3.12.)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(heading)
    t.right(ANGLE)
    pythagoras_tree(t, order - 1, size * SHRINK, max_order)


def draw_pythagoras_tree(order: int, size: float = 120) -> None:
    """Налаштовує екран turtle і малює дерево заданого рівня рекурсії."""
    screen = turtle.Screen()
    screen.setup(width=900, height=800)
    screen.bgcolor("white")
    screen.title(f"Дерево Піфагора (рівень рекурсії = {order})")
    screen.tracer(0)            # вимикаємо покрокову анімацію — миттєве відмалювання

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.goto(0, -size * 2.2)      # старт унизу по центру
    t.setheading(90)            # стовбур росте вертикально вгору
    t.pendown()

    pythagoras_tree(t, order, size, order)

    screen.update()
    screen.mainloop()


def parse_input(user_input: str) -> int:
    """Парсить рівень рекурсії; кидає ValueError для некоректного вводу."""
    level = int(user_input)
    if level < 0:
        raise ValueError("рівень рекурсії має бути невід'ємним")
    return level


if __name__ == "__main__":
    while True:
        try:
            order = parse_input(input("Введіть рівень рекурсії (рекомендовано 5–12): "))
            break
        except ValueError:
            print("Будь ласка, введіть невід'ємне ціле число.")

    if order > 13:
        print("Увага: великий рівень рекурсії може малюватися повільно.")

    draw_pythagoras_tree(order)
