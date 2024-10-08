from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QComboBox

from packages.Startup.InitializeScreenResolution import screen_size


class InfoCellDialogTabComboBox(QComboBox):
    def __init__(self, hint):
        super().__init__()
        self.hint_when_enabled = hint
        self.closeOnLineEditClick = False
        self.setStyleSheet("QComboBox::pane {border-radius: 5px;}")
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit().setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.lineEdit().selectionChanged.connect(self.disable_select)
        self.lineEdit().installEventFilter(self)
        self.setMaximumWidth(screen_size.width() // 12)
        self.setMinimumWidth(screen_size.width() // 14)
        self.setToolTip(self.hint_when_enabled)

    def disable_select(self):
        self.lineEdit().deselect()

    def eventFilter(self, object, event):
        if str(event.__class__).find("Event") == -1:
            return False
        try:
            if self.isEnabled():
                if object == self.lineEdit():
                    if event.type() == QEvent.MouseButtonRelease:
                        if self.closeOnLineEditClick:
                            self.hidePopup()
                        else:
                            self.showPopup()
                        return True
                    return False
        except Exception as e:
            return False

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False
