import numpy as np
import random
from welt import welt, AKTIONEN, FLAGGE, schritt, zeige

# ---------------------------------------------------------
# Einstellungen (hier kannst du später herumprobieren)
# ---------------------------------------------------------
START = (1, 1)       # Startposition der Figur
alpha = 0.1          # Lernrate: wie stark eine Erfahrung eine Zahl ändert
gamma = 0.9          # Zukunftsfaktor: wie viel das nächste Feld zählt
epsilon = 0.2        # Anteil Erkunden (zufällige Aktion)

eingabe = input("Wie viele Episoden (Enter = 500): ")
episoden = int(eingabe) if eingabe else 500              # leerer Text zählt als "falsch"
eingabe = input("Maximale Schritte pro Episode (Enter = 200): ")
max_schritte = int(eingabe) if eingabe else 200

AKTIONSNAMEN = list(AKTIONEN)    # ["hoch", "runter", "links", "rechts"]


# ---------------------------------------------------------
# Aktion wählen: Erkunden oder Ausnutzen
# ---------------------------------------------------------
def waehle_aktion(q, figur, epsilon):
    if random.random() < epsilon:
        return random.randrange(len(AKTIONSNAMEN))       # Erkunden: zufällige Richtung
    werte = q[figur]                                     # die 4 Zahlen dieses Feldes
    beste = np.flatnonzero(werte == np.max(werte))       # alle Positionen mit dem Höchstwert
    return int(random.choice(beste))                     # Ausnutzen (bei Gleichstand zufällig)


# ---------------------------------------------------------
# Ein Schritt in der Welt: neue Position, Belohnung, Episodenende
# ---------------------------------------------------------
def umgebungs_schritt(welt, figur, aktion_nr):
    neu = schritt(welt, figur, AKTIONSNAMEN[aktion_nr])  # Nummer -> Name -> Bewegung
    if welt[neu] == FLAGGE:
        return neu, 1.0, True       # neue Position, Belohnung, Episode zu Ende
    return neu, 0.0, False


# ---------------------------------------------------------
# Training
# ---------------------------------------------------------
q = np.zeros((welt.shape[0], welt.shape[1], len(AKTIONSNAMEN)))   # frischer Spickzettel

for episode in range(episoden):
    figur = START
    for s in range(max_schritte):
        a = waehle_aktion(q, figur, epsilon)
        neu, belohnung, fertig = umgebungs_schritt(welt, figur, a)

        z, sp = figur
        if fertig:
            ziel = belohnung                                  # Episode zu Ende: nur Belohnung
        else:
            ziel = belohnung + gamma * np.max(q[neu])         # Belohnung + Ausblick aufs nächste Feld
        q[z, sp, a] += alpha * (ziel - q[z, sp, a])           # Zahl ein Stück korrigieren

        figur = neu
        if fertig:
            break

    if episode % 50 == 0:
        print("Episode", episode, "-> Schritte:", s + 1)


# ---------------------------------------------------------
# Test: nur noch Ausnutzen (epsilon = 0), 100 Versuche
# ---------------------------------------------------------
erfolge = 0
laengen = []
for _ in range(100):
    figur = START
    for s in range(max_schritte):
        a = waehle_aktion(q, figur, 0.0)
        figur, belohnung, fertig = umgebungs_schritt(welt, figur, a)
        if fertig:
            erfolge += 1
            laengen.append(s + 1)
            break

print("Erfolge:", erfolge, "von 100")
if laengen:
    print("Kürzester Weg:", min(laengen), "Schritte, Durchschnitt:", sum(laengen) / len(laengen))
print("Zum Vergleich: der kürzeste mögliche Weg sind 8 Schritte")


# ---------------------------------------------------------
# Vorführ-Episode: kein Zufall mehr, nur der Spickzettel
# ---------------------------------------------------------
print("\nVorführ-Episode (epsilon = 0):")
figur = START
geschafft = False
zeige(welt, figur)

for s in range(max_schritte):
    a = waehle_aktion(q, figur, 0.0)                         # epsilon 0 = nur Ausnutzen
    figur, belohnung, fertig = umgebungs_schritt(welt, figur, a)
    print("\nSchritt", s + 1, ":", AKTIONSNAMEN[a])
    zeige(welt, figur)
    if fertig:
        geschafft = True
        break

if geschafft:
    print("\nFlagge erreicht nach", s + 1, "Schritten!")
else:
    print("\nLimit von", max_schritte, "Schritten erreicht, keine Flagge.")