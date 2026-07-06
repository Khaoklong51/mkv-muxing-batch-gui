import json
import logging
from pathlib import Path
from PySide6.QtWidgets import QWidget
from packages.Startup.GlobalFiles import SettingJsonInfoFilePath
from packages.Widgets.SingleDefaultPresetsData import SingleDefaultPresetsData


def get_data_from_json(json_data, attribute, default_value):
    try:
        return json_data[attribute]
    except Exception:
        return default_value


def get_names_list_of_presets():
    names_list = []
    for preset in Options.DefaultPresets:
        names_list.append(preset.Preset_Name)
    return names_list


def ensure_valid_current_preset():
    if not Options.DefaultPresets:
        Options.DefaultPresets.append(SingleDefaultPresetsData())
    if not isinstance(Options.FavoritePresetId, int):
        Options.FavoritePresetId = 0
    if Options.FavoritePresetId < 0 or Options.FavoritePresetId >= len(
        Options.DefaultPresets
    ):
        Options.FavoritePresetId = 0
    Options.CurrentPreset = Options.DefaultPresets[Options.FavoritePresetId]


class Options(QWidget):
    DefaultPresets = [SingleDefaultPresetsData()]
    CurrentPreset = SingleDefaultPresetsData()
    FavoritePresetId = 0
    Dark_Mode = False
    Main_Window_Geometry = {}
    Main_Window_Maximized = False
    Attachment_Expert_Mode_Info_Message_Show = True
    Choose_Preset_On_Startup = False


def save_options():
    default_presets_data = []
    for preset_id in range(len(Options.DefaultPresets)):
        temp_default_preset = {
            "Preset_Name": Options.DefaultPresets[preset_id].Preset_Name,
            "Default_Video_Directory": Options.DefaultPresets[
                preset_id
            ].Default_Video_Directory,
            "Default_Video_Extensions": Options.DefaultPresets[
                preset_id
            ].Default_Video_Extensions,
            "Default_Subtitle_Directory": Options.DefaultPresets[
                preset_id
            ].Default_Subtitle_Directory,
            "Default_Subtitle_Extensions": Options.DefaultPresets[
                preset_id
            ].Default_Subtitle_Extensions,
            "Default_Subtitle_Language": Options.DefaultPresets[
                preset_id
            ].Default_Subtitle_Language,
            "Default_Audio_Directory": Options.DefaultPresets[
                preset_id
            ].Default_Audio_Directory,
            "Default_Audio_Extensions": Options.DefaultPresets[
                preset_id
            ].Default_Audio_Extensions,
            "Default_Audio_Language": Options.DefaultPresets[
                preset_id
            ].Default_Audio_Language,
            "Default_Chapter_Directory": Options.DefaultPresets[
                preset_id
            ].Default_Chapter_Directory,
            "Default_Chapter_Extensions": Options.DefaultPresets[
                preset_id
            ].Default_Chapter_Extensions,
            "Default_Attachment_Directory": Options.DefaultPresets[
                preset_id
            ].Default_Attachment_Directory,
            "Default_Destination_Directory": Options.DefaultPresets[
                preset_id
            ].Default_Destination_Directory,
            "Default_Favorite_Subtitle_Languages": Options.DefaultPresets[
                preset_id
            ].Default_Favorite_Subtitle_Languages,
            "Default_Favorite_Audio_Languages": Options.DefaultPresets[
                preset_id
            ].Default_Favorite_Audio_Languages,
        }
        default_presets_data.append(temp_default_preset)
    options_data = {
        "Presets": default_presets_data,
        "FavoritePresetId": Options.FavoritePresetId,
        "Dark_Mode": Options.Dark_Mode,
        "Main_Window_Geometry": Options.Main_Window_Geometry,
        "Main_Window_Maximized": Options.Main_Window_Maximized,
        "Attachment_Expert_Mode_Info_Message_Show": Options.Attachment_Expert_Mode_Info_Message_Show,
        "Choose_Preset_On_Startup": Options.Choose_Preset_On_Startup,
    }
    options_file_path = Path(SettingJsonInfoFilePath)
    try:
        with open(options_file_path, "w+", encoding="UTF-8") as option_file:
            json.dump(options_data, option_file, indent=4)
    except OSError as e:
        logging.warning("Could not save settings file: %s", e)


