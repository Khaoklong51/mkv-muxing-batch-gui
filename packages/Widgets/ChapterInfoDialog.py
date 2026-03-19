from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFormLayout,
    QDoubleSpinBox,
)

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class ChapterInfoDialog(MyDialog):
    def __init__(
        self,
        chapter_name: str = "Test",
        chapter_delay=0.0,
        chapter_default_value_delay=0.0,
        parent=None,
    ):
        super().__init__(parent)
        self.window_title = "Chapter Info"
        self.state = "no"
        self.messageIcon = QLabel()
        self.chapter_name_label = QLabel("Chapter Name:")
        self.chapter_name_value = QLabel(str(chapter_name))

        self.current_chapter_delay = chapter_delay

        self.chapter_delay_label = QLabel("Chapter Delay:")
        self.chapter_delay_spin = QDoubleSpinBox()
        self.chapter_default_delay = chapter_default_value_delay
        self.setup_chapter_delay_spin()

        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")
        self.reset_button = QPushButton("Reset To Default")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch(stretch=4)
        self.buttons_layout.addWidget(self.reset_button, stretch=2)
        self.buttons_layout.addWidget(self.yes_button, stretch=2)
        self.buttons_layout.addWidget(self.no_button, stretch=2)
        self.buttons_layout.addStretch(stretch=4)
        self.chapter_setting_layout = QGridLayout()
        self.chapter_editable_setting_layout = QFormLayout()
        self.chapter_editable_setting_layout.addRow(
            self.chapter_name_label, self.chapter_name_value
        )
        self.chapter_editable_setting_layout.addRow(
            self.chapter_delay_label,
            self.chapter_delay_spin,
        )
        self.chapter_setting_layout.addLayout(
            self.chapter_editable_setting_layout, 1, 0, 4, 2
        )
        self.chapter_setting_layout.addWidget(self.messageIcon, 0, 3, 5, -1)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.chapter_setting_layout, 0, 0, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, 1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_chapter_delay_spin(self):
        # self.chapter_delay_spin.setMaximumWidth(screen_size.width() // 16)
        self.chapter_delay_spin.setDecimals(3)
        self.chapter_delay_spin.setMinimum(-9999.0)
        self.chapter_delay_spin.setMaximum(9999.0)
        self.chapter_delay_spin.setSingleStep(0.5)
        self.chapter_delay_spin.setValue(float(self.current_chapter_delay))

    def update_current_chapter_delay(self):
        self.current_chapter_delay = round(self.chapter_delay_spin.value(), 5)

    def setup_ui(self):
        self.disable_question_mark_window()
        self.messageIcon.setPixmap(
            QtGui.QPixmap(GlobalFiles.ChapterIconPath).scaledToHeight(60)
        )
        self.set_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.chapter_delay_spin.editingFinished.connect(self.update_current_chapter_delay)
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        self.reset_button.clicked.connect(self.reset_chapter_setting)

    def reset_chapter_setting(self):
        self.chapter_delay_spin.setValue(float(self.chapter_default_delay))

    def click_yes(self):
        self.state = "yes"
        self.close()

    def click_no(self):
        self.state = "no"
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalIcons.InfoSettingIcon)

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def set_default_buttons(self):
        self.yes_button.setDefault(True)
        self.yes_button.setFocus()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
