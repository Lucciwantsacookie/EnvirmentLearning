import numpy as np


# Blocktypen (Kodierung)
WEG = 0
WAND = 1
FLAGGE = 2

# Raster 6 Zeilen x 8 Spalten, zuerst alles Weg
welt = np.zeros((6, 8), dtype=int)

# Rand aus Wänden
welt[0, :] = WAND    # oberste Zeile
welt[-1, :] = WAND   # unterste Zeile
welt[:, 0] = WAND    # linke Spalte
welt[:, -1] = WAND   # rechte Spalte

# Flagge setzen
welt[4, 6] = FLAGGE



# Figur: Position als (zeile, spalte)
figur = (1, 1)
#if Laufzahl == "":
 #   Laufzahl = 200
 #   Durchgang = (0)

    

    # Zuordnung Blocktyp -> Zeichen (ein "Dictionary", also ein Wörterbuch)
SYMBOLE = {WEG: ".", WAND: "#", FLAGGE: "F"}

def zeige(welt, figur):
    for z in range(welt.shape[0]):        # shape[0] = Anzahl Zeilen
        text = ""
        for s in range(welt.shape[1]):    # shape[1] = Anzahl Spalten
            if (z, s) == figur:
                text += "A"               # A = Agent (unsere Figur)
            else:
                text += SYMBOLE[welt[z, s]]
        print(text)        
            

    

    # Aktion -> Veränderung von (zeile, spalte)
AKTIONEN = {
        "hoch":   (-1, 0),
        "runter": (1, 0),
        "links":  (0, -1),
        "rechts": (0, 1),
    }

def schritt(welt, figur, aktion):
        dz, ds = AKTIONEN[aktion]
        neu = (figur[0] + dz, figur[1] + ds)
        if welt[neu] == WAND:
            return figur      # Wand: Figur bleibt stehen
        return neu            # sonst: neue Position



eingabe = input("Maximale Schritte pro Episode (Enter = 200): ")
max_schritte = int(eingabe) if eingabe else 200   # leerer Text zählt als "falsch"

figur = (1, 1)
gefunden = False

for durchgang in range(1, max_schritte + 1):

    if welt[figur] == FLAGGE:
        gefunden = True
        break                                # Episode endet an der Flagge

zeige(welt, figur)
if gefunden:
    print("Flagge gefunden nach", durchgang, "Schritten!")
else:
    print("Limit von", max_schritte, "Schritten erreicht, keine Flagge.")





 




