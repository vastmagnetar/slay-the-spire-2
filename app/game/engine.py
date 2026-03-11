"""Main game engine and orchestration."""

from app.game.state import GameState, Player
from app.game.monsters import (
    Cultist, Worker, TheGuardian, SpikeSlime, 
    Jaw, Gremlin, Spheric, Avocado, Exploder, OgreFirehead
)
from app.utils.enums import CharacterClass, GamePhase
import random


class GameEngine:
    """Main game engine orchestrating all systems."""
    
    def __init__(self, ascension=0):
        self.player = Player(CharacterClass.IRONCLAD)
        self.player.ascension = ascension
        self.game_state = GameState(self.player, ascension)
        self.sessions = {}  # Store active game sessions
    
    def create_session(self, session_id):
        """Create a new game session."""
        # Create a new player for this session
        player = Player(CharacterClass.IRONCLAD)
        player.ascension = self.player.ascension
        self.game_state = GameState(player, player.ascension)
        self.game_state.start_act(1)
        self.sessions[session_id] = self.game_state
        return self.game_state
    
    def get_session(self, session_id):
        """Retrieve a game session."""
        return self.sessions.get(session_id)
    
    def start_combat(self, session_id):
        """Start a random combat encounter."""
        game_state = self.get_session(session_id)
        if not game_state:
            return False
        
        # Generate random monsters based on difficulty
        act_monsters = [
            (Cultist, 2.0),
            (Worker, 1.5),
            (Jaw, 1.5),
            (Gremlin, 2.0),
        ]
        
        boss_monsters = [
            (TheGuardian, 0.5),
            (OgreFirehead, 0.5),
        ]
        
        # Act 1
        if game_state.act == 1:
            weights = [w[1] for w in act_monsters]
            monster_classes = [m[0] for m in act_monsters]
        # Act 2+
        else:
            more_monsters = act_monsters + [(SpikeSlime, 1.0), (Avocado, 1.5), (Exploder, 1.0)]
            weights = [w[1] for w in more_monsters]
            monster_classes = [m[0] for m in more_monsters]
        
        count = random.randint(1, 2) if game_state.act == 1 else random.randint(2, 3)
        monsters = []
        for _ in range(count):
            MonsterClass = random.choices(monster_classes, weights=weights)[0]
            if MonsterClass == SpikeSlime:
                # Random size for slimes
                size = random.choice(["large", "medium"])
                monsters.append(MonsterClass(size))
            else:
                monsters.append(MonsterClass())
        
        game_state.enter_combat(monsters)
        return True
    
    def play_card(self, session_id, card_index, target_idx=0):
        """Play a card in combat."""
        game_state = self.get_session(session_id)
        if not game_state or not game_state.current_combat:
            return False, "Not in combat"
        
        return game_state.current_combat.play_card(card_index, target_idx)
    
    def end_turn(self, session_id):
        """End player turn."""
        game_state = self.get_session(session_id)
        if not game_state or not game_state.current_combat:
            return False, "Not in combat"
        
        game_state.current_combat.end_player_turn()
        return True, "Turn ended"
    
    def move_to_node(self, session_id, node_id):
        """Move to a map node."""
        game_state = self.get_session(session_id)
        if not game_state or not game_state.current_map:
            return False, "Not on map"
        
        if game_state.current_map.move_to_node(node_id):
            # Start combat based on node type
            from app.utils.enums import NodeType
            current_node = game_state.current_map.nodes[node_id]
            
            if current_node.type in [NodeType.COMBAT, NodeType.ELITE, NodeType.BOSS]:
                self.start_combat(session_id)
            
            return True, f"Moved to node {node_id}"
        
        return False, "Cannot move to that node"
    
    def get_game_state(self, session_id):
        """Get current game state for serialization."""
        game_state = self.get_session(session_id)
        return game_state.to_dict() if game_state else None
