# -*- coding: utf-8 -*-

# Importieren

from re import search

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6 import uic

# Variablen

Planes = []

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

def addLBL(text, Planes):
    for i in range(len(Planes)):
        for x in range(len(text)):
            s=0
            print(x)
            if str(Planes[i]) == str(text[x-s]):
                LabelNummer = 50 + i
                text.insert(x+1," CALL LBL " + str(LabelNummer) + "\n")
                s=s+1


    return text

def findPlanes(text, Planes):
    for i in range(len(text)):
        if search("PLANE", text[i]):
            Planes.insert(len(Planes), text[i])
    PlanesZwischenspeicher = []
    for i in Planes:
        if i not in PlanesZwischenspeicher:
            PlanesZwischenspeicher.append(i)
    Planes = PlanesZwischenspeicher

    for i in range(len(Planes)):
        if search("PLANE RESET TURN", Planes[i]):
            Planes.pop(i)
    return Planes      

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

# Abarbeitung Programm

app = QApplication(sys.argv)
w = uic.loadUi("Gui/MainWindow.ui")

w.show()

sys.exit(app.exec())

# DateiPfad = "test.h"

# Datei = open(DateiPfad, 'r')
# text = Datei.readlines()
# Datei.close()

# text = removeNumbers(text)
# Planes = findPlanes(text, Planes)
# text = addLBL(text, Planes)
# text = addEND(text)
# text = addNumbers(text)
# DateiSchreiben(DateiPfad, text)

# Programm Ende
