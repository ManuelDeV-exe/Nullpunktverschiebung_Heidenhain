import sys
import os
from cx_Freeze import setup, Executable

# Dateien 
files = ['Gui/', 'Endcode.h']

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
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    )