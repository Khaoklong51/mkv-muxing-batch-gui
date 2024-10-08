from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QGridLayout, QLabel, \
     QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class ConfirmCheckMakeThisTrackDefaultWithUnCheckOption(MyDialog):
    def __init__(self, track_type, parent=None):
        super().__init__(parent)
        self.track_type = track_type
        self.yesButton = QPushButton("OK")
        self.noButton = QPushButton("Cancel")
        self.thirdButton = QPushButton("Uncheck this one")
        self.setWindowTitle("Confirm Check")
        self.setWindowIcon(GlobalIcons.QuestionIcon)
        self.message = QLabel("<nobr>Are you sure?<br>This will <b>uncheck</b> set default and set forced options "
                              "from " + self.track_type + " tab")
        self.messageIcon = QLabel()

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.thirdButton)
        self.buttons_layout.addWidget(self.yesButton)
        self.buttons_layout.addWidget(self.noButton)
        self.main_layout_spacer_item = QLabel()
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(self.main_layout_spacer_item, 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 4, 1, 1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_info()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.yesButton.clicked.connect(self.click_yes)
        self.noButton.clicked.connect(self.click_no)
        self.thirdButton.clicked.connect(self.click_third_button)

    def click_yes(self):
        self.result = "Yes"
        self.close()

    def click_no(self):
        self.result = "No"
        self.close()

    def click_third_button(self):
        self.result = "Third"
        self.close()

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_message_icon_info(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.InfoBigIconPath))

    def set_default_buttons(self):
        self.yesButton.setDefault(False)
        self.noButton.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
