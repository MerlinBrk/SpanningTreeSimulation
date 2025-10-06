# Definition einer Node (Knoten) in einem Netzwerk
class Node:
    def __init__(self, id, name):
        self.id = id                # Eindeutige Knoten-ID
        self.name = name            # Name des Knotens (z.B. "A", "B", ...)

        self.root_id = id           # Aktuell bekannte Root-ID (initial eigene ID)
        self.cost = 0               # Aktueller Pfadkostenwert zum Root
        self.next_hop = None  # Der Nachbar, über den die beste Route zum Root läuft

        self.neighbors = []         # Liste von Nachbarn als Tupel (Node, Gewicht)
        self.received_messages = [] # Zwischenspeicher für empfangene Nachrichten

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
            elif root_id == self.root_id and total_cost == self.cost and neighbor_id < self.next_hop.id:
                updated = True
                self.add_used_neighbor(neighbor_id);
        # Nachrichten nach der Verarbeitung löschen
        self.received_messages.clear()
        return updated

    # Setzt den Nachbarn, über den die Route zum Root läuft
    def add_used_neighbor(self, node_id):
        for neighbor in self.neighbors:
            if neighbor[0].id == node_id:
                self.next_hop = neighbor[0]
                break
        

# Funktion zur Ausgabe des aktuellen Zustands aller Knoten
def print_out(all_nodes):
    for node in all_nodes:
        # Gibt den Namen des Knotens und seinen "benutzten Nachbarn" aus
        print(f"{node.name}->{node.next_hop.name if node.next_hop else 'Root'}")
        # Alternative Debug-Ausgaben:
        #print(f"Node {node.name}: Root={node.root_id}, Cost={node.cost}")
        #print(f"Used neighbor: {node.next_hop.name if node.next_hop else 'None'}")

# Hauptfunktion zur Simulation des Spanning Tree Protocols
def stp_protocol(all_nodes):
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



nodes = {}
edges = []

with open('input.txt', 'r') as f:
    in_graph = False
    for line in f:
        line = line.strip()
        if line.startswith('Graph'):
            in_graph = True
        elif line == '}':
            in_graph = False
        elif in_graph:
            # Extrahieren der Knoten
            node = re.match(r'([A-Za-z])\s*=\s*(\d+);', line)
            if node:
                node_name, node_id = node.groups()
                nodes[node_name] = Node(int(node_id), node_name)
            # Extrahieren der Kanten
            edge = re.match(r'([A-Za-z])\s*-\s*([A-Za-z])\s*:\s*(\d+);', line)
            if edge:
                n1, n2, weight = edge.groups()
                edges.append((n1, n2, int(weight)))

# Nachbarn für beide Knoten hinzufügen
for n1, n2, weight in edges:
    nodes[n1].add_neighbor(nodes[n2], weight)
    nodes[n2].add_neighbor(nodes[n1], weight)

all_nodes = list(nodes.values())

# Start der Spanning Tree Protocol Simulation
stp_protocol(all_nodes)

# Ausgabe des finalen Zustands aller Knoten
print_out(all_nodes)
