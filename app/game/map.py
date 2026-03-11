"""Map generation and traversal."""

import random
from app.utils.enums import NodeType
from app.utils.constants import MAP_WIDTH, MAP_HEIGHT


class MapNode:
    """A single node on the spire map."""
    
    _id_counter = 0
    
    def __init__(self, x, y, node_type, act=1, floor=0):
        MapNode._id_counter += 1
        self.id = MapNode._id_counter
        self.x = x
        self.y = y
        self.type = node_type
        self.act = act
        self.floor = floor
        self.is_visited = False
        self.reward = None
        self.connections = []  # Adjacent node IDs
    
    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "type": self.type.value,
            "visited": self.is_visited,
            "act": self.act,
        }


class SpireMap:
    """Procedurally generated map for an act."""
    
    def __init__(self, act=1, seed=None):
        self.act = act
        self.nodes = {}
        self.current_node_id = None
        self.seed = seed
        if seed:
            random.seed(seed)
        
        self.generate_map()
    
    def generate_map(self):
        """Generate a map for the act."""
        # Simple branching path generation
        path_length = 15 + self.act * 5
        
        for floor in range(path_length):
            # Determine room type based on position
            if floor == 0:
                node_type = NodeType.COMBAT
            elif floor == path_length - 1:
                node_type = NodeType.BOSS
            else:
                weights = {
                    NodeType.COMBAT: 0.60,
                    NodeType.ELITE: 0.15,
                    NodeType.MERCHANT: 0.10,
                    NodeType.REST: 0.10,
                    NodeType.EVENT: 0.05,
                }
                chosen = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
                node_type = chosen
            
            # Create nodes for branching (2-3 per floor)
            branches = random.randint(2, 3) if floor < path_length - 1 else 1
            
            for branch_idx in range(branches):
                x = branch_idx
                y = floor
                node = MapNode(x, y, node_type, self.act, floor)
                self.nodes[node.id] = node
                
                if floor == 0:
                    self.current_node_id = node.id
        
        # Connect nodes (simple vertical branching)
        nodes_by_floor = {}
        for node in self.nodes.values():
            if node.y not in nodes_by_floor:
                nodes_by_floor[node.y] = []
            nodes_by_floor[node.y].append(node)
        
        for floor in sorted(nodes_by_floor.keys()):
            if floor + 1 in nodes_by_floor:
                current_nodes = nodes_by_floor[floor]
                next_nodes = nodes_by_floor[floor + 1]
                for current in current_nodes:
                    for next_node in next_nodes:
                        current.connections.append(next_node.id)
    
    def get_available_next_nodes(self):
        """Get adjacent unvisited nodes."""
        if not self.current_node_id:
            return []
        
        current = self.nodes[self.current_node_id]
        return [self.nodes[node_id] for node_id in current.connections if not self.nodes[node_id].is_visited]
    
    def move_to_node(self, node_id):
        """Move to a node."""
        if node_id not in self.nodes:
            return False
        
        self.current_node_id = node_id
        self.nodes[node_id].is_visited = True
        return True
    
    def to_dict(self):
        return {
            "act": self.act,
            "current_node_id": self.current_node_id,
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "available_next": [node.to_dict() for node in self.get_available_next_nodes()],
        }
