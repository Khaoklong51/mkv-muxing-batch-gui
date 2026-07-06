import logging
import struct
import subprocess
import sys
from pathlib import Path
import os
from shutil import which

from PySide6.QtWidgets import QApplication

from packages.Widgets.MissingFilesMessage import MissingFilesMessage
from packages.Startup.Debug import USE_PG_PORTABLE


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
    else:
        app_data = home / ".local/share"
    my_app_data_folder = app_data / "MKV Muxing Batch GUI"
    try:
        my_app_data_folder.mkdir(exist_ok=True, parents=True)
    except Exception:
        pass
    return my_app_data_folder


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
        try:
            file_name.unlink(missing_ok=True)
        except OSError as e:
            logging.warning("Could not delete old media info file %s: %s", file_name, e)


script_path = Path(sys.argv[0])  # get path of the this file
script_folder = script_path.parent
resources_folder = script_folder.resolve() / "Resources"
FontFolderPath = resources_folder.resolve() / "Fonts"
IconFolderPath = resources_folder.resolve() / "Icons"
DLLFolderPath = resources_folder.resolve() / "DLL"
GlobalToolsFolderPath = resources_folder.resolve() / "Tools"
ToolsFolderPath = GlobalToolsFolderPath.resolve() / "Windowsx64"
LanguagesFolderPath = resources_folder.resolve() / "Languages"
LibFolderPath = Path()
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


def get_program_version(program_path: Path, program_name: str) -> str:
    def run_version(path: Path) -> str | None:
        try:
            result = subprocess.run(
                [str(path), "-V"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                env=ENVIRONMENT,
                text=True,
                check=True,
            )
            output = result.stdout.strip()
            logging.debug(output)
            if program_name in output:
                return output
        except (OSError, subprocess.CalledProcessError):
            return None
        return None

    # Try system path
    version = run_version(program_path)
    if version:
        logging.info(f"{program_path.stem} OK")
        return version

    # Try portable fallback
    logging.warning(
        f"Could not use system {program_path.stem}. Trying portable version..."
    )
    suffix = ".exe" if sys.platform == "win32" else ""
    fallback = ToolsFolderPath.resolve() / f"{program_path.stem}{suffix}"

    version = run_version(fallback)
    if version:
        logging.info(f"{fallback.stem} OK")
        return version

    # If both fail
    msg = f"Cannot use {program_path.stem} from system or portable path"
    logging.error(msg)
    raise RuntimeError(msg)


def get_custom_program_path(program: str, suffix: str) -> Path | None:
    executable_name = f"{program}{suffix}"
    for env_var in ("MKVTOOLNIX_PATH", "MKVTOOLNIX_DIR"):
        custom_path = os.environ.get(env_var)
        if not custom_path:
            continue
        custom_candidate = Path(custom_path).expanduser()
        if custom_candidate.is_dir():
            custom_candidate = custom_candidate / executable_name
        elif custom_candidate.name.lower() != executable_name.lower():
            logging.warning(
                "%s points to %s, not %s",
                env_var,
                custom_candidate,
                executable_name,
            )
            continue
        if custom_candidate.exists():
            return custom_candidate.resolve()
    return None


def get_nearby_program_path(program: str, suffix: str) -> Path | None:
    executable_name = f"{program}{suffix}"
    for folder_path in (script_folder.resolve(), script_folder.resolve().parent):
        candidate = folder_path / executable_name
        if candidate.exists():
            return candidate.resolve()
    return None


def get_program_path(program: str) -> Path:
    # Decide suffix
    suffix = ".exe" if sys.platform == "win32" else ""
    candidate = None

    if not USE_PG_PORTABLE:
        custom_candidate = get_custom_program_path(program, suffix)
        if custom_candidate:
            global Use_System_PG
            Use_System_PG = True
            return custom_candidate

        nearby_candidate = get_nearby_program_path(program, suffix)
        if nearby_candidate:
            Use_System_PG = True
            return nearby_candidate

    found = which(program)
    if found and not USE_PG_PORTABLE:
        Use_System_PG = True
        return Path(found).resolve()

    if sys.platform == "win32" and not USE_PG_PORTABLE:
        program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        pf_candidate = program_files / "MKVToolNix" / f"{program}{suffix}"
        if pf_candidate.exists():
            candidate = pf_candidate

    if not candidate or USE_PG_PORTABLE:
        if not USE_PG_PORTABLE:
            logging.warning(
                f"Could not find system {program}. Trying portable version..."
            )
        else:
            logging.warning("Force Use portable version")
        candidate = ToolsFolderPath.resolve() / f"{program}{suffix}"

    candidate = candidate.resolve()

    if not candidate.exists():
        logging.error(f"{program} not found in path, Program Files, or Tools folder!")
        raise FileNotFoundError(f"{program} not found!")

    return candidate


def update_enviro_if_not_windows():
    if "LD_LIBRARY_PATH" not in ENVIRONMENT.keys():
        ENVIRONMENT["LD_LIBRARY_PATH"] = ""
    if sys.platform != "win32" and not Use_System_PG:
        ENVIRONMENT["LD_LIBRARY_PATH"] = (
            f"{LibFolderPath.resolve()}:{ENVIRONMENT['LD_LIBRARY_PATH']}"
        )


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
    # not sure why logging set in main not work in here
    # this use to check mkvtoolnix tool
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
    Use_System_PG = False
    MKVPROPEDIT_PATH = get_program_path("mkvpropedit")
    MKVMERGE_PATH = get_program_path("mkvmerge")
    ENVIRONMENT = os.environ.copy()
    update_enviro_if_not_windows()
    MKVPROPEDIT_VERSION = get_program_version(MKVPROPEDIT_PATH, "mkvpropedit")
    MKVMERGE_VERSION = get_program_version(MKVMERGE_PATH, "mkvmerge")
except Exception as e:
    logging.error(e)
    if QApplication.instance() is not None:
        missing_files_message = MissingFilesMessage(error_message=str(e))
        missing_files_message.execute()
    raise SystemExit(1) from e
