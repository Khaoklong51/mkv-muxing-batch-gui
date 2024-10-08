from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QGroupBox

from packages.Startup.Options import Options
from packages.Tabs.AttachmentTab.Widgets.AllowDuplicateAttachmentsCheckBox import AllowDuplicateAttachmentsCheckBox
from packages.Tabs.AttachmentTab.Widgets.AttachmentClearButton import AttachmentClearButton
from packages.Tabs.AttachmentTab.Widgets.AttachmentSourceButton import AttachmentSourceButton
from packages.Tabs.AttachmentTab.Widgets.AttachmentSourceLineEdit import AttachmentSourceLineEdit
from packages.Tabs.AttachmentTab.Widgets.AttachmentTable import AttachmentTable
from packages.Tabs.AttachmentTab.Widgets.AttachmentsTotalSizeValueLabel import AttachmentsTotalSizeValueLabel
from packages.Tabs.AttachmentTab.Widgets.DiscardOldAttachmentsCheckBox import DiscardOldAttachmentsCheckBox
from packages.Tabs.AttachmentTab.Widgets.ExpertModeCheckBox import ExpertModeCheckBox
from packages.Tabs.AttachmentTab.Widgets.MatchAttachmentWidget import MatchAttachmentWidget
from packages.Widgets.RefreshFilesButton import RefreshFilesButton
from packages.Tabs.GlobalSetting import *
from packages.Tabs.GlobalSetting import sort_names_like_windows, get_readable_filesize, get_files_names_absolute_list, \
    get_file_name_absolute_path
from packages.Widgets.InvalidPathDialog import *
# noinspection PyAttributeOutsideInit
from packages.Widgets.WarningDialog import WarningDialog


def get_files_size_list(files_list, folder_path):
    files_size_list = []
    for i in range(len(files_list)):
        file_name_absolute = get_file_name_absolute_path(file_name=files_list[i], folder_path=folder_path)
        file_size_bytes = os.path.getsize(file_name_absolute)
        files_size_list.append(get_readable_filesize(size_bytes=file_size_bytes))
    return files_size_list


def get_files_size_with_absolute_path_list(files_name_absolute_path):
    files_size_list = []
    for i in range(len(files_name_absolute_path)):
        file_name_absolute = files_name_absolute_path[i]
        file_size_bytes = os.path.getsize(file_name_absolute)
        files_size_list.append(get_readable_filesize(size_bytes=file_size_bytes))
    return files_size_list


