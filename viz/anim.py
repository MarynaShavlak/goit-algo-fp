"""Складання GIF-анімацій із кадрів matplotlib (backend Agg, без дисплея).

`save_gif` малює задану кількість кадрів через колбек `draw_frame(ax, i)` і
склеює їх у зациклений GIF (через Pillow). Дані й алгоритми готують `task_*`,
тут — лише складання анімації.
"""

import io
from collections.abc import Callable


def save_gif(draw_frame: Callable[..., None], n_frames: int, save_path: str,
             figsize: tuple[float, float] = (8.0, 6.0), duration: int = 800) -> None:
    """Рендерить `n_frames` кадрів і зберігає зациклений GIF у `save_path`."""
    import matplotlib.pyplot as plt
    from PIL import Image

    plt.switch_backend("Agg")          # рендер без графічного середовища
    fig, ax = plt.subplots(figsize=figsize)
    frames = []
    for i in range(n_frames):
        ax.clear()
        draw_frame(ax, i)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=80)
        buf.seek(0)
        frames.append(Image.open(buf).convert("RGB"))
    plt.close(fig)
    frames[0].save(save_path, save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, optimize=True)
