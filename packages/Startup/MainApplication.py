import os
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QToolTip, QStyleFactory


def keep_screen_resolution_good():
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"


keep_screen_resolution_good()
MainApplication = QApplication.instance() or QApplication(sys.argv)

from packages.Startup.GlobalFiles import SettingJsonInfoFilePath  # noqa: E402
from packages.Startup.Options import Options, read_option_file  # noqa: E402
from packages.Startup.SetupThems import (  # noqa: E402
    get_dark_palette,
    get_light_palette,
)


def set_application_style():
    MainApplication.setStyle(QStyleFactory.create("Fusion"))
    if Options.Dark_Mode:
        apply_dark_mode()
    else:
        apply_light_mode()


def apply_light_mode():
    palette = get_light_palette()
    MainApplication.setPalette(palette)
    QToolTip.setPalette(palette)


def apply_dark_mode():
    palette = get_dark_palette()
    MainApplication.setPalette(palette)
    QToolTip.setPalette(palette)


read_option_file(option_file=SettingJsonInfoFilePath)
set_application_style()