class AttachmentSelectionSetting(GlobalSetting):
    tab_clicked_signal = Signal()
    activation_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.attachment_source_label = QLabel("Attachment Source Folder:")
        self.attachment_total_size_label = QLabel("Total Attachment Size:")
        self.attachment_total_size_value_label = AttachmentsTotalSizeValueLabel()
        self.attachment_source_lineEdit = AttachmentSourceLineEdit()
        self.attachment_clear_button = AttachmentClearButton()
        self.attachment_source_button = AttachmentSourceButton()
        self.attachment_refresh_files_button = RefreshFilesButton()
        self.discard_old_attachments_checkBox = DiscardOldAttachmentsCheckBox()
        self.allow_duplicate_attachments_checkBox = AllowDuplicateAttachmentsCheckBox()
        self.expert_mode_checkBox = ExpertModeCheckBox()
        self.table = AttachmentTable()
        self.expert_mode_widget = MatchAttachmentWidget(parent=self)
        self.MainLayout = QVBoxLayout()
        self.attachments_options_layout = QHBoxLayout()
        self.attachment_main_groupBox = QGroupBox(self)
        self.attachment_main_layout = QGridLayout()
        self.folder_path = ""
        self.drag_and_dropped_text = "[Drag & Drop Files]"
        self.is_drag_and_drop = False
        self.files_names_list = []
        self.files_checked_list = []
        self.files_names_absolute_list = []
        self.files_size_list = []
        self.setup_layouts()
        self.connect_signals()

    def setup_layouts(self):
        self.setup_attachments_options_layout()
        self.setup_main_layout()
        self.setup_attachment_main_groupBox()
        self.MainLayout.addWidget(self.attachment_main_groupBox)
        self.setLayout(self.MainLayout)

    def setup_attachment_main_groupBox(self):
        self.attachment_main_groupBox.setTitle("Attachments")
        self.attachment_main_groupBox.setCheckable(True)
        self.attachment_main_groupBox.setChecked(False)
        self.attachment_main_groupBox.setLayout(self.attachment_main_layout)
        # self.attachment_main_groupBox.setFocusProxy(Qt.FocusPolicy.NoFocus)

    def update_folder_path(self, new_path: str):
        if self.expert_mode_checkBox.isChecked():
            if new_path != "":
                self.attachment_source_lineEdit.set_text_safe_change(new_path)
                self.expert_mode_widget.update_paths(path=new_path)
                self.attachment_refresh_files_button.update_current_path(new_path=new_path)
                self.attachment_refresh_files_button.setEnabled(True)
            else:
                if self.is_drag_and_drop:
                    self.attachment_source_lineEdit.set_text_safe_change(self.drag_and_dropped_text)

        else:
            if new_path != "":
                self.attachment_source_lineEdit.set_text_safe_change(new_path)
                self.update_files_lists(new_path)
                self.update_total_size()
                self.show_files_list()
                self.attachment_refresh_files_button.update_current_path(new_path=new_path)
                self.attachment_refresh_files_button.setEnabled(True)
            else:
                if self.is_drag_and_drop:
                    self.attachment_source_lineEdit.set_text_safe_change(self.drag_and_dropped_text)

    def update_total_size(self):
        self.attachment_total_size_value_label.update_total_size(self.files_names_absolute_list,
                                                                 self.files_checked_list)

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            if self.is_drag_and_drop:
                new_files_absolute_path_list = []
                self.files_names_list = []
                for file_absolute_path in self.files_names_absolute_list_with_dropped_files:
                    if os.path.isdir(file_absolute_path):
                        continue
                    if os.path.getsize(file_absolute_path) == 0:
                        continue
                    new_files_absolute_path_list.append(file_absolute_path)
                    self.files_names_list.append(os.path.basename(file_absolute_path))
                self.attachment_source_lineEdit.stop_check_path = True
                self.attachment_source_lineEdit.setText(self.drag_and_dropped_text)
                self.is_drag_and_drop = True
                self.folder_path = ""
                self.files_names_absolute_list = new_files_absolute_path_list.copy()
                self.files_size_list = get_files_size_with_absolute_path_list(new_files_absolute_path_list)
                self.files_checked_list = ([True] * len(new_files_absolute_path_list))
                self.attachment_source_lineEdit.stop_check_path = False
                self.update_total_size()
            else:
                self.attachment_source_lineEdit.set_text_safe_change("")
            return
        try:
            self.is_drag_and_drop = False
            self.folder_path = folder_path
            self.files_names_list = self.get_files_list(self.folder_path)
            self.files_names_absolute_list = get_files_names_absolute_list(self.files_names_list, self.folder_path)
            self.files_size_list = get_files_size_list(files_list=self.files_names_list, folder_path=self.folder_path)
            self.files_checked_list = ([True] * len(self.files_names_absolute_list))
        except Exception as e:
            invalid_path_dialog = InvalidPathDialog(parent=self)
            invalid_path_dialog.execute()

    def get_files_list(self, folder_path):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, folder_path)
        result = []
        for i in range(len(temp_files_names)):
            if os.path.isdir(temp_files_names_absolute[i]):
                continue
            if os.path.getsize(temp_files_names_absolute[i]) == 0:
                continue
            result.append(temp_files_names[i])
        return result

    def show_files_list(self):
        self.table.show_files_list(files_names_list=self.files_names_list,
                                   files_names_checked_list=self.files_checked_list,
                                   files_size_list=self.files_size_list)
        self.update_other_classes_variables()

    def update_other_classes_variables(self):
        # self.change_global_last_path_directory()
        self.change_global_attachment_list()
        self.attachment_source_lineEdit.set_current_folder_path(self.folder_path)
        self.attachment_source_lineEdit.set_is_drag_and_drop(self.is_drag_and_drop)
        self.attachment_clear_button.set_is_there_old_file(len(self.files_names_list) > 0)

    def setup_attachments_options_layout(self):
        self.attachments_options_layout.addWidget(self.expert_mode_checkBox)
        self.attachments_options_layout.addWidget(self.allow_duplicate_attachments_checkBox)
        self.attachments_options_layout.addWidget(self.discard_old_attachments_checkBox)

    def setup_main_layout(self):
        self.attachment_main_layout.addWidget(self.attachment_source_label, 0, 0)
        self.attachment_main_layout.addWidget(self.attachment_source_lineEdit, 0, 1, 1, 80)
        self.attachment_main_layout.addWidget(self.attachment_clear_button, 0, 81, 1, 1)
        self.attachment_main_layout.addWidget(self.attachment_refresh_files_button, 0, 82, 1, 1)
        self.attachment_main_layout.addWidget(self.attachment_source_button, 0, 83, 1, 1)
        self.attachment_main_layout.addWidget(self.attachment_total_size_label, 1, 0)
        self.attachment_main_layout.addWidget(self.attachment_total_size_value_label, 1, 1)
        self.attachment_main_layout.addLayout(self.attachments_options_layout, 1, 39, 1, -1,
                                              alignment=Qt.AlignmentFlag.AlignRight)
        self.attachment_main_layout.addWidget(self.table, 2, 0, 1, -1)
        self.attachment_main_layout.addWidget(self.expert_mode_widget, 2, 0, 1, -1)

    def clear_files(self):
        if self.expert_mode_checkBox.isChecked():
            self.attachment_refresh_files_button.update_current_path(new_path="")
            self.attachment_refresh_files_button.setEnabled(True)
            self.attachment_source_lineEdit.set_text_safe_change("")
            self.is_drag_and_drop = False
            self.expert_mode_widget.clear_paths()
        else:
            self.folder_path = ""
            self.files_names_list = []
            self.files_names_absolute_list = []
            self.files_size_list = []
            self.attachment_refresh_files_button.update_current_path(new_path="")
            self.attachment_refresh_files_button.setEnabled(True)
            self.attachment_source_lineEdit.set_text_safe_change("")
            self.is_drag_and_drop = False
            self.files_checked_list = []
            self.update_total_size()
            self.show_files_list()

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace() and not self.is_drag_and_drop:
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def change_global_attachment_list(self):
        GlobalSetting.ATTACHMENT_FILES_LIST = self.files_names_list
        GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = self.files_names_absolute_list
        GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST = []
        for i in range(len(self.files_names_list)):
            if self.files_checked_list[i]:
                GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST.append(True)
            else:
                GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST.append(False)

    def connect_signals(self):
        self.attachment_source_button.clicked_signal.connect(self.update_folder_path)
        self.attachment_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.attachment_refresh_files_button.clicked_signal.connect(self.update_folder_path)
        self.attachment_source_lineEdit.set_is_drag_and_drop_signal.connect(self.update_is_drag_and_drop)
        self.attachment_main_groupBox.toggled.connect(self.activate_tab)
        self.tab_clicked_signal.connect(self.tab_clicked)
        self.table.update_checked_attachment_signal.connect(self.update_checked_attachment)
        self.table.update_unchecked_attachment_signal.connect(
            self.update_unchecked_attachment)
        self.table.drop_folder_and_files_signal.connect(self.update_files_with_drag_and_drop)
        self.attachment_clear_button.clear_files_signal.connect(self.clear_files)
        self.expert_mode_checkBox.is_checked_signal.connect(self.expert_mode_toggled)
        self.expert_mode_widget.drag_and_dropped_signal.connect(
            self.disable_attachment_refresh_button_cause_drag_and_drop)
        self.expert_mode_widget.update_total_size_readable_signal.connect(
            self.attachment_total_size_value_label.update_total_size_readable_expert_mode)
        self.expert_mode_widget.is_there_old_paths_signal.connect(self.update_is_there_old_files)

    def expert_mode_toggled(self, on):
        if on:
            self.clear_files()
            self.table.hide()
            self.expert_mode_widget.show()
            GlobalSetting.ATTACHMENT_FILES_LIST = []
            GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST = []
            GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
            GlobalSetting.ATTACHMENT_PATH_DATA_LIST = []
        else:
            self.clear_files()
            self.table.show()
            self.expert_mode_widget.hide()
            self.expert_mode_widget.clear_attachment_table()
            GlobalSetting.ATTACHMENT_FILES_LIST = []
            GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST = []
            GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
            GlobalSetting.ATTACHMENT_PATH_DATA_LIST = []

    def update_checked_attachment(self, attachment_file_name_absolute):
        index = GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST.index(attachment_file_name_absolute)
        self.files_checked_list[index] = True
        self.attachment_total_size_value_label.attachment_checked(attachment_file_name_absolute)

    def update_unchecked_attachment(self, attachment_file_name_absolute):
        index = GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST.index(attachment_file_name_absolute)
        self.files_checked_list[index] = False
        self.attachment_total_size_value_label.attachment_unchecked(attachment_file_name_absolute)

    def tab_clicked(self):
        self.expert_mode_widget.show_video_files()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.disable_editable_widgets()
            self.expert_mode_widget.disable_editable_widgets()
        else:
            self.enable_editable_widgets()
            self.expert_mode_widget.enable_editable_widgets()

    def disable_editable_widgets(self):
        self.attachment_source_lineEdit.setEnabled(False)
        self.attachment_source_button.setEnabled(False)
        self.discard_old_attachments_checkBox.setEnabled(False)
        self.allow_duplicate_attachments_checkBox.setEnabled(False)
        self.attachment_clear_button.setEnabled(False)
        self.attachment_refresh_files_button.setEnabled(False)
        self.expert_mode_checkBox.setEnabled(False)
        self.attachment_main_groupBox.setCheckable(False)
        self.table.setAcceptDrops(False)
        self.table.disable_selection()

    def enable_editable_widgets(self):
        self.attachment_source_lineEdit.setEnabled(True)
        self.attachment_source_button.setEnabled(True)
        self.discard_old_attachments_checkBox.setEnabled(True)
        self.allow_duplicate_attachments_checkBox.setEnabled(True)
        self.expert_mode_checkBox.setEnabled(True)
        self.attachment_clear_button.setEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.enable_selection()
        if not self.is_drag_and_drop:
            self.attachment_refresh_files_button.setEnabled(True)
        else:
            self.disable_attachment_refresh_button_cause_drag_and_drop()
        if GlobalSetting.ATTACHMENT_ENABLED:
            self.attachment_main_groupBox.setCheckable(True)
        else:
            self.attachment_main_groupBox.setCheckable(True)
            GlobalSetting.ATTACHMENT_ENABLED = False
            self.attachment_main_groupBox.setChecked(GlobalSetting.ATTACHMENT_ENABLED)

    def activate_tab(self, on):
        if not on:
            self.table.clear_table()
            self.attachment_source_lineEdit.set_text_safe_change("")
            self.attachment_total_size_value_label.set_total_size_zero()
            self.discard_old_attachments_checkBox.setChecked(False)
            self.allow_duplicate_attachments_checkBox.setChecked(False)
            self.expert_mode_checkBox.setChecked(False)
            self.folder_path = ""
            self.files_names_list = []
            self.files_names_absolute_list = []
            self.files_size_list = []
            self.files_checked_list = []
            self.is_drag_and_drop = False
            self.attachment_refresh_files_button.setEnabled(False)
            self.attachment_source_lineEdit.set_is_drag_and_drop(False)
            GlobalSetting.ATTACHMENT_FILES_LIST = []
            GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
            GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST = []
            GlobalSetting.ATTACHMENT_DISCARD_OLD = False
        else:
            self.attachment_refresh_files_button.setEnabled(True)
        self.activation_signal.emit(on)
        GlobalSetting.ATTACHMENT_ENABLED = on

    def update_files_with_drag_and_drop(self, paths_list):
        duplicate_flag = False
        not_duplicate_files_absolute_path_list = []
        not_duplicate_files_list = []
        duplicate_files_list = []
        new_files_absolute_path_list = []
        for path in paths_list:
            if os.path.isfile(path):
                if os.path.getsize(path) == 0:
                    continue
                new_files_absolute_path_list.append(path)
            else:
                new_files_absolute_path_list.extend(
                    sort_names_like_windows(get_files_names_absolute_list(self.get_files_list(path), path)))

        for new_file_name in new_files_absolute_path_list:
            if os.path.basename(new_file_name).lower() in map(str.lower, self.files_names_list):
                duplicate_flag = True
                duplicate_files_list.append(os.path.basename(new_file_name))
            else:
                not_duplicate_files_absolute_path_list.append(new_file_name)
                not_duplicate_files_list.append(os.path.basename(new_file_name))
                self.files_names_list.append(os.path.basename(new_file_name))
        self.attachment_source_lineEdit.stop_check_path = True
        self.attachment_source_lineEdit.setText(self.drag_and_dropped_text)
        self.is_drag_and_drop = True
        self.folder_path = ""
        self.files_names_absolute_list.extend(not_duplicate_files_absolute_path_list)
        self.files_size_list.extend(get_files_size_with_absolute_path_list(not_duplicate_files_absolute_path_list))
        self.files_checked_list.extend([True] * len(not_duplicate_files_absolute_path_list))
        self.update_total_size()
        self.show_files_list()
        self.attachment_source_lineEdit.stop_check_path = False
        if duplicate_flag:
            info_message = "One or more files have the same name with the old files will be " \
                           "skipped:"
            for file_name in duplicate_files_list:
                info_message += "\n" + file_name
            warning_dialog = WarningDialog(window_title="Duplicate files names", info_message=info_message,
                                           parent=self.window())
            warning_dialog.execute_wth_no_block()
        self.disable_attachment_refresh_button_cause_drag_and_drop()

    def disable_attachment_refresh_button_cause_drag_and_drop(self):
        self.attachment_source_lineEdit.stop_check_path = True
        self.attachment_source_lineEdit.setText(self.drag_and_dropped_text)
        self.update_is_drag_and_drop(True)
        self.attachment_refresh_files_button.setEnabled(False)
        self.attachment_refresh_files_button.setToolTip("Disabled due to Drag/Drop mode")

    def update_is_drag_and_drop(self, new_state):
        self.is_drag_and_drop = new_state

    def set_default_directory(self):
        if Options.CurrentPreset.Default_Attachment_Directory == "":
            return
        self.attachment_main_groupBox.setChecked(True)
        self.attachment_source_lineEdit.set_text_safe_change(Options.CurrentPreset.Default_Attachment_Directory)
        self.update_folder_path(Options.CurrentPreset.Default_Attachment_Directory)
        self.attachment_source_lineEdit.check_new_path()

    def set_preset_options(self):
        self.set_default_directory()

    def update_theme_mode_state(self):
        self.table.update_theme_mode_state()

    def update_is_there_old_files(self, new_state):
        self.attachment_clear_button.set_is_there_old_file(new_state)
