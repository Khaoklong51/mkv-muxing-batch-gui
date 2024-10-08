from packages.Widgets.CloseDialog import CloseDialog


class CloseDialogWhileAtLeastOneOptionSelected(CloseDialog):
    def __init__(self, parent=None):
        super().__init__(parent, info_message="Are you sure you want to exit ?\nThis will discard current selection",
                         close_button_name="Exit")
