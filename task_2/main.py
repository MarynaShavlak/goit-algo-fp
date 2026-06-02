"""
goit-algo-fp / Завдання 2 — Фрактал «дерево Піфагора» (рекурсія).

Рекурсія `pythagoras_segments` будує геометрію дерева (список відрізків), а
рендер відокремлений: малювання у turtle чи збереження PNG — у пакеті `viz`
(`viz/pythagoras.py`). Довжина гілок скорочується з кожним рівнем, а колір і
товщина задаються на боці рендера за рівнем гілки.
"""

import argparse
import math
from pathlib import Path

from viz.pythagoras import render_turtle, save_png

ANGLE = 45      # кут розгалуження (градуси)
SHRINK = 0.75   # коефіцієнт скорочення довжини гілки на кожному рівні

Segment = tuple[float, float, float, float, int]  # (x0, y0, x1, y1, order гілки)


def pythagoras_segments(order: int, size: float,
                        x: float = 0.0, y: float = 0.0,
                        heading: float = 90.0) -> list[Segment]:
    """Рекурсивно будує відрізки дерева Піфагора (без малювання).

    Базовий випадок — `order <= 0` (порожньо). Інакше гілка довжини `size` дає
    відрізок, а з її кінця рекурсивно ростуть ліва (`heading + ANGLE`) і права
    (`heading − ANGLE`) гілки довжини `size * SHRINK`. Стартовий напрямок
    `heading = 90°` — вертикально вгору. Кожен відрізок несе свій `order`, щоб
    рендер обрав товщину й колір.
    """
    segments: list[Segment] = []

    def grow(order: int, size: float, x: float, y: float, heading: float) -> None:
        if order <= 0:   # <= (а не ==) робить рекурсію стійкою до від'ємного --level
            return
        rad = math.radians(heading)
        x1 = x + size * math.cos(rad)
        y1 = y + size * math.sin(rad)
        segments.append((x, y, x1, y1, order))
        grow(order - 1, size * SHRINK, x1, y1, heading + ANGLE)   # ліве піддерево
        grow(order - 1, size * SHRINK, x1, y1, heading - ANGLE)   # праве піддерево

    grow(order, size, x, y, heading)
    return segments


def parse_input(user_input: str) -> int:
    """Парсить рівень рекурсії; кидає ValueError для некоректного вводу."""
    level = int(user_input)
    if level < 0:
        raise ValueError("рівень рекурсії має бути невід'ємним")
    return level


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Фрактал «дерево Піфагора»: інтерактивний turtle або PNG-прев'ю."
    )
    parser.add_argument(
        "--save", nargs="?", const="", metavar="PATH",
        help="зберегти PNG через matplotlib (без turtle-вікна); "
             "без значення — у tree.png поруч зі скриптом",
    )
    parser.add_argument(
        "--level", type=int, default=10,
        help="рівень рекурсії для --save (типово 10, як у tree.png)",
    )
    args = parser.parse_args()

    if args.save is not None:
        # Неінтерактивний режим: рендеримо PNG з відрізків через matplotlib.
        order = args.level
        segments = pythagoras_segments(order, size=1.0)
        out = args.save or (Path(__file__).parent / "tree.png")
        save_png(segments, order, out,
                 title=f"Дерево Піфагора (рівень рекурсії = {order})")
        print(f"PNG збережено: {out}")
    else:
        # Інтерактивний режим: запитуємо рівень рекурсії й малюємо в turtle.
        while True:
            try:
                order = parse_input(input("Введіть рівень рекурсії (рекомендовано 5–12): "))
                break
            except ValueError:
                print("Будь ласка, введіть невід'ємне ціле число.")

        if order > 13:
            print("Увага: великий рівень рекурсії може малюватися повільно.")

        segments = pythagoras_segments(order, size=120.0, y=-120.0 * 2.2)
        render_turtle(segments, order,
                      title=f"Дерево Піфагора (рівень рекурсії = {order})")
