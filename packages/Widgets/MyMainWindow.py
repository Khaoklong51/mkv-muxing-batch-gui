import platform
import sys
import typing

from PySide6.QtCore import QRect
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication

from packages.Startup.Options import Options, save_options

if sys.platform == "win32":
    from ctypes import byref, c_bool, sizeof, windll
    from ctypes.wintypes import BOOL
else:
    if typing.TYPE_CHECKING:
        from ctypes import byref, c_bool, sizeof, windll
        from ctypes.wintypes import BOOL


class MyMainWindow(QMainWindow):
    def __init__(self, args, parent=None):
        super().__init__()
        self.is_dark_mode_supported = False
        self.is_os_windows = sys.platform == "win32"
        if self.is_os_windows:
            dwm_api = windll.LoadLibrary("dwmapi")
            try:
                windows_version = int(platform.version().split(".")[2])
            except Exception:
                windows_version = 1
            if windows_version < 19041:
                self.dwnwa_use_immersive_dark_mode = 19
            else:
                self.dwnwa_use_immersive_dark_mode = 20
            self.dwmSetWindowAttribute = dwm_api.DwmSetWindowAttribute

    def apply_saved_window_placement(self, default_width: int, default_height: int):
        self.resize(default_width, default_height)
        geometry = self.get_saved_window_geometry()
        if not geometry:
            return
        self.resize(geometry["width"], geometry["height"])
        if self.is_geometry_on_screen(geometry):
            self.move(geometry["x"], geometry["y"])

    def get_saved_window_geometry(self):
        geometry = Options.Main_Window_Geometry
        if not isinstance(geometry, dict):
            return None
        try:
            width = int(geometry["width"])
            height = int(geometry["height"])
            x = int(geometry["x"])
            y = int(geometry["y"])
        except (KeyError, TypeError, ValueError):
            return None
        if width < 640 or height < 360:
            return None
        return {"x": x, "y": y, "width": width, "height": height}

    @staticmethod
    def is_geometry_on_screen(geometry):
        window_rect = QRect(
            geometry["x"], geometry["y"], geometry["width"], geometry["height"]
        )
        for screen in QApplication.screens():
            if screen.availableGeometry().intersects(window_rect):
                return True
        return False

    def show_saved_window(self):
        if Options.Main_Window_Maximized:
            self.showMaximized()
        else:
            self.showNormal()
        self.raise_()
        self.activateWindow()

    def save_window_placement(self):
        geometry = self.normalGeometry()
        if not geometry.isValid():
            geometry = self.geometry()
        Options.Main_Window_Geometry = {
            "x": geometry.x(),
            "y": geometry.y(),
            "width": geometry.width(),
            "height": geometry.height(),
        }
        Options.Main_Window_Maximized = self.isMaximized()
        save_options()

    def closeEvent(self, event: QCloseEvent):
        self.save_window_placement()
        super().closeEvent(event)

    def set_dark_mode(self, on):
        if self.is_os_windows:
            self.dwmSetWindowAttribute(
                int(self.winId()),
                self.dwnwa_use_immersive_dark_mode,
                byref(c_bool(on)),
                sizeof(BOOL),
            )
            # to force redraw of title bar
            self.resize(self.width(), self.height() + 1)
            self.resize(self.width(), self.height() - 1)
