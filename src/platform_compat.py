# DualCPY Linux - Dual-screen scrcpy docking and control UI
# Copyright (C) 2026 the_swest
# Contact: Github issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# src/platform_compat.py
#
# Small cross-platform shims so the customtkinter UI (originally Windows-only)
# runs on Linux. Each helper degrades gracefully when its backend is missing.

import sys
import logging

logger = logging.getLogger(__name__)


def apply_dark_titlebar(window):
    """Apply a dark window title bar where the platform supports it.

    On Windows this calls DwmSetWindowAttribute via the Tk window's HWND.
    On Linux/macOS the window manager draws the frame, so this is a no-op.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes
        from src.win32_darkmode import enable_dark_titlebar
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id()) or window.winfo_id()
        enable_dark_titlebar(hwnd)
    except Exception as e:
        logger.debug(f"apply_dark_titlebar skipped: {e}")


def get_clipboard_text(widget):
    """Read clipboard text via Tk (cross-platform). Returns '' on failure."""
    try:
        return widget.clipboard_get()
    except Exception as e:
        logger.debug(f"clipboard read failed: {e}")
        return ""


def set_clipboard_text(widget, text):
    """Write text to the clipboard via Tk (cross-platform)."""
    try:
        widget.clipboard_clear()
        widget.clipboard_append(text)
    except Exception as e:
        logger.debug(f"clipboard write failed: {e}")


def grab_region_png(left, top, width, height, path):
    """Capture a screen region to a PNG file using mss (X11/Wayland/Win/mac).

    Returns True on success. Replaces the Windows-only dxcam path.
    """
    if width <= 0 or height <= 0:
        logger.error(f"grab_region_png: invalid size {width}x{height}")
        return False
    try:
        import mss
        import mss.tools
        with mss.mss() as sct:
            region = {"left": int(left), "top": int(top),
                      "width": int(width), "height": int(height)}
            img = sct.grab(region)
            mss.tools.to_png(img.rgb, img.size, output=path)
        logger.info(f"Saved screenshot region -> {path}")
        return True
    except Exception as e:
        logger.error(f"grab_region_png failed: {e}")
        return False


def grab_x11_window_png(window_id, path):
    """Capture an X11 window directly to a PNG file.

    This is more reliable than screen-region capture on some WMs because it
    reads the window's own pixels instead of the compositor output.
    """
    if not window_id:
        return False

    try:
        from Xlib import X, display
        from PIL import Image

        disp = display.Display()
        win = disp.create_resource_object("window", int(window_id))
        geom = win.get_geometry()
        width = int(geom.width)
        height = int(geom.height)
        if width <= 0 or height <= 0:
            logger.error(f"grab_x11_window_png: invalid size {width}x{height}")
            return False

        raw = win.get_image(0, 0, width, height, X.ZPixmap, 0xFFFFFFFF)
        data = raw.data
        if not data:
            logger.error("grab_x11_window_png: empty image data")
            return False

        if len(data) >= width * height * 4:
            image = Image.frombytes("RGBA", (width, height), data, "raw", "BGRA")
        else:
            image = Image.frombytes("RGB", (width, height), data, "raw", "BGR")

        image.save(path)
        logger.info(f"Saved X11 window screenshot -> {path}")
        return True
    except Exception as e:
        logger.error(f"grab_x11_window_png failed: {e}")
        return False
