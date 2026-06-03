"""Рендер фрактала «дерево Піфагора» — task_2.

Геометрію (список відрізків) обчислює рекурсія `pythagoras_segments` у
`task_2/main.py`; ці функції лише малюють уже готові відрізки, тож рендер
відокремлений від рекурсії. Один і той самий набір відрізків можна показати у
turtle (інтерактивно) або зберегти в PNG через matplotlib.

Відрізок — кортеж `(x0, y0, x1, y1, order)`, де `order` — рівень гілки (більший
ближче до кореня); за ним обираємо товщину й колір.
"""

from .colors import lerp_color

Segment = tuple[float, float, float, float, int]


def branch_color(order: int, max_order: int) -> tuple[float, float, float]:
    """Колір гілки: від коричневого (біля кореня) до зеленого (на верхівках)."""
    t = 0.0 if max_order <= 0 else 1 - order / max_order
    brown, green = (0.40, 0.26, 0.13), (0.13, 0.55, 0.13)
    r, g, b = lerp_color(brown, green, t)
    return r, g, b


def render_turtle(segments: list[Segment], max_order: int,
                  title: str | None = None) -> None:
    """Малює відрізки у вікні turtle; екран автоматично кадрується під дерево."""
    import turtle

    screen = turtle.Screen()
    screen.setup(width=900, height=800)
    screen.bgcolor("white")
    if title:
        screen.title(title)

    # Підганяємо систему координат під межі дерева (працює для будь-якого рівня).
    if segments:
        xs = [s[0] for s in segments] + [s[2] for s in segments]
        ys = [s[1] for s in segments] + [s[3] for s in segments]
        margin = 0.05 * max(max(xs) - min(xs), max(ys) - min(ys), 1.0)
        screen.setworldcoordinates(min(xs) - margin, min(ys) - margin,
                                   max(xs) + margin, max(ys) + margin)

    screen.tracer(0)            # миттєве відмалювання, без покрокової анімації
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    for x0, y0, x1, y1, order in segments:
        t.penup()
        t.goto(x0, y0)
        t.pendown()
        t.width(max(1, order))                 # товщі гілки ближче до кореня
        t.pencolor(branch_color(order, max_order))
        t.goto(x1, y1)

    screen.update()
    screen.mainloop()


def save_png(segments: list[Segment], max_order: int,
             save_path, title: str | None = None) -> str:
    """Рендерить відрізки у PNG через matplotlib (backend Agg, без дисплея)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    lines = [((x0, y0), (x1, y1)) for x0, y0, x1, y1, _ in segments]
    colors = [branch_color(o, max_order) for *_, o in segments]
    widths = [max(0.6, o * 0.7) for *_, o in segments]   # товщі гілки ближче до кореня

    fig, ax = plt.subplots(figsize=(10.4, 10.4))
    ax.add_collection(LineCollection(lines, colors=colors, linewidths=widths,
                                     capstyle="round"))
    if title:
        ax.set_title(title, fontsize=15)
    ax.autoscale()
    ax.set_aspect("equal")
    ax.margins(0.04)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(save_path, dpi=100)
    plt.close(fig)
    return str(save_path)
