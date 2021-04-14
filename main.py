# -*- coding: utf-8 -*-

# Importieren

import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from PyQt6 import uic
from pathlib import Path
from configparser import ConfigParser
import shutil
import time

# Variablen

homePath = os.path.dirname(__file__) # Ansonsten wird kein Icon angezeigt
logo_Pfad = os.path.join(homePath, 'Gui\\data\\Icon.png')
AppdataPath = os.getenv('APPDATA') + '/Nullpunkt Bscheißer/config'
AppdataPath = Path(AppdataPath)
configfile_pfad = Path(str(AppdataPath) + '/config.ini')

Planes = []
InfoTexte = []
text = []
EndcodeTXT = []
lastLineInFile = ""

NullpunktLBL = [" LBL ", " CALL LBL 50", " CYCL DEF 7.0 NULLPUNKT", " CYCL DEF 7.1  X+0", " CYCL DEF 7.2  Y+0", " CYCL DEF 7.3  Z+0", " LBL 0"]
EndcodeTXT = ["L Z+0 R0 FMAX M92 M9\n", "L X+0 Y+0 R0 FMAX M92\n", "STOP M36 M30\n", ";\n"]

# Funktionen Programmlogic

def removeNumbers(text):
    for i in range(len(text)):
        textOhneZahl = ""
        platzhalterliste = text[i].split(" ")
        for x in range(len(platzhalterliste)-1):
            if platzhalterliste[x].isdigit() == True:
                textOhneZahl = textOhneZahl + " " + platzhalterliste[x+1]
            else:
                textOhneZahl = textOhneZahl + " " + platzhalterliste[x+1]
            text[i] = textOhneZahl
    return text

def addNumbers(text):
    for i in range(len(text)):
        tempText = text[i]

        if tempText[:1] != " ":
            text[i] = str(i) + " " + text[i]
            if i <= 9:
                text[i] = "0" + text[i]
        else:
            text[i] = str(i) + text[i]
            if i <= 9:
                text[i] = "0" + text[i]
    return text

def addLBL(text, Planes, InfoTexte):
    ReadConfigfile()

    for i in range(len(Planes)):
        for x in range(len(text)):
            s=0
            if str(Planes[i]) == str(text[x-s]):
                LabelNummer = 50 + i
                text.insert(x+1," CALL LBL " + str(LabelNummer) + "\n")
                s=s+1

    for i in range(len(Planes)):
        number = 50 + i
        text.insert(len(text)-1, NullpunktLBL[0] + str(number) + " ; " + Planes[i])

        if cf_SchwenkTexte == "true":
            text.insert(len(text)-1, " ; " + InfoTexte[i])
        if number != 50:
            text.insert(len(text)-1, NullpunktLBL[1] + "\n")
        
        text.insert(len(text)-1, NullpunktLBL[2] + "\n")
        text.insert(len(text)-1, NullpunktLBL[3] + "\n")
        text.insert(len(text)-1, NullpunktLBL[4] + "\n")
        text.insert(len(text)-1, NullpunktLBL[5] + "\n")
        text.insert(len(text)-1, NullpunktLBL[6] + "\n")
        text.insert(len(text)-1, " ;" + "\n")

    return text

def findPlanes(text):
    planesVar = []
    infotext = []
    
    for i in range(len(text)):
        if "PLANE" in text[i]:
            planesVar.insert(len(planesVar), text[i])
            
            for x in range(5):
                if "SPATIAL" in text[i]:
                    if "Operation" in text[i+x]:
                        infotext.insert(len(infotext), text[i+x+1])
                    if "Operation" in text[i-x]:
                        infotext.insert(len(infotext), text[i-x+1])

    PlanesZwischenspeicher = []
    for i in planesVar:
        if i not in PlanesZwischenspeicher:
            PlanesZwischenspeicher.append(i)
    planesVar = PlanesZwischenspeicher

    for i in range(len(planesVar)):
        if "PLANE RESET TURN" in planesVar[i]:
            planesVar.pop(i)
    return planesVar, infotext   

