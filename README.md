# SpanningTreeSimulation
Simulation of a Spanning Tree Protocol

## Übersicht

Dieses Python-Programm simuliert das **Spanning Tree Protocol (STP)**, das in Computernetzwerken eingesetzt wird, um Schleifen zu vermeiden und einen logischen, schleifenfreien Baum (Spanning Tree) aus einem vermaschten Netzwerk zu bilden.

Jeder **Knoten (Node)** repräsentiert dabei einen Switch, und jede **Kante (Edge)** eine Netzwerkverbindung mit einem bestimmten Gewicht (Kosten). Das Ziel der Simulation ist es, den Root-Switch (mit der kleinsten ID) und die jeweils besten Pfade zu ihm zu bestimmen.

---

## Hauptbestandteile

### 1. Klasse `Node`

Die Klasse `Node` modelliert einen Netzwerkknoten mit folgenden Attributen:

* **id** – eindeutige numerische ID des Knotens
* **name** – symbolischer Name (z. B. "A", "B", "C")
* **root_id** – aktuell bekannte Root-ID (initial die eigene ID)
* **cost** – aktuelle Kosten bis zum Root
* **next_hop** – der Nachbar, über den der beste Pfad zum Root führt
* **neighbors** – Liste der Nachbarn als Tupel *(Node, Gewicht)*
* **received_messages** – Puffer für empfangene Nachrichten

#### Wichtige Methoden:

* **`add_neighbor(neighbor_node, weight)`**
  Fügt eine bidirektionale Verbindung zu einem Nachbarn mit gegebenem Gewicht hinzu.

* **`send_message()`**
  Sendet die aktuelle Root-ID und die Kosten an alle Nachbarn.

* **`receive_message(root_id, cost, weight, neighbor_id)`**
  Speichert eingehende Informationen von Nachbarn zwischen.

* **`update_state()`**
  Vergleicht empfangene Nachrichten mit dem aktuellen Zustand:

  * Wenn ein kleinerer `root_id` erkannt wird, wird ein neuer Root gewählt.
  * Wenn derselbe Root, aber geringere Kosten entdeckt werden, wird der Pfad angepasst.
  * Bei gleichen Kosten wird (zur Stabilität) der Nachbar mit kleinerer ID bevorzugt.

  Gibt `True` zurück, wenn sich der Zustand des Knotens geändert hat.

* **`add_used_neighbor(node_id)`**
  Setzt den Nachbarn, über den aktuell die beste Route zum Root läuft.

---

### 2. Funktion `stp_protocol(all_nodes)`

Steuert den Simulationsablauf des STP:

1. Jeder Knoten sendet seine Nachricht an alle Nachbarn.
2. Alle Knoten aktualisieren ihren Zustand basierend auf empfangenen Nachrichten.
3. Wiederholung, bis kein Knoten mehr eine Änderung vornimmt (Konvergenz).

---

### 3. Funktion `print_out(all_nodes)`

Gibt für jeden Knoten aus, über welchen Nachbarn er den Root erreicht:

```
A->Root
B->A
C->B
```

---

### 4. Eingabedatei `input.txt`

Die Netzwerktopologie wird aus einer Datei eingelesen.
Beispiel:

```
Graph {
A = 1;
B = 2;
C = 3;
A-B: 2;
B-C: 1;
}
```

Knoten werden über `A = 1;` definiert, Verbindungen über `A-B: 2;`.

---

## Ablauf der Simulation

1. **Einlesen der Topologie** aus der Datei
2. **Erstellen aller Knoten und Kanten**
3. **Start der STP-Simulation** mit `stp_protocol(all_nodes)`
4. **Ausgabe** des stabilen Spanning Trees über `print_out(all_nodes)`

---

## Beispielausgabe

```
A->Root
B->A
C->B
```

→ Knoten A ist der Root; B und C verbinden sich über den jeweils kostengünstigsten Pfad.

---

## Zweck

Dieses Programm dient zum **Verständnis und zur Visualisierung des STP-Mechanismus**:

* Es zeigt, wie sich Knoten gegenseitig Informationen über den Root und die Pfadkosten austauschen.
* Es demonstriert den Prozess der **Konvergenz zu einem stabilen, schleifenfreien Netzwerkbaum**.
