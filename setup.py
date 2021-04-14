import sys
import os
from cx_Freeze import setup, Executable

# Build Optionen
build_exe_options = dict(packages = ["configparser", "pathlib", "PyQt6", "sys", "os", "shutil", "time"], excludes = [], include_files = ["Gui/","config/"])

# Ziel
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="Gui/data/favicon.ico"
)

# Setup CX Freez
setup( 
    name = "Nullpunkt Bscheißer",
    version = "1.1",
    description = "Nullpunkt Bscheißer für Heidenhain Programme",
    author= "Manuel Bücherl",
    options = {'build_exe' : build_exe_options},
    executables = [target]
    )