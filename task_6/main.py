"""
goit-algo-fp / Завдання 6 — Жадібний алгоритм та динамічне програмування.

Вибір страв із максимальною сумарною калорійністю в межах бюджету —
класична задача про рюкзак 0/1 (кожну страву можна взяти не більше разу).

    * greedy_algorithm           — жадібний вибір за калорії/вартість;
    * dynamic_programming        — гарантовано оптимальний набір (0/1 knapsack);
    * dynamic_programming_value  — лише максимум калорій на 1D-таблиці O(budget).
"""

import argparse
import random
from pathlib import Path

Items = dict[str, dict[str, int]]


def greedy_algorithm(items: Items, budget: int) -> list[str]:
    """Жадібний вибір страв за спаданням співвідношення калорії/вартість.

    Бере страви з найкращим співвідношенням, поки вистачає бюджету. Якщо
    чергова страва не вміщується — пропускає її (continue), а не зупиняється,
    тож може «добрати» дешевші страви далі по списку. Не гарантує оптимуму — це
    евристика для 0/1 knapsack; для від'ємного бюджету кидає ValueError.
    """
    if budget < 0:
        raise ValueError("budget має бути невід'ємним")

    sorted_items = sorted(
        items.items(),
        key=lambda kv: (
            kv[1]["calories"] / kv[1]["cost"] if kv[1]["cost"] > 0 else float("inf")
        ),
        reverse=True,
    )

    result: list[str] = []
    for name, details in sorted_items:
        if details["cost"] <= budget:
            result.append(name)
            budget -= details["cost"]
    return result


def dynamic_programming(items: Items, budget: int) -> list[str]:
    """Динамічне програмування: ГАРАНТОВАНО оптимальний набір страв.

    Класичний рюкзак 0/1 на 2D-таблиці `dp[i][b]` — максимальна калорійність,
    якщо розглянуто перші i страв і дозволено витратити до b. Оптимальний набір
    відновлюємо ЗВОРОТНИМ проходом: страву i взято тоді, коли `dp[i][b]` кращий
    за `dp[i-1][b]` (значення дала саме вона). Для від'ємного бюджету кидає
    ValueError.
    """
    if budget < 0:
        raise ValueError("budget має бути невід'ємним")

    names = list(items)
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]                       # не беремо i-ту страву...
            if cost <= b:                                 # ...або беремо, якщо краще
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)

    # Зворотний прохід: відновлюємо, які саме страви дали dp[n][budget].
    chosen: list[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:                      # значення дала страва i
            chosen.append(names[i - 1])
            b -= items[names[i - 1]]["cost"]
    chosen.reverse()
    return chosen


def dynamic_programming_value(items: Items, budget: int) -> int:
    """Максимальна калорійність (без переліку страв) на 1D-таблиці — O(budget) пам'яті.

    Той самий рюкзак 0/1, але зберігається лише поточний рядок `dp[b]`. Внутрішній
    цикл за бюджетом іде у ЗВОРОТНОМУ порядку, тож кожна страва враховується
    щонайбільше раз. Повертає те саме максимальне значення, що й
    `dynamic_programming`, але без O(n·budget) пам'яті. Для від'ємного бюджету
    кидає ValueError.
    """
    if budget < 0:
        raise ValueError("budget має бути невід'ємним")
    dp = [0] * (budget + 1)
    for details in items.values():
        cost, calories = details["cost"], details["calories"]
        for b in range(budget, cost - 1, -1):
            dp[b] = max(dp[b], dp[b - cost] + calories)
    return dp[budget]


def summarize(items: Items, names: list[str]) -> dict[str, object]:
    """Сумарна вартість і калорійність обраного набору страв."""
    cost = sum(items[n]["cost"] for n in names)
    calories = sum(items[n]["calories"] for n in names)
    return {"items": names, "cost": cost, "calories": calories}


def benchmark_greedy_vs_dp(trials: int = 300, n_items: int = 8,
                           budget: int = 100, seed: int = 42) -> list[float]:
    """Відносний програш жадібного від оптимуму ДП (%) на випадкових меню.

    Генерує `trials` наборів із `n_items` випадкових страв і для кожного рахує
    (ДП − жадібний) / ДП у відсотках. Лише для графіка `--bench`.
    """
    rng = random.Random(seed)
    shortfalls: list[float] = []
    for _ in range(trials):
        items: Items = {
            f"item{i}": {"cost": rng.randint(5, 40), "calories": rng.randint(50, 400)}
            for i in range(n_items)
        }
        dp_cal = sum(items[n]["calories"] for n in dynamic_programming(items, budget))
        greedy_cal = sum(items[n]["calories"] for n in greedy_algorithm(items, budget))
        shortfalls.append(0.0 if dp_cal == 0 else (dp_cal - greedy_cal) / dp_cal * 100)
    return shortfalls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Рюкзак 0/1: демо або бенчмарк greedy vs ДП (--bench)."
    )
    parser.add_argument(
        "--bench", action="store_true",
        help="зберегти графік програшу жадібного від оптимуму (knapsack_compare.png)",
    )
    args = parser.parse_args()

    if args.bench:
        from viz.bench import draw_knapsack_gap
        out = Path(__file__).parent / "knapsack_compare.png"
        draw_knapsack_gap(benchmark_greedy_vs_dp(), save_path=str(out))
        print(f"Графік збережено: {out}")
        raise SystemExit

    items: Items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }
    budget = 100

    greedy = greedy_algorithm(items, budget)
    dp = dynamic_programming(items, budget)

    print(f"Бюджет: {budget}\n")
    print("Жадібний алгоритм:")
    print(f"  {summarize(items, greedy)}")
    print("\nДинамічне програмування:")
    print(f"  {summarize(items, dp)}")

    print("\nДП (лише максимум, O(budget) пам'яті):")
    print(f"  калорій = {dynamic_programming_value(items, budget)}")
