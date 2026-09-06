from typing import Sequence, Tuple


Rect = Tuple[int, int, int, int]


def layout_bounds(rects: Sequence[Rect]) -> Rect:
    """Return the bounding rectangle containing every layout rectangle."""
    if not rects:
        raise ValueError("layout requires at least one rectangle")

    min_x = min(rect[0] for rect in rects)
    min_y = min(rect[1] for rect in rects)
    max_x = max(rect[0] + rect[2] for rect in rects)
    max_y = max(rect[1] + rect[3] for rect in rects)
    return min_x, min_y, max_x - min_x, max_y - min_y


def layout_size(rects: Sequence[Rect]) -> Tuple[int, int]:
    """Return minimum container size while preserving configured coordinates."""
    if not rects:
        raise ValueError("layout requires at least one rectangle")

    width = max(x + rect_width for x, _, rect_width, _ in rects)
    height = max(y + rect_height for _, y, _, rect_height in rects)
    if width <= 0 or height <= 0:
        raise ValueError("layout dimensions must be positive")
    return width, height


def fit_layout_to_container(
    rects: Sequence[Rect],
    container_width: int,
    container_height: int,
) -> Tuple[Rect, ...]:
    """Scale and center a layout to fit the available container."""
    layout_width, layout_height = layout_size(rects)

    available_width = max(0, container_width)
    available_height = max(0, container_height)
    scale = min(
        available_width / layout_width,
        available_height / layout_height,
    )
    scaled_width = round(layout_width * scale)
    scaled_height = round(layout_height * scale)
    offset_x = max(0, (available_width - scaled_width) // 2)
    offset_y = max(0, (available_height - scaled_height) // 2)

    return tuple(
        (
            offset_x + round(x * scale),
            offset_y + round(y * scale),
            max(1, round(width * scale)),
            max(1, round(height * scale)),
        )
        for x, y, width, height in rects
    )
