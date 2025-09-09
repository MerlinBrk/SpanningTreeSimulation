class Node:
    def __init__(self, root_id, id, cost=0):
        self.root_id = root_id
        self.id = id
        self.cost = cost
        self.neighbors = []  
        self.received_messages = []  

    def add_neighbor(self, neighbor_node, weight):
        self.neighbors.append((neighbor_node, weight))

    def send_message(self):
        for neighbor, weight in self.neighbors:
            neighbor.receive_message(self.root_id, self.cost, weight)

    def receive_message(self, root_id, cost, weight_to_neighbor):
        self.received_messages.append((root_id, cost, weight_to_neighbor))

    def update_state(self):
        updated = False
        for root_id, cost, weight_to_neighbor in self.received_messages:
            total_cost = cost + weight_to_neighbor

            if root_id < self.root_id:
                self.root_id = root_id
                self.cost = total_cost
                updated = True
            elif root_id == self.root_id and total_cost < self.cost:
                self.cost = total_cost
                updated = True

        self.received_messages.clear()
        return updated
    
class Node:
    def __init__(self, id):
        self.id = id
        self.root_id = id  # Start: jeder Knoten sieht sich selbst als Root
        self.cost = 0
        self.neighbors = []  # list of (neighbor_node, weight)
        self.received_messages = []

    def add_neighbor(self, neighbor_node, weight):
        self.neighbors.append((neighbor_node, weight))

    def send_message(self):
        for neighbor, weight in self.neighbors:
            neighbor.receive_message(self.root_id, self.cost, weight)

    def receive_message(self, root_id, cost, weight_to_neighbor):
        self.received_messages.append((root_id, cost, weight_to_neighbor))

    def update_state(self):
        updated = False
        for root_id, cost, weight_to_neighbor in self.received_messages:
            total_cost = cost + weight_to_neighbor
            if root_id < self.root_id:
                self.root_id = root_id
                self.cost = total_cost
                updated = True
            elif root_id == self.root_id and total_cost < self.cost:
                self.cost = total_cost
                updated = True
        self.received_messages.clear()
        return updated


A = Node(5)
B = Node(1)
C = Node(3)
D = Node(7)
E = Node(6)
F = Node(4)


A.add_neighbor(B, 10)
B.add_neighbor(A, 10)

A.add_neighbor(C, 10)
C.add_neighbor(A, 10)

B.add_neighbor(D, 15)
D.add_neighbor(B, 15)

B.add_neighbor(E, 10)
E.add_neighbor(B, 10)

C.add_neighbor(D, 3)
D.add_neighbor(C, 3)

C.add_neighbor(E, 10)
E.add_neighbor(C, 10)

D.add_neighbor(E, 2)
E.add_neighbor(D, 2)

D.add_neighbor(F, 10)
F.add_neighbor(D, 10)

E.add_neighbor(F, 2)
F.add_neighbor(E, 2)

all_nodes = [A, B, C, D, E, F]


converged = False
rounds = 0
while not converged and rounds < all_nodes.__len__():  
    rounds += 1
    converged = True
    for node in all_nodes:
        node.send_message()
    for node in all_nodes:
        if node.update_state():
            converged = False


for node in all_nodes:
    print(f"Node {node.id}: Root={node.root_id}, Cost={node.cost}")


