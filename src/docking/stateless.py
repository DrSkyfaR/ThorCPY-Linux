from src.docking import DockManager
import logging

logger = logging.getLogger(__name__)

class StatelessDockManager(DockManager):
    """
    Fallback dock manager for pure Wayland sessions (no XWayland available).
    Window embedding is not possible without an X11 server; all docking
    operations are no-ops and scrcpy windows float freely.
    """

    def __init__(self):
        logger.info("Initializing StatelessDockManager (Floating Mode)")
        self.hwnd_container = None
        self.hwnd_top = None
        self.hwnd_bottom = None

    def create_container(self, x, y, w, h):
        """
        No container window needed in floating mode.
        Returns a dummy ID.
        """
        logger.debug("StatelessDockManager: create_container called (no-op)")
        return 0

    def process_events(self):
        """
        No platform specific event loop needed here.
        """
        pass

    def find_window(self, title):
        """
        We can't reliably find/control specific window IDs in a cross-platform way 
        without X11/Win32 APIs. In Wayland, this is restricted.
        Returns None to indicate we don't 'own' the window.
        """
        # logger.debug(f"StatelessDockManager: find_window '{title}' called (no-op)")
        return None

    def dock_window(self, window_id, parent_id):
        """
        Docking is not supported.
        """
        logger.debug("StatelessDockManager: dock_window called (no-op)")
        return False

    def undock_window(self, window_id):
        """
        Undocking is not supported (windows are always floating).
        """
        return True

    def sync_layout(self, tx, ty, bx, by, w1, h1, w2, h2, is_docked=True):
        """
        Layout synchronization is not possible as we don't control window positions.
        """
        pass
    
    def resize_container(self, container_id, w, h):
        """No-op in floating mode."""
        pass

    def set_window_simple_focus(self, window_id):
        """
        Cannot reliably set focus in restricted environments.
        """
        return False
