from re import search


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

def addLBL(text):
    for i in range(len(text)):
        if search("PLANE RESET TURN FMAX", text[i]):
            text.insert(i+1," CALL LBL 50 \n")
        #if search("PLANE RESET TURN FMAX", text[i]):
        #    text.insert(i+1," CALL LBL 50 \n")
        #if search("PLANE RESET TURN FMAX", text[i]):
        #    text.insert(i+1," CALL LBL 50 \n")
    return text

def addEND(text):
    i = len(text)-1
    Endcode = open("Endcode.h", 'r')
    Endcode = Endcode.readlines()
    lenEndcode = len(Endcode)-1
    Endcode[lenEndcode] = Endcode[lenEndcode] + "\n"
    for x in range(len(Endcode)):
        w = x + i
        Endcode[x] = " " + Endcode[x]
        text.insert(w, Endcode[x])
    return text

def DateiSchreiben(DateiPfad, text):
    x = open(DateiPfad, 'w')
    for i in range(len(text)):
        x.writelines(text[i])

DateiPfad = "test.h"

Datei = open(DateiPfad, 'r')
text = Datei.readlines()
Datei.close()

text = removeNumbers(text)
text = addLBL(text)
text = addEND(text)
text = addNumbers(text)
DateiSchreiben(DateiPfad, text)