from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QGridLayout, QLabel, \
     QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class CloseDialog(MyDialog):
    """
    CloseDialog class to create an exit dialog with confirmation button
    You can check for result after calling `CloseDialog.execute()`
    By checking of value `CloseDialog.result` which can be either [Cancel/Exit]
    """
    def __init__(self, parent=None, info_message="Close Dialog", close_button_name="Close"):
        super().__init__(parent)
        self.info_message = info_message
        self.window_title = "Confirm Exit"
        self.message = QLabel()
        self.messageIcon = QLabel()
        self.exit_button = QPushButton(close_button_name)
        self.cancel_button = QPushButton("Cancel")
        self.result = "Cancel"
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.exit_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.main_layout_spacer_item = QLabel()
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(self.main_layout_spacer_item, 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, -1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_warning()
        self.set_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def set_message_icon_warning(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.WarningCheckBigIconPath))

    def signal_connect(self):
        self.exit_button.clicked.connect(self.click_exit)
        self.cancel_button.clicked.connect(self.click_cancel)

    def click_cancel(self):
        self.result = "Cancel"
        self.close()

    def click_exit(self):
        self.result = "Exit"
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalIcons.WarningCheckBigIcon)
        self.message.setText(self.info_message)

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_default_buttons(self):
        self.cancel_button.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
