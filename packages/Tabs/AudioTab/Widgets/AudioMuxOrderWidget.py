from PySide6.QtWidgets import QCheckBox, QWidget, QHBoxLayout

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.AudioTab.Widgets.AudioMuxAfterTracksComboBox import AudioMuxAfterTracksComboBox


class AudioMuxOrderWidget(QWidget):
    def __init__(self, tab_index):
        super().__init__()
        self.tab_index = tab_index
        self.hint_when_enabled = "<nobr>Define Where the <b>new</b> audio track will be among old audio tracks<" \
                                 "br>The Default behavior is new audios added after the last track<br>" \
                                 "Only check it if you really know what you are doing <br><b>*</b>[" \
                                 "Respecting other audios with the same option] "
        self.setMaximumWidth(300)
        self.setToolTip(self.hint_when_enabled)
        self.mini_layout = QHBoxLayout()
        self.tracks_combobox = AudioMuxAfterTracksComboBox()
        self.check_box = QCheckBox()
        self.check_box.setText("Mux After:")
        self.setup_contents_margin()
        self.setup_mini_layout()
        self.setLayout(self.mini_layout)
        self.check_current_status()
        self.connect_signals()

    def connect_signals(self):
        self.check_box.stateChanged.connect(self.check_box_state_changed)
        self.tracks_combobox.current_index_changed.connect(self.change_global_audio_set_at_top)

    def setup_mini_layout(self):
        self.mini_layout.addWidget(self.check_box, stretch=0)
        self.mini_layout.addWidget(self.tracks_combobox, stretch=2)

    def setup_contents_margin(self):
        self.mini_layout.setSpacing(0)
        self.mini_layout.setContentsMargins(0, 0, 0, 0)
        self.check_box.setContentsMargins(0, 0, 0, 0)
        self.tracks_combobox.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def change_global_audio_set_at_top(self, new_order):
        GlobalSetting.AUDIO_SET_ORDER[self.tab_index] = new_order

    def check_box_state_changed(self, new_state):
        if new_state:
            self.tracks_combobox.setEnabled(True)
            if not GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_REORDER_ACTIVATED:
                self.tracks_combobox.update_tracks(
                    number_of_tracks=len(GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.keys()))
            else:
                self.tracks_combobox.update_tracks(
                    number_of_tracks=0)
        else:
            self.tracks_combobox.setCurrentIndex(-1)
            self.tracks_combobox.setEnabled(False)

    def check_current_status(self):
        if self.check_box.isChecked():
            self.tracks_combobox.setEnabled(True)
            if not GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_REORDER_ACTIVATED:
                if self.tracks_combobox.count() != len(
                        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.keys()) + 1:
                    self.tracks_combobox.update_tracks(
                        number_of_tracks=len(GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.keys()))
                    self.check_box.setChecked(False)
            else:
                if self.tracks_combobox.count() != 1:
                    self.tracks_combobox.update_tracks(
                        number_of_tracks=0)
                    self.check_box.setChecked(False)
        else:
            self.tracks_combobox.setCurrentIndex(-1)
            self.tracks_combobox.setEnabled(False)

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if (
                self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY) and not GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_MODIFIED_ACTIVATED:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)
