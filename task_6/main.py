"""
goit-algo-fp / Завдання 6 — Жадібний алгоритм та динамічне програмування.

Вибір страв із максимальною сумарною калорійністю в межах бюджету —
класична задача про рюкзак 0/1 (кожну страву можна взяти не більше разу).

    * greedy_algorithm    — жадібний вибір за співвідношенням калорії/вартість;
    * dynamic_programming — гарантовано оптимальний набір (0/1 knapsack).
"""

from typing import Dict, List

Items = Dict[str, Dict[str, int]]


def greedy_algorithm(items: Items, budget: int) -> List[str]:
    """Жадібний вибір страв за спаданням співвідношення калорії/вартість.

    Бере страви з найкращим співвідношенням, поки вистачає бюджету. Якщо
    чергова страва не вміщується — пропускає її (continue), а не зупиняється,
    тож може «добрати» дешевші страви далі по списку.

    Не гарантує оптимуму — це евристика для задачі 0/1 knapsack.
    Складність: O(n log n) (сортування).

    :raises ValueError: якщо budget < 0.
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

    result: List[str] = []
    for name, details in sorted_items:
        if details["cost"] <= budget:
            result.append(name)
            budget -= details["cost"]
    return result


def dynamic_programming(items: Items, budget: int) -> List[str]:
    """Динамічне програмування: ГАРАНТОВАНО оптимальний набір страв.

    Класичний рюкзак 0/1. Зовнішній цикл — страви, внутрішній — бюджет у
    ЗВОРОТНОМУ порядку (від budget до cost). Зворотний порядок гарантує, що
    кожну страву враховано щонайбільше один раз.

    Складність: час O(n * budget), пам'ять O(budget).

    :raises ValueError: якщо budget < 0.
    """
    if budget < 0:
        raise ValueError("budget має бути невід'ємним")

    dp = [0] * (budget + 1)                       # dp[b] — макс. калорійність у межах b
    chosen: List[List[str]] = [[] for _ in range(budget + 1)]

    for name, details in items.items():
        cost, calories = details["cost"], details["calories"]
        for b in range(budget, cost - 1, -1):
            if dp[b - cost] + calories > dp[b]:
                dp[b] = dp[b - cost] + calories
                chosen[b] = chosen[b - cost] + [name]

    return chosen[budget]


def summarize(items: Items, names: List[str]) -> Dict[str, object]:
    """Сумарна вартість і калорійність обраного набору страв."""
    cost = sum(items[n]["cost"] for n in names)
    calories = sum(items[n]["calories"] for n in names)
    return {"items": names, "cost": cost, "calories": calories}


if __name__ == "__main__":
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
