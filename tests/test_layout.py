import pytest

from src.layout import fit_layout_to_container, layout_bounds, layout_size


THOR_LAYOUT = (
    (0, 0, 1920, 1080),
    (340, 1080, 1240, 1080),
)


def test_layout_bounds_preserve_relative_positions():
    rects = ((-100, 20, 200, 100), (150, 150, 100, 50))

    assert layout_bounds(rects) == (-100, 20, 350, 180)
    assert layout_size(rects) == (250, 200)
    assert fit_layout_to_container(rects, 250, 200) == (
        (-100, 20, 200, 100),
        (150, 150, 100, 50),
    )


def test_layout_preserves_configured_positive_offsets():
    rects = ((100, 50, 200, 100), (150, 150, 100, 50))

    assert layout_size(rects) == (300, 200)
    assert fit_layout_to_container(rects, 300, 200) == rects


def test_layout_scales_up_to_fit_container():
    assert fit_layout_to_container(THOR_LAYOUT, 3840, 4320) == (
        (0, 0, 3840, 2160),
        (680, 2160, 2480, 2160),
    )


def test_layout_centers_on_axis_with_spare_space():
    assert fit_layout_to_container(THOR_LAYOUT, 2500, 2160) == (
        (290, 0, 1920, 1080),
        (630, 1080, 1240, 1080),
    )


def test_layout_scales_down_before_content_is_clipped():
    assert fit_layout_to_container(THOR_LAYOUT, 1000, 1000) == (
        (55, 0, 889, 500),
        (212, 500, 574, 500),
    )


def test_layout_rejects_empty_or_invalid_geometry():
    with pytest.raises(ValueError):
        layout_bounds(())

    with pytest.raises(ValueError):
        layout_size(())

    with pytest.raises(ValueError):
        fit_layout_to_container(((0, 0, 0, 100),), 100, 100)
