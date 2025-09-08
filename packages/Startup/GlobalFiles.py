import logging
import struct
import subprocess
import sys
from pathlib import Path
import os
from shutil import which

from packages.Widgets.MissingFilesMessage import MissingFilesMessage


def create_app_data_folder():
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """
    home = Path.home()
    app_data = ""
    if sys.platform == "win32":
        app_data = home / "AppData/Roaming"
    elif sys.platform == "linux":
        app_data = home / ".local/share"
    elif sys.platform == "darwin":
        app_data = home / "Library/Application Support"
    my_app_data_folder = app_data / "MKV Muxing Batch GUI"
    try:
        my_app_data_folder.mkdir(exist_ok=True)
    except Exception:
        pass
    return my_app_data_folder


def add_double_quotation(string):
    return '"' + str(string) + '"'


def get_file_name_absolute_path(file_name: str, folder_path) -> Path:
    return Path(folder_path) / file_name


def get_files_names_absolute_list(files_names, folder_path) -> list[Path]:
    result = []
    for i in range(len(files_names)):
        result.append(
            get_file_name_absolute_path(file_name=files_names[i], folder_path=folder_path)
        )
    return result


def delete_old_media_files():
    only_media_info_files = MediaInfoFolderPath.iterdir()
    for file_name in only_media_info_files:
        file_name.unlink(missing_ok=True)


script_path = Path(sys.argv[0])  # get path of the this file
script_folder = script_path.parent
resources_folder = script_folder.resolve() / "Resources"
FontFolderPath = resources_folder.resolve() / "Fonts"
IconFolderPath = resources_folder.resolve() / "Icons"
DLLFolderPath = resources_folder.resolve() / "DLL"
GlobalToolsFolderPath = resources_folder.resolve() / "Tools"
ToolsFolderPath = GlobalToolsFolderPath.resolve() / "Windowsx64"
LanguagesFolderPath = resources_folder.resolve() / "Languages"
LibFolderPath = ""
if sys.platform == "win32":
    if struct.calcsize("P") * 8 == 32:
        ToolsFolderPath = GlobalToolsFolderPath.resolve() / "Windows32"
    else:
        ToolsFolderPath = GlobalToolsFolderPath.resolve() / "Windows64"

elif sys.platform == "linux" or sys.platform == "linux2":
    ToolsFolderPath = GlobalToolsFolderPath.resolve() / "Linux"
    LibFolderPath = ToolsFolderPath.resolve() / "lib"
else:
    ToolsFolderPath = GlobalToolsFolderPath.resolve() / "Other Systems"

AppDataFolderPath = create_app_data_folder()
MergeLogsFolderPath = AppDataFolderPath.resolve() / "Logs"
MediaInfoFolderPath = AppDataFolderPath.resolve() / "MediaInfo"
MergeLogsFolderPath.mkdir(exist_ok=True, parents=True)
MediaInfoFolderPath.mkdir(exist_ok=True, parents=True)
delete_old_media_files()


def get_mkvmerge_version():
    command = [MKVMERGE_PATH, "-V"]
    result = subprocess.run(command, stdout=subprocess.PIPE, env=ENVIRONMENT, text=True)
    return result.stdout.strip()


def get_mkvpropedit_version():
    command = [MKVPROPEDIT_PATH, "-V"]
    result = subprocess.run(command, stdout=subprocess.PIPE, env=ENVIRONMENT, text=True)
    return result.stdout.strip()


def update_enviro_if_not_windows():
    if "LD_LIBRARY_PATH" not in ENVIRONMENT.keys():
        ENVIRONMENT["LD_LIBRARY_PATH"] = ""
    if sys.platform != "win32":
        ENVIRONMENT["LD_LIBRARY_PATH"] = (
            f"{Path(LibFolderPath).resolve()}:{ENVIRONMENT['LD_LIBRARY_PATH']}"
        )


def get_program_from_path_and_tool(program: str) -> Path:
    program_path = which(program)

    if program_path is None:
        logging.warning("Could not find system mkvmerge. Trying portable version...")
        program_path = ToolsFolderPath.resolve() / program
    else:
        program_path = Path(program_path)

    return program_path


try:
    MyFontPath = FontFolderPath.resolve() / "OpenSans.ttf"
    WarningCheckBigIconPath = IconFolderPath.resolve() / "WarningCheckBig.png"
    WarningCheckIconPath = IconFolderPath.resolve() / "WarningCheck.png"
    TrueCheckIconPath = IconFolderPath.resolve() / "TrueCheck.png"
    GreenTikMarkIconPath = IconFolderPath.resolve() / "GreenTikMark.png"
    RedCrossMarkIconPath = IconFolderPath.resolve() / "RedCrossMark.png"
    ChapterIconPath = IconFolderPath.resolve() / "Chapter.svg"
    SubtitleLightIconPath = IconFolderPath.resolve() / "Subtitle_Light.svg"
    AudioLightIconPath = IconFolderPath.resolve() / "Audio_Light.svg"
    SubtitleDarkIconPath = IconFolderPath.resolve() / "Subtitle_Dark.svg"
    AudioDarkIconPath = IconFolderPath.resolve() / "Audio_Dark.svg"
    StartMultiplexingIconPath = IconFolderPath.resolve() / "StartMultiplexing.png"
    PauseMultiplexingIconPath = IconFolderPath.resolve() / "Pause.png"
    AddToQueueIconPath = IconFolderPath.resolve() / "AddToQueue.svg"
    InfoSettingIconPath = IconFolderPath.resolve() / "InfoSetting.svg"
    InfoIconPath = IconFolderPath.resolve() / "Info.svg"
    AboutIconPath = IconFolderPath.resolve() / "About.svg"
    NoMarkIconPath = IconFolderPath.resolve() / "NoMark.svg"
    RedDashIconPath = IconFolderPath.resolve() / "RedDash.svg"
    PlusIconPath = IconFolderPath.resolve() / "Plus.svg"
    TrashLightIconPath = IconFolderPath.resolve() / "Trash_Light.svg"
    TrashDarkIconPath = IconFolderPath.resolve() / "Trash_Dark.svg"
    RenameIconPath = IconFolderPath.resolve() / "Rename.png"
    SwitchIconPath = IconFolderPath.resolve() / "Switch.svg"
    QuestionIconPath = IconFolderPath.resolve() / "Question.svg"
    InfoBigIconPath = IconFolderPath.resolve() / "InfoBig.png"
    OkIconPath = IconFolderPath.resolve() / "Ok.png"
    PresetLightIconPath = IconFolderPath.resolve() / "Preset_Light.png"
    PresetDarkIconPath = IconFolderPath.resolve() / "Preset_Dark.png"
    SelectedItemIconPath = IconFolderPath.resolve() / "SelectedItemIcon.png"
    UnSelectedItemIconPath = IconFolderPath.resolve() / "UnSelectedItemIcon.png"
    EmptyIconPath = IconFolderPath.resolve() / "Empty.png"
    ErrorIconPath = IconFolderPath.resolve() / "Error.png"
    LeftArrowIconPath = IconFolderPath.resolve() / "LeftArrow.png"
    RightArrowIconPath = IconFolderPath.resolve() / "RightArrow.png"
    ErrorBigIconPath = IconFolderPath.resolve() / "ErrorBig.png"
    DonationsIconPath = IconFolderPath.resolve() / "Donations.png"
    ClearIconPath = IconFolderPath.resolve() / "Clear.svg"
    RefreshIconPath = IconFolderPath.resolve() / "Refresh.png"
    TopLightIconPath = IconFolderPath.resolve() / "Top_Light.svg"
    DownLightIconPath = IconFolderPath.resolve() / "Down_Light.svg"
    UpLightIconPath = IconFolderPath.resolve() / "Up_Light.svg"
    BottomLightIconPath = IconFolderPath.resolve() / "Bottom_Light.svg"
    TopDarkIconPath = IconFolderPath.resolve() / "Top_Dark.svg"
    DownDarkIconPath = IconFolderPath.resolve() / "Down_Dark.svg"
    UpDarkIconPath = IconFolderPath.resolve() / "Up_Dark.svg"
    BottomDarkIconPath = IconFolderPath.resolve() / "Bottom_Dark.svg"
    FolderIconPath = IconFolderPath.resolve() / "SelectFolder.svg"
    SpinnerIconPath = IconFolderPath.resolve() / "Spinner.gif"
    GoodJobIconPath = IconFolderPath.resolve() / "GoodJob.png"
    SettingIconPath = IconFolderPath.resolve() / "Setting.svg"
    TelegramIconPath = IconFolderPath.resolve() / "Telegram.svg"
    TwitterIconPath = IconFolderPath.resolve() / "Twitter.svg"
    ThemeIconPath = IconFolderPath.resolve() / "Day_And_Night.png"
    AppIconPath = IconFolderPath.resolve() / "App.ico"

    LanguagesFilePath = LanguagesFolderPath.resolve() / "iso639_language_list.json"
    AppLogFilePath = AppDataFolderPath.resolve() / "app_log.txt"
    MuxingLogFilePath = AppDataFolderPath.resolve() / "muxing_log_file.txt"
    TestMkvmergeFilePath = AppDataFolderPath.resolve() / "test_mkvmerge.txt"
    TestMkvpropeditFilePath = AppDataFolderPath.resolve() / "test_mkvpropedit.txt"
    mkvpropeditJsonJobFilePath = AppDataFolderPath.resolve() / "mkvpropeditJob.json"
    mkvmergeJsonJobFilePath = AppDataFolderPath.resolve() / "MkvmergeJob.json"
    mkvmergeJsonInfoFilePath = AppDataFolderPath.resolve() / "MkvmergeInfo.json"
    SettingJsonInfoFilePath = AppDataFolderPath.resolve() / "setting.json"

    TaskBarLibFilePath = DLLFolderPath.resolve() / "TaskbarLib.tlb"
    MKVPROPEDIT_PATH = get_program_from_path_and_tool("mkvpropedit")
    MKVMERGE_PATH = get_program_from_path_and_tool("mkvmerge")
    ENVIRONMENT = os.environ.copy()
    update_enviro_if_not_windows()
    MKVPROPEDIT_VERSION = get_mkvpropedit_version()
    MKVMERGE_VERSION = get_mkvmerge_version()
    if "mkvmerge" not in MKVMERGE_VERSION:
        logging.warning("Could not use system mkvmerge. Trying portable version...")
        if sys.platform == "win32":
            suffix = ".exe"
        else:
            suffix = ""
        mkvmerge = f"mkvmerge{suffix}"
        MKVMERGE_PATH = ToolsFolderPath.resolve() / mkvmerge
        MKVMERGE_VERSION = get_mkvmerge_version()
        if "mkvmerge" not in MKVMERGE_VERSION:
            MKVMERGE_VERSION = "mkvmerge: not found!"
            raise Exception("mkvmerge file! ")
        else:
            logging.info("mkvmerge OK")
    else:
        logging.info("mkvmerge OK")
    if "mkvpropedit" not in MKVPROPEDIT_VERSION:
        logging.warning("Could not use system mkvpropedit. Trying portable version...")
        if sys.platform == "win32":
            suffix = ".exe"
        else:
            suffix = ""
        mkvpropedit = f"mkvpropedit{suffix}"
        MKVPROPEDIT_PATH = ToolsFolderPath.resolve() / mkvpropedit
        MKVPROPEDIT_VERSION = get_mkvpropedit_version()
        if "mkvpropedit" not in MKVPROPEDIT_VERSION:
            MKVPROPEDIT_VERSION = "mkvpropedit: not found!"
            raise Exception("mkvpropedit file! ")
        else:
            logging.info("mkvpropedit OK")
    else:
        logging.info("mkvpropedit OK")
except Exception as e:
    logging.error(e)
    missing_files_message = MissingFilesMessage(error_message=str(e))
    missing_files_message.execute()
