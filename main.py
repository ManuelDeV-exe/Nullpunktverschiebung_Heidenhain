# -*- coding: utf-8 -*-

# Importieren

from re import search

import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from PyQt6 import uic

# Variablen

Planes = []
InfoTexte = []

amEndeEntfernen = 6

NullpunktLBL = [" LBL ", " CALL LBL 50", " CYCL DEF 7.0 NULLPUNKT", " CYCL DEF 7.1  X+0", " CYCL DEF 7.2  Y+0", " CYCL DEF 7.3  Z+0", " LBL 0"]
EndcodeTXT = [" L Z+0 R0 FMAX M92 M9", " L X+0 Y+0 R0 FMAX M92", " STOP M36 M30", " ;"]


# Funktionen

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

    for i in range(amEndeEntfernen):
        text.pop(len(text)-2)

    i = len(text)-1
    for x in range(len(EndcodeTXT)):
        w = x + i
        EndcodeTXT[x] = " " + EndcodeTXT[x] + "\n"
        text.insert(w, EndcodeTXT[x])
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
    if search(".H", DateiPfad):
        pass
    elif search(".h", DateiPfad):
        pass
    else:
        e.ErrorText.setText("Bitte gib eine gültige Datei an. Endung = .h oder .H")
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
    InfoTexte.insert(0, "Nullpunkt zurücksetzen \n")
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

# Abarbeitung Programm

app = QApplication(sys.argv)
w = uic.loadUi("Gui/MainWindow.ui")
e = uic.loadUi("Gui/Error.ui")

w.setWindowIcon(QIcon('Gui/data/favicon.ico')) 
e.setWindowIcon(QIcon('Gui/data/favicon.ico')) 

w.LabelDone.setVisible(False)
w.selectfile_Rawfile.clicked.connect(ButtonSelectPath)
w.ButtonStartEdit.clicked.connect(ButtonStartEditFile)

e.ErrorOkButton.clicked.connect(ClosseErrorWindow)

w.show()
sys.exit(app.exec())

# Programm Ende