def addEND(text):
    stop = 0
    while stop < 1:
        if "Z+0" in text[len(text)-2]:
            text.pop(len(text)-2)
            stop = 2
        else:
            text.pop(len(text)-2)
            stop = 0

    for x in range(len(EndcodeTXT)):
        EndcodeTXT[x] = EndcodeTXT[x].replace('\n', '')

    i = len(text)-1
    for x in range(len(EndcodeTXT)):
        w = x + i
        text.insert(w, " " + EndcodeTXT[x] + "\n")
    return text

def DateiSchreiben(DateiPfad, text):
    x = open(DateiPfad, 'w')
    for i in range(len(text)):
        x.writelines(text[i])

# GUIFunktionen

def ButtonSelectPath():
    ReadConfigfile()
    filepath = QFileDialog.getOpenFileName( None, 'Test Dialog', cf_PostOrdner, 'Heidenhain Programm(*.h*)')
    MainWindow.rawFilePath.setText(filepath[0])

def ButtonOpenEinstellungen():
    EinstellungenWindow.show()

def ProgressBar(Prozent):
    MainWindow.progressBar.setValue(Prozent)
    if Prozent == 100:
        MainWindow.LabelDone.setVisible(True)
    else:
            MainWindow.LabelDone.setVisible(False)

def ButtonStartEditFile():
    ReadConfigfile()
    text = []
    del text[:]

    DateiPfad = MainWindow.rawFilePath.text()
    if DateiPfad == "":
        ErrorWindow.ErrorText.setText("Bitte eine Datei selektieren!")
        ErrorWindow.show()
        return
    if ".H" in DateiPfad:
        pass
    elif ".h" in DateiPfad:
        pass
    else:
        ErrorWindow.ErrorText.setText("Bitte gib eine gültige Datei an. Endung = .h oder .H")
        ErrorWindow.show()
        return

    ProgressBar(10)
    Datei = open(DateiPfad, 'r')
    text = Datei.readlines()
    ProgressBar(20)
    Datei.close()

    for i in range(len(text)):
        if "CALL LBL 50" in text[i]:
            ProgressBar(0)
            del text[:]
            ErrorWindow.ErrorText.setText("Diese datei wurde bereits bearbeitet!!")
            ErrorWindow.show()
            return 

    text = removeNumbers(text)
    ProgressBar(30)
    if cf_Endcode == "true":
        text = addEND(text)
        ProgressBar(40)
    
    Planes = findPlanes(text)
    InfoTexte = Planes[1]
    InfoTexte.insert(0, "Nullpunkt zurücksetzen \n")
    Planes = Planes[0]
    ProgressBar(50)

    text = addLBL(text, Planes, InfoTexte)
    ProgressBar(60)

    if cf_withoutNumbers == "true":
        text = addNumbers(text)
    ProgressBar(70)

    DateiSchreiben(DateiPfad, text)
    ProgressBar(100)
    del Planes[:]
    del InfoTexte[:]
    del text[:]

def ClosseErrorWindow():
    ErrorWindow.close()

def BackToMainWindow():
    # Code ob sicher nicht speichern
    EinstellungenWindow.close()

# Config Funktionen -----------------------

