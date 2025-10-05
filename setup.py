import cx_Freeze
from packages.Startup.Version import Version
import sys
from pathlib import Path

icon_suffix = ".png"
program_suffix = ""
if sys.platform == "win32":
    system = "Windows64"
    program_suffix = ".exe"
    icon_suffix = ".ico"
elif sys.platform == "linux":
    system = "Linux"
else:
    system = "Other Systems"

# --- Included Files Configuration ---
include_files = [
    [
        "Resources/Languages/iso639_language_list.json",
        "Resources/Languages/iso639_language_list.json",
    ],
    ["Resources/Icons/", "Resources/Icons/"],
    ["Resources/Fonts/OpenSans.ttf", "Resources/Fonts/OpenSans.ttf"],
]

# Dynamically include mkvtoolnix binaries if they exist for the target system
for tool in ["mkvmerge", "mkvpropedit"]:
    src = f"Resources/Tools/{system}/{tool}{program_suffix}"
    dst = f"Tools/{system}/{tool}{program_suffix}"
    if Path(src).exists():
        include_files.append([src, dst])

build_exe_options = {
    "include_files": include_files,
    "zip_include_packages": [
        "PySide6",
        "psutil",
        "comtypes",
    ],
    "optimize": 2,
}


cx_Freeze.setup(
    name="mkv-muxing-batch-gui",
    version=Version,
    description="Batch gui program to mux mkv files",
    options={
        "build_exe": build_exe_options,
    },
    executables=[
        {
            "script": "main.py",
            "base": "gui",
            "icon": f"Resources/Icons/App{icon_suffix}",
            "copyright": "Copyright (c) Khaoklong51",
            "target_name": "mkv-muxing-batch-gui",
        }
    ],
)
