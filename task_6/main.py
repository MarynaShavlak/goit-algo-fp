"""
goit-algo-fp / Завдання 6 — Жадібний алгоритм та динамічне програмування.

Вибір страв із максимальною сумарною калорійністю в межах бюджету —
класична задача про рюкзак 0/1 (кожну страву можна взяти не більше разу).

    * greedy_algorithm    — жадібний вибір за співвідношенням калорії/вартість;
    * dynamic_programming — гарантовано оптимальний набір (0/1 knapsack).
"""

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


def summarize(items: Items, names: list[str]) -> dict[str, object]:
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
