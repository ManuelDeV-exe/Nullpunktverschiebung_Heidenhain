# -*- coding: utf-8 -*-

# Importieren

from re import search

import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from PyQt6 import uic

# Variablen

Planes = []
InfoTexte = []

NullpunktLBL = [" LBL ", " CALL LBL 50", " CYCL DEF 7.0 NULLPUNKT", " CYCL DEF 7.1  X+0", " CYCL DEF 7.1  Y+0", " CYCL DEF 7.1  Z+0", " LBL 0"]

# Funktionen

def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

def removeNumbers(text):
    wiederholungen = len(text)
    for i in range(wiederholungen):
        textOhneZahl = ""
        platzhalter = text[i].split(" ")
        if platzhalter[0] == " ":
            return text
        for x in range(len(platzhalter)-1):
            x = x + 1
            textOhneZahl = textOhneZahl + " " + platzhalter[x]
        text[i] = textOhneZahl
    return text

def addNumbers(text):
    for i in range(len(text)):
        text[i] = str(i) + text[i]
        if i <= 9:
            text[i] = "0" + text[i]
    return text

def addLBL(text, Planes, InfoTexte):
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
        text.insert(len(text)-1, " ; " + InfoTexte[i])
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
        if search("PLANE", text[i]):
            planesVar.insert(len(planesVar), text[i])
            
            for x in range(5):
                if search("SPATIAL", text[i]):
                    if search("Operation", text[i+x]):
                        infotext.insert(len(infotext), text[i+x+1])
                    if search("Operation", text[i-x]):
                        infotext.insert(len(infotext), text[i-x+1])

    PlanesZwischenspeicher = []
    for i in planesVar:
        if i not in PlanesZwischenspeicher:
            PlanesZwischenspeicher.append(i)
    planesVar = PlanesZwischenspeicher

    for i in range(len(planesVar)):
        if search("PLANE RESET TURN", planesVar[i]):
            planesVar.pop(i)
    return planesVar, infotext   

def addEND(text):
    Endcode = open("Endcode.h", 'r')
    Endcode = Endcode.readlines()
    lenEndcode = len(Endcode)-1
    Endcode[lenEndcode] = Endcode[lenEndcode] + "\n"
    text.pop(len(text)-2)
    text.pop(len(text)-2)
    text.pop(len(text)-2)
    text.pop(len(text)-2)
    i = len(text)-1
    for x in range(len(Endcode)):
        w = x + i
        Endcode[x] = " " + Endcode[x]
        text.insert(w, Endcode[x])
    return text

def DateiSchreiben(DateiPfad, text):
    x = open(DateiPfad, 'w')
    for i in range(len(text)):
        x.writelines(text[i])

# GUIFunktionen

def ButtonSelectPath():
    filepath = QFileDialog.getOpenFileName()
    w.rawFilePath.setText(filepath[0])

def ProgressBar(Prozent):
    w.progressBar.setValue(Prozent)

def ButtonStartEditFile():
    DateiPfad = w.rawFilePath.text()
    if DateiPfad == "":
        e.ErrorText.setText("Bitte eine Datei selektieren!")
        e.show()
        return
    ProgressBar(10)
    Datei = open(DateiPfad, 'r')
    text = Datei.readlines()
    ProgressBar(20)
    Datei.close()

    text = removeNumbers(text)
    ProgressBar(30)
    text = addEND(text)
    ProgressBar(40)
    Planes = findPlanes(text)
    InfoTexte = Planes[1]
    InfoTexte.insert(0, "Nullpunkt zurücksetzen")
    Planes = Planes[0]
    ProgressBar(50)
    text = addLBL(text, Planes, InfoTexte)
    ProgressBar(60)
    text = addNumbers(text)
    ProgressBar(70)
    DateiSchreiben(DateiPfad, text)
    ProgressBar(100)

    w.LabelDone.setVisible(True)

def ClosseErrorWindow():
    e.close()

# Resource Dateien

resource_path('Gui/Einstellungen.ui')
resource_path('Gui/Error.ui')
resource_path('Gui/Icons.ui')
resource_path('Gui/MainWindow.ui')
resource_path('Gui/data/favicon.ico')
resource_path('Gui/data/Icon.jpg')


# Abarbeitung Programm

app = QApplication(sys.argv)
w = uic.loadUi("Gui/MainWindow.ui")
e = uic.loadUi("Gui/Error.ui")

w.LabelDone.setVisible(False)
w.selectfile_Rawfile.clicked.connect(ButtonSelectPath)
w.ButtonStartEdit.clicked.connect(ButtonStartEditFile)

e.ErrorOkButton.clicked.connect(ClosseErrorWindow)

w.show()
sys.exit(app.exec())

# Programm Ende
