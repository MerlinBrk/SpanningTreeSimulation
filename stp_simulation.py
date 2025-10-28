import re

# -----------------------------------------------------------------------------
# Definition der Node-Klasse (Knoten im Netzwerk)
# -----------------------------------------------------------------------------
class Node:
    """
    Repräsentiert einen Knoten (Node) in einem Netzwerk.

    Attribute:
        id (int): Eindeutige ID des Knotens.
        name (str): Name des Knotens (z. B. 'A', 'B', ...).
        root_id (int): Aktuell bekannte Root-ID (initial eigene ID).
        cost (int): Aktuelle Pfadkosten zum Root-Knoten.
        next_hop (Node | None): Nachbar, über den der beste Pfad zum Root führt.
        neighbors (list): Liste direkter Nachbarn im Format (Node, Gewicht).
        received_messages (list): Temporärer Speicher für empfangene Nachrichten.
    """

    def __init__(self, id, name):
        """Initialisiert den Knoten mit ID, Name und Standardwerten."""
        self.id = id
        self.name = name
        self.root_id = id
        self.cost = 0
        self.next_hop = None
        self.neighbors = []
        self.received_messages = []

    def add_neighbor(self, neighbor_node, weight):
        """Fügt einen Nachbarn mit gegebenem Kantengewicht hinzu."""
        self.neighbors.append((neighbor_node, weight))

    def send_message(self):
        """Sendet die aktuelle Root-ID und Kosten an alle Nachbarn."""
        for neighbor, weight in self.neighbors:
            neighbor.receive_message(self.root_id, self.cost, weight, self.id)

    def receive_message(self, root_id, cost, weight_to_neighbor, neighbor_id):
        """Empfängt eine Nachricht eines Nachbarn und speichert sie temporär."""
        self.received_messages.append((root_id, cost, weight_to_neighbor, neighbor_id))

    def update_state(self):
        """
        Aktualisiert den Zustand des Knotens anhand der empfangenen Nachrichten.
        Gibt True zurück, wenn sich der Zustand geändert hat.
        """
        updated = False  # Flag, ob eine Änderung erfolgt ist

        # Jede empfangene Nachricht prüfen
        for root_id, cost, weight_to_neighbor, neighbor_id in self.received_messages:
            # Gesamtkosten über diesen Nachbarn berechnen
            total_cost = cost + weight_to_neighbor

            # -------------------------
            # Fall 1: Neue Root-ID kleiner → Root wechseln
            # -------------------------
            if root_id < self.root_id:
                self.root_id = root_id      # Neue Root-ID übernehmen
                self.cost = total_cost      # Kosten zum Root aktualisieren
                updated = True
                self.add_next_hop(neighbor_id)  # Next Hop setzen

            # -------------------------
            # Fall 2: Gleiche Root, aber geringere Kosten → Route verbessern
            # -------------------------
            elif root_id == self.root_id and total_cost < self.cost:
                self.cost = total_cost
                updated = True
                self.add_next_hop(neighbor_id)

            # -------------------------
            # Fall 3: Gleiche Root & Kosten, deterministische Wahl anhand Nachbar-ID
            # -------------------------
            elif root_id == self.root_id and total_cost == self.cost and neighbor_id < self.next_hop.id:
                updated = True
                self.add_next_hop(neighbor_id)

        # Nach der Verarbeitung alle Nachrichten löschen
        self.received_messages.clear()
        return updated

    def add_next_hop(self, node_id):
        """Setzt den Next Hop (Nachbar), über den die Route zum Root läuft."""
        for neighbor in self.neighbors:
            if neighbor[0].id == node_id:
                self.next_hop = neighbor[0]
                break


# -----------------------------------------------------------------------------
# Hilfsfunktion: Gibt den aktuellen Zustand aller Knoten aus
# -----------------------------------------------------------------------------
def print_out(all_nodes):
    """
    Gibt den Routing-Zustand aller Knoten aus.
    
    Format:
        Knotenname -> Name des nächsten Hops (oder 'Root' falls selbst Root)
    """
    for node in all_nodes:
        print(f"{node.name}->{node.next_hop.name if node.next_hop else 'Root'}")


# -----------------------------------------------------------------------------
# Funktion: Liest die Netzwerktopologie aus einer Datei ein
# -----------------------------------------------------------------------------
def read_topology_from_file(filename):
    """
    Liest eine Netzwerktopologie aus einer Datei im Format:
    
    Graph {
        A = 1;
        B = 2;
        C = 3;
        A-B: 4;
        B-C: 2;
        ...
    }

    Rückgabe:
        list: Liste aller Node-Objekte mit initialisierten Nachbarn.
    """
    nodes = {}
    edges = []
    in_graph = False

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Start des Graph-Blocks
            if line.startswith('Graph'):
                in_graph = True
                continue
            # Ende des Graph-Blocks
            elif line == '}':
                in_graph = False
                continue
            elif in_graph:
                # Knoten erkennen (z. B. "A = 1;")
                node_match = re.match(r'([A-Za-z])\s*=\s*(\d+);', line)
                if node_match:
                    node_name, node_id = node_match.groups()
                    nodes[node_name] = Node(int(node_id), node_name)
                    continue

                # Kante erkennen (z. B. "A-B: 4;")
                edge_match = re.match(r'([A-Za-z])\s*-\s*([A-Za-z])\s*:\s*(\d+);', line)
                if edge_match:
                    n1, n2, weight = edge_match.groups()
                    edges.append((n1, n2, int(weight)))
                    continue

    # Nachbarn für alle Knoten hinzufügen (bidirektional)
    for n1, n2, weight in edges:
        nodes[n1].add_neighbor(nodes[n2], weight)
        nodes[n2].add_neighbor(nodes[n1], weight)

    return list(nodes.values())


# -----------------------------------------------------------------------------
# Simulation des Spanning Tree Protocol (STP)
# -----------------------------------------------------------------------------
def stp_protocol(all_nodes):
    """
    Simuliert das Spanning Tree Protocol.
    
    Ablauf:
        1. Jeder Knoten sendet seine Root-ID und Kosten an alle Nachbarn.
        2. Jeder Knoten aktualisiert seinen Zustand anhand der empfangenen Nachrichten.
        3. Wiederholen bis alle Knoten stabil sind (Konvergenz erreicht).
    """
    converged = False
    rounds = 0

    while not converged and rounds <= len(all_nodes):
        rounds += 1
        converged = True

        # Phase 1: Nachrichten senden
        for node in all_nodes:
            node.send_message()

        # Phase 2: Nachrichten verarbeiten
        for node in all_nodes:
            if node.update_state():
                converged = False


# -----------------------------------------------------------------------------
# Hauptprogramm
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Topologie aus Datei einlesen
    all_nodes = read_topology_from_file('input.txt')

    # Simulation starten
    stp_protocol(all_nodes)

    # Ergebnis ausgeben
    print_out(all_nodes)
