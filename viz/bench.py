"""Графіки емпіричних порівнянь — task_1 (час сортувань) і task_6 (greedy vs ДП).

Дані готують відповідні `task_*` (стандартна бібліотека); тут — лише побудова
графіків через matplotlib. Модуль імпортується тільки в режимі `--bench`.
"""

import matplotlib
import matplotlib.pyplot as plt


def draw_sort_timing(sizes: list[int], insertion: list[float], merge: list[float],
                     save_path: str | None = None) -> None:
    """Лог-лог графік часу insertion_sort vs merge_sort за розміром списку."""
    if save_path:
        matplotlib.use("Agg")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, insertion, "o-", color="#E8590C", label="insertion_sort — O(n²)")
    ax.plot(sizes, merge, "o-", color="#1296F0", label="merge_sort — O(n log n)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("розмір списку n")
    ax.set_ylabel("час, с")
    ax.set_title("Час сортування однозв'язного списку")
    ax.legend()
    ax.grid(visible=True, which="both", linestyle=":", alpha=0.5)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=120)
        plt.close(fig)
    else:
        plt.show()


def draw_knapsack_gap(shortfalls: list[float], save_path: str | None = None) -> None:
    """Гістограма відносного програшу жадібного від оптимуму ДП (%)."""
    if save_path:
        matplotlib.use("Agg")
    optimal = sum(1 for s in shortfalls if s == 0)
    share = 100 * optimal / len(shortfalls) if shortfalls else 0.0
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(shortfalls, bins=20, color="#1296F0", edgecolor="white")
    ax.set_xlabel("програш жадібного від оптимуму ДП, %")
    ax.set_ylabel("кількість випадків")
    ax.set_title(f"Greedy vs ДП на {len(shortfalls)} випадкових меню\n"
                 f"жадібний оптимальний у {share:.0f}% випадків")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=120)
        plt.close(fig)
    else:
        plt.show()
