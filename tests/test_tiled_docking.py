from types import SimpleNamespace

from Xlib import X

from src.docking import DockManager
from src.docking.x11 import X11DockManager
from src.launcher import Launcher, LayoutMode


class FakeDisplay:
    def __init__(self, events):
        self.events = list(events)

    def pending_events(self):
        return len(self.events)

    def next_event(self):
        return self.events.pop(0)


class FakeDock(DockManager):
    def __init__(self, container_size):
        super().__init__()
        self.hwnd_top = 1
        self.hwnd_bottom = 2
        self.container_size = container_size
        self.synced = None

    def create_container(self, x, y, w, h):
        return None

    def process_events(self):
        pass

    def find_window(self, title):
        return None

    def dock_window(self, window_id, parent_id):
        pass

    def undock_window(self, window_id):
        pass

    def sync_layout(self, *args, **kwargs):
        self.synced = args

    def set_window_simple_focus(self, window_id):
        pass

    def get_container_size(self):
        return self.container_size


def make_launcher(container_size):
    launcher = Launcher.__new__(Launcher)
    launcher.docked = True
    launcher.layout_mode = LayoutMode.DUAL
    launcher.dock = FakeDock(container_size)
    launcher.scrcpy = SimpleNamespace(
        f_w1=1920,
        f_h1=1080,
        f_w2=1240,
        f_h2=1080,
    )
    launcher.tx = 0
    launcher.ty = 0
    launcher.bx = 340
    launcher.by = 1080
    launcher._last_sync_params = None
    return launcher


def test_configure_notify_tracks_only_current_container():
    manager = X11DockManager.__new__(X11DockManager)
    DockManager.__init__(manager)
    manager.hwnd_container = 20
    manager._container_size = (1920, 2160)
    manager._pending_container_size = None
    manager._container_resize_deadline = 0.0
    manager.disp = FakeDisplay(
        (
            SimpleNamespace(
                type=X.ConfigureNotify,
                window=SimpleNamespace(id=10),
                width=800,
                height=600,
            ),
            SimpleNamespace(
                type=X.ConfigureNotify,
                window=SimpleNamespace(id=20),
                width=2500,
                height=2160,
            ),
        )
    )

    manager.process_events()

    assert manager.get_container_size() == (1920, 2160)
    manager._container_resize_deadline = 0.0
    manager.process_events()

    assert manager.get_container_size() == (2500, 2160)


def test_tiled_growth_scales_both_children_together():
    launcher = make_launcher((3840, 4320))

    launcher._sync_now()

    assert launcher.dock.synced == (
        0, 0, 680, 2160,
        3840, 2160, 2480, 2160,
    )


def test_tiled_shrink_scales_children_to_fit():
    launcher = make_launcher((1000, 1000))

    launcher._sync_now()

    assert launcher.dock.synced == (
        55, 0, 212, 500,
        889, 500, 574, 500,
    )


def test_container_resize_invalidates_layout_via_sync_parameters():
    launcher = make_launcher((1920, 2160))
    launcher._sync_now()
    initial_layout = launcher.dock.synced

    launcher.dock.container_size = (2500, 3000)
    launcher._sync_now()

    assert launcher.dock.synced != initial_layout
    assert launcher.dock.synced == (
        0, 94, 443, 1500,
        2500, 1406, 1615, 1406,
    )
