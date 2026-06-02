"""
goit-algo-fp / Завдання 7 — Метод Монте-Карло: суми при киданні двох кубиків.

Імітуємо велику кількість кидків двох кубиків, рахуємо ймовірність кожної суми
(2..12) і порівнюємо результат з ТОЧНИМИ (аналітичними) ймовірностями.
Стовпчиковий графік — у пакеті `viz` (`viz/dice_chart.py`).
"""

import argparse
import random
from pathlib import Path

from viz.dice_chart import draw_chart


def monte_carlo_dice(n_rolls: int) -> dict[int, float]:
    """Імітує `n_rolls` кидків двох кубиків; повертає ймовірності сум (у %)."""
    if n_rolls <= 0:
        raise ValueError("кількість кидків має бути додатною")
    counts = {s: 0 for s in range(2, 13)}
    for _ in range(n_rolls):
        roll = random.randint(1, 6) + random.randint(1, 6)
        counts[roll] += 1
    return {s: counts[s] / n_rolls * 100 for s in counts}


def ways(s: int) -> int:
    """Кількість комбінацій двох кубиків, що дають суму s."""
    return 6 - abs(s - 7)


def analytical_probabilities() -> dict[int, float]:
    """Точні ймовірності сум (у %).

    Кількість комбінацій для суми s з двох кубиків: ways(s) = 6 - |s - 7|
    (від 1/36 для 2 і 12 до 6/36 для 7), усього 36 рівноймовірних результатів.
    """
    return {s: ways(s) / 36 * 100 for s in range(2, 13)}


def max_deviation(mc: dict[int, float], exact: dict[int, float]) -> float:
    """Максимальне абсолютне відхилення Монте-Карло від аналітики (у в.п.)."""
    return max(abs(mc[s] - exact[s]) for s in range(2, 13))


def print_comparison(mc: dict[int, float], exact: dict[int, float]) -> None:
    """Друкує таблицю: сума | частка | аналітично | Монте-Карло | |Δ|."""
    print(f"{'Сума':>5} | {'Частка':>7} | {'Аналітично':>11} | "
          f"{'Монте-Карло':>12} | {'|Δ|, в.п.':>9}")
    print("-" * 60)
    for s in range(2, 13):
        frac = f"{ways(s)}/36"
        diff = abs(mc[s] - exact[s])
        print(f"{s:>5} | {frac:>7} | {exact[s]:>10.2f}% | "
              f"{mc[s]:>11.2f}% | {diff:>9.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Монте-Карло: суми двох кубиків.")
    parser.add_argument(
        "--save", action="store_true",
        help="зберегти dice.png поруч зі скриптом замість показу вікна",
    )
    args = parser.parse_args()

    random.seed(42)  # для відтворюваності результату
    exact = analytical_probabilities()

    # Збіжність: зі зростанням кількості кидків відхилення від аналітики падає.
    print("Збіжність методу Монте-Карло (макс. відхилення від аналітики):")
    for n in (1_000, 10_000, 100_000):
        mc_n = monte_carlo_dice(n)
        max_err = max_deviation(mc_n, exact)
        print(f"  {n:>7} кидків -> {max_err:.3f} в.п.")

    # Основна симуляція + порівняльна таблиця.
    N = 1_000_000
    mc = monte_carlo_dice(N)
    print(f"\nПорівняльна таблиця ({N:,} кидків):\n".replace(",", " "))
    print_comparison(mc, exact)

    max_err = max_deviation(mc, exact)
    print(f"\nМаксимальне відхилення від аналітики: {max_err:.2f} в.п.")

    # Графік (якщо встановлено matplotlib).
    try:
        if args.save:
            out = Path(__file__).parent / "dice.png"
            draw_chart(mc, exact, N, save_path=str(out))
            print(f"Графік збережено: {out}")
        else:
            draw_chart(mc, exact, N)
    except ImportError:
        print("(matplotlib не встановлено — графік пропущено.)")