def read_option_file(option_file):
    option_file_path = Path(option_file)
    should_save_options = True
    if option_file_path.is_file():
        try:
            with open(option_file_path, "r", encoding="UTF-8") as option_file:
                data = json.load(option_file)
        except (OSError, json.JSONDecodeError) as e:
            logging.warning("Could not read settings file, using defaults: %s", e)
            should_save_options = False
        else:
            presets = get_data_from_json(
                json_data=data, attribute="Presets", default_value="Old"
            )
            if not isinstance(presets, list) or len(presets) == 0:
                presets = [{}]
            preset_number = len(presets)
            Options.DefaultPresets.clear()
            for preset_id in range(preset_number):
                preset_data = presets[preset_id]
                if not isinstance(preset_data, dict):
                    preset_data = {}
                temp_default_preset = SingleDefaultPresetsData()
                temp_default_preset.Preset_Name = get_data_from_json(
                    json_data=preset_data,
                    attribute="Preset_Name",
                    default_value=f"Preset #{preset_id + 1}",
                )
                temp_default_preset.Default_Video_Directory = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Video_Directory",
                    default_value="",
                )
                temp_default_preset.Default_Video_Extensions = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Video_Extensions",
                    default_value=["MKV"],
                )
                temp_default_preset.Default_Subtitle_Directory = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Subtitle_Directory",
                    default_value="",
                )
                temp_default_preset.Default_Subtitle_Extensions = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Subtitle_Extensions",
                    default_value=["ASS"],
                )
                temp_default_preset.Default_Subtitle_Language = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Subtitle_Language",
                    default_value="English",
                )
                temp_default_preset.Default_Audio_Directory = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Audio_Directory",
                    default_value="",
                )
                temp_default_preset.Default_Audio_Extensions = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Audio_Extensions",
                    default_value=["AAC"],
                )
                temp_default_preset.Default_Audio_Language = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Audio_Language",
                    default_value="English",
                )
                temp_default_preset.Default_Chapter_Directory = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Chapter_Directory",
                    default_value="",
                )
                temp_default_preset.Default_Chapter_Extensions = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Chapter_Extensions",
                    default_value=["XML"],
                )
                temp_default_preset.Default_Attachment_Directory = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Attachment_Directory",
                    default_value="",
                )
                temp_default_preset.Default_Destination_Directory = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Destination_Directory",
                    default_value="",
                )
                temp_default_preset.Default_Favorite_Subtitle_Languages = (
                    get_data_from_json(
                        json_data=preset_data,
                        attribute="Default_Favorite_Subtitle_Languages",
                        default_value=["English", "Arabic"],
                    )
                )
                temp_default_preset.Default_Favorite_Audio_Languages = get_data_from_json(
                    json_data=preset_data,
                    attribute="Default_Favorite_Audio_Languages",
                    default_value=["English", "Arabic"],
                )
                Options.DefaultPresets.append(temp_default_preset)
            Options.FavoritePresetId = get_data_from_json(
                json_data=data, attribute="FavoritePresetId", default_value=0
            )
            Options.Dark_Mode = get_data_from_json(
                json_data=data, attribute="Dark_Mode", default_value=False
            )
            Options.Main_Window_Geometry = get_data_from_json(
                json_data=data, attribute="Main_Window_Geometry", default_value={}
            )
            if not isinstance(Options.Main_Window_Geometry, dict):
                Options.Main_Window_Geometry = {}
            Options.Main_Window_Maximized = bool(
                get_data_from_json(
                    json_data=data,
                    attribute="Main_Window_Maximized",
                    default_value=False,
                )
            )
            Options.Attachment_Expert_Mode_Info_Message_Show = get_data_from_json(
                json_data=data,
                attribute="Attachment_Expert_Mode_Info_Message_Show",
                default_value=True,
            )
            Options.Choose_Preset_On_Startup = get_data_from_json(
                json_data=data, attribute="Choose_Preset_On_Startup", default_value=False
            )
    ensure_valid_current_preset()
    if should_save_options:
        save_options()
