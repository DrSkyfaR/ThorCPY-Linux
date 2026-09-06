from src.scrcpy_manager import select_render_driver


def test_xwayland_uses_software_renderer():
    assert select_render_driver("linux", "wayland", ":0", "x11") == "software"


def test_native_x11_keeps_opengl_renderer():
    assert select_render_driver("linux", "x11", ":0", "x11") == "opengl"


def test_pure_wayland_keeps_opengl_renderer():
    assert select_render_driver("linux", "wayland", None, "wayland") == "opengl"