def SaveEinstllungen(config_file):
    if EinstellungenWindow.EndcodHinzu.isChecked() == False:
        config.set('Einstellungen', 'Endcode', 'false')
    else:
        config.set('Einstellungen', 'Endcode', 'true')
    
    if EinstellungenWindow.SchwenkTexte.isChecked() == False:
        config.set('Einstellungen', 'SchwenkTexte', 'false')
    else:
        config.set('Einstellungen', 'SchwenkTexte', 'true')

    if EinstellungenWindow.withoutNumbers.isChecked() == False:
        config.set('Einstellungen', 'withoutNumbers', 'false')
    else:
        config.set('Einstellungen', 'withoutNumbers', 'true')
    
    if EinstellungenWindow.PostOrdner.text() == "":
        EinstellungenWindow.PostOrdner.setText(cf_PostOrdner)
        ErrorWindow.ErrorText.setText("Ausgabepfad darf nicht leer sein!")
        ErrorWindow.show()

    config.set('Pfade', 'PostOrdner', EinstellungenWindow.PostOrdner.text())
    
    with open(configfile_pfad, 'w') as configfile:
        config.write(configfile)
    EinstellungenWindow.close()

def CheckAndChangeEinstellungen():
    ReadConfigfile()
    if cf_Endcode == "false":
        EinstellungenWindow.EndcodHinzu.setChecked(False)
    if cf_SchwenkTexte == "false":
        EinstellungenWindow.SchwenkTexte.setChecked(False)
    if cf_withoutNumbers == "false":
        EinstellungenWindow.withoutNumbers.setChecked(False)
    if cf_PostOrdner == "":
        config.set('Pfade', 'PostOrdner', "C:/")
        ReadConfigfile()
        EinstellungenWindow.PostOrdner.setText(cf_PostOrdner)
    else:
        EinstellungenWindow.PostOrdner.setText(cf_PostOrdner)

def ReadConfigfile():
    # Initialisieren
    global cf_Endcode 
    global cf_SchwenkTexte
    global cf_withoutNumbers
    global cf_PostOrdner

    #  Zuweißen
    cf_Endcode = config['Einstellungen']['Endcode']
    cf_SchwenkTexte = config['Einstellungen']['SchwenkTexte']
    cf_withoutNumbers = config['Einstellungen']['withoutNumbers']
    cf_PostOrdner = config['Pfade']['PostOrdner'] 

# Abarbeitung Programm ---------------------------

# zuweißung der fenster
app = QApplication(sys.argv)
MainWindow = uic.loadUi("Gui/MainWindow.ui")
ErrorWindow = uic.loadUi("Gui/Error.ui")
EinstellungenWindow = uic.loadUi("Gui/EinstellungenWindow.ui")

# Abfragen zwegs config datei
if os.path.exists(AppdataPath) != True:
    os.makedirs(AppdataPath)
    shutil.copy('config/config.ini', str(AppdataPath))
if os.path.exists(configfile_pfad) != True:
    shutil.copy('config/config.ini', str(AppdataPath))

config = ConfigParser()
config.read(configfile_pfad)

# Zuweißung Icons
MainWindow.setWindowIcon(QIcon(logo_Pfad)) 
ErrorWindow.setWindowIcon(QIcon(logo_Pfad)) 
EinstellungenWindow.setWindowIcon(QIcon(logo_Pfad))

# Update nach Config
CheckAndChangeEinstellungen()

    # MainWindow Funktionen
MainWindow.LabelDone.setVisible(False) # Fertig text verstecken
MainWindow.btn_selectfile.clicked.connect(ButtonSelectPath) # Dateiauswahl

MainWindow.btn_ButtonStart.clicked.connect(ButtonStartEditFile) # Start verknüpfung
MainWindow.btn_Einstellungen.clicked.connect(ButtonOpenEinstellungen) # Einstellungen verknüpfung

    # Error Window Funktionen
ErrorWindow.ErrorOkButton.clicked.connect(ClosseErrorWindow) # Close Errow window

    # Einstellungen Funktionen
EinstellungenWindow.btn_backToMain.clicked.connect(BackToMainWindow) # Back to Main Menü
EinstellungenWindow.btn_SaveEinstllungen.clicked.connect(SaveEinstllungen) # Save and Back to Main menü

MainWindow.show() # main window öffnen
MainWindow.activateWindow()
sys.exit(app.exec()) # alles beenden
# Programm Ende
