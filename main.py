# Definition einer Node (Knoten) in einem Netzwerk
class Node:
    def __init__(self, id, name):
        self.id = id                # Eindeutige Knoten-ID
        self.root_id = id           # Aktuell bekannte Root-ID (initial eigene ID)
        self.name = name            # Name des Knotens (z.B. "A", "B", ...)
        self.cost = 0               # Aktueller Pfadkostenwert zum Root
        self.neighbors = []         # Liste von Nachbarn als Tupel (Node, Gewicht)
        self.received_messages = [] # Zwischenspeicher für empfangene Nachrichten
        self.used_neighbors = None  # Der Nachbar, über den die beste Route zum Root läuft

    # Fügt einen Nachbarn mit einem Gewicht hinzu
    def add_neighbor(self, neighbor_node, weight):
        self.neighbors.append((neighbor_node, weight))

    # Sendet eine Nachricht an alle Nachbarn mit eigener Root-ID und Kosten
    def send_message(self):
        for neighbor, weight in self.neighbors:
            neighbor.receive_message(self.root_id, self.cost, weight, self.id)

    # Empfängt eine Nachricht von einem Nachbarn und speichert sie zwischen
    def receive_message(self, root_id, cost, weight_to_neighbor, neighbor_id):
        self.received_messages.append((root_id, cost, weight_to_neighbor, neighbor_id))

    # Aktualisiert den Zustand basierend auf empfangenen Nachrichten
    def update_state(self):
        updated = False
        for root_id, cost, weight_to_neighbor, neighbor_id in self.received_messages:
            total_cost = cost + weight_to_neighbor  # Gesamtkosten über den Nachbarn
            # Fall 1: Neue Root-ID ist kleiner -> neue Root wählen
            if root_id < self.root_id:
                self.root_id = root_id
                self.cost = total_cost
                updated = True
                self.add_used_neighbor(neighbor_id)
            # Fall 2: Gleiches Root, aber niedrigere Kosten -> bessere Route wählen
            elif root_id == self.root_id and total_cost < self.cost:
                self.cost = total_cost
                updated = True
                self.add_used_neighbor(neighbor_id)
        # Nachrichten nach der Verarbeitung löschen
        self.received_messages.clear()
        return updated
    
    # Setzt den Nachbarn, über den die Route zum Root läuft
    def add_used_neighbor(self, node_id):
        for neighbor in self.neighbors:
            if neighbor[0].id == node_id:
                self.used_neighbors = neighbor[0]
                break
        

# Funktion zur Ausgabe des aktuellen Zustands aller Knoten
def print_out(all_nodes):
    for node in all_nodes:
        # Gibt den Namen des Knotens und seinen "benutzten Nachbarn" aus
        print(f"{node.name}->{node.used_neighbors.name if node.used_neighbors else 'Root'}")
        # Alternative Debug-Ausgaben:
        #print(f"Node {node.name}: Root={node.root_id}, Cost={node.cost}")
        #print(f"Used neighbor: {node.used_neighbors.name if node.used_neighbors else 'None'}")


# Erstellung der Knoten im Netzwerk
A = Node(5,"A")
B = Node(1,"B")
C = Node(3,"C")
D = Node(7,"D")
E = Node(6,"E")
F = Node(4,"F")

# Aufbau der Nachbarschaften mit Gewicht (bidirektional)
A.add_neighbor(B, 10); B.add_neighbor(A, 10)
A.add_neighbor(C, 10); C.add_neighbor(A, 10)
B.add_neighbor(D, 15); D.add_neighbor(B, 15)
B.add_neighbor(E, 10); E.add_neighbor(B, 10)
C.add_neighbor(D, 3);  D.add_neighbor(C, 3)
C.add_neighbor(E, 10); E.add_neighbor(C, 10)
D.add_neighbor(E, 2);  E.add_neighbor(D, 2)
D.add_neighbor(F, 10); F.add_neighbor(D, 10)
E.add_neighbor(F, 2);  F.add_neighbor(E, 2)

# Liste aller Knoten
all_nodes = [A, B, C, D, E, F]

# Simulationsschleife: Knoten senden Nachrichten und aktualisieren sich, bis Konvergenz
converged = False
rounds = 0
while not converged and rounds <= len(all_nodes):  # Schleife bis alle Knoten stabil sind
    rounds += 1
    converged = True
    # Phase 1: Sende Nachrichten an alle Nachbarn
    for node in all_nodes:
        node.send_message()
    # Phase 2: Aktualisiere Zustände basierend auf empfangenen Nachrichten
    for node in all_nodes:
        if node.update_state():
            converged = False  # Wenn irgendein Knoten aktualisiert wurde, noch nicht konvergiert

# Ausgabe der finalen Pfade zum Root
print_out(all_nodes)
