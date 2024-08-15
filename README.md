Dieses Programm ermöglicht das Erstellen und Verwalten von digitalen Karteikarten. Es unterstützt das Hinzufügen neuer Karten, das Lernen der Karten in einem bestimmten Deck sowie das Filtern und Sortieren der Karten nach verschiedenen Kriterien.

Hauptfunktionen des Programms:
1. Karten hinzufügen (`--add`)
2. Lernen starten (`--learn`)
3. Karten anzeigen (`--list`)

**Karten hinzufügen (`--add`)**
Diese Funktion erlaubt das Hinzufügen von neuen Karteikarten zu einem bestimmten Deck. Der Benutzer wird aufgefordert, die Vorderseite und Rückseite der Karte einzugeben. Nach jeder hinzugefügten Karte wird gefragt, ob eine weitere Karte hinzugefügt werden soll. Der Benutzer kann das Hinzufügen jederzeit durch Eingabe von `q` abbrechen.

**Lernen starten (`--learn`)**
Diese Funktion startet eine Lernsession mit den Karten eines bestimmten Decks. Der Benutzer wird die Vorderseite der Karte angezeigt und kann durch Drücken der Enter-Taste die Rückseite aufdecken. Danach wird der Benutzer gefragt, ob er die Antwort wusste (mit den Optionen `j`, `n` oder Angabe des Levels). Basierend auf der Antwort wird der Schwierigkeitsgrad (Level) der Karte angepasst.

**Karten anzeigen (`--list`)**
Mit dieser Funktion können alle Karten eines Decks angezeigt werden. Der Benutzer kann wählen, ob er nur die Vorderseite oder auch die Rückseite der Karten sehen möchte. Auch hier kann das Programm durch Eingabe von `q` jederzeit beendet werden.

**Filter- und Sortieroptionen**
Das Programm bietet verschiedene Möglichkeiten, die Karten nach bestimmten Kriterien zu filtern oder zu sortieren.

**Filteroptionen:**
- `-l0`: Zeigt nur Karten mit Level 0 (noch nie wiederholt).
- `-l1`, `-l2`, `-l3`, `-l4`, `-l5`: Filtert Karten nach ihrem Level.
- `-lg`: Filtert Karten mit Level größer als eine bestimmte Zahl.
- `-lk`: Filtert Karten mit Level kleiner als eine bestimmte Zahl.
- `-wk`: Filtert Karten, die nach einem bestimmten Zeitpunkt wiederholt wurden.
- `-wg`: Filtert Karten, die vor einem bestimmten Zeitpunkt wiederholt wurden.
- `-ck`: Filtert Karten, die nach einem bestimmten Zeitpunkt erstellt wurden.
- `-cg`: Filtert Karten, die vor einem bestimmten Zeitpunkt erstellt wurden.
- `-id`: Filtert Karten nach einer oder mehreren spezifischen IDs.

**Sortieroptionen:**
- `-swauf`: Sortiert Karten nach Wiederholung aufsteigend.
- `-swab`: Sortiert Karten nach Wiederholung absteigend.
- `-scauf`: Sortiert Karten nach Erstellungsdatum aufsteigend.
- `-scab`: Sortiert Karten nach Erstellungsdatum absteigend.
- `-saauf`: Sortiert Karten alphabetisch nach der Vorderseite aufsteigend.
- `-saab`: Sortiert Karten alphabetisch nach der Vorderseite absteigend.
- `-r`: Mischt die Karten zufällig.

**Bedienung des Programms**
Das Programm wird durch die Eingabe verschiedener Befehle über die Kommandozeile gesteuert. Der Benutzer kann eine oder mehrere Optionen gleichzeitig verwenden, um das gewünschte Verhalten zu erzielen. Alle Eingaben des Benutzers werden in Kleinschreibung und ohne führende oder nachfolgende Leerzeichen erwartet. Die Eingabe von `q` beendet das Programm jederzeit sofort. 

Beispielaufrufe:
- `python programm.py --add deck1`: Fügt neue Karten zu "deck1" hinzu.
- `python programm.py --learn deck1 -l2`: Startet eine Lernsession mit Karten aus "deck1", die Level 2 haben.
- `python programm.py --list deck1 -saauf --back`: Zeigt alle Karten aus "deck1" sortiert nach der Vorderseite aufsteigend an, inklusive der Rückseite.

Das Programm speichert die Decks als JSON-Dateien, sodass sie einfach geladen, bearbeitet und gespeichert werden können. Es erwartet, dass alle Dateien im gleichen Verzeichnis wie das Skript gespeichert werden. Das Programm nutzt die Standardbibliotheken von Python und benötigt keine zusätzlichen Abhängigkeiten.
