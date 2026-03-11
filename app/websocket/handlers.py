"""WebSocket event handlers."""

from flask_socketio import emit, join_room, leave_room
from app.game.engine import GameEngine
import uuid

# Global game engine
engine = GameEngine()

# Active sessions
sessions = {}


def register_handlers(socketio):
    """Register all WebSocket event handlers."""
    
    @socketio.on("connect")
    def handle_connect():
        """Handle client connection."""
        session_id = str(uuid.uuid4())
        game_state = engine.create_session(session_id)
        emit("session_created", {"session_id": session_id})
        emit("game_state", game_state.to_dict())
    
    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle client disconnection."""
        pass
    
    @socketio.on("start_run")
    def handle_start_run(data):
        """Start a new run."""
        session_id = data.get("session_id")
        ascension = data.get("ascension", 0)
        
        print(f"[START_RUN] session_id={session_id}, ascension={ascension}")
        
        game_state = engine.get_session(session_id)
        if game_state:
            # Update ascension level
            game_state.ascension = ascension
            game_state.player.ascension = ascension
            # Start combat
            engine.start_combat(session_id)
            
            # Debug logging
            state_dict = game_state.to_dict()
            print(f"[START_RUN] Player deck size: {len(game_state.player.deck)}")
            print(f"[START_RUN] Combat hand size: {len(game_state.current_combat.hand) if game_state.current_combat else 0}")
            print(f"[START_RUN] Sending game state with phase: {state_dict['phase']}")
            if game_state.current_combat:
                print(f"[START_RUN] Hand items: {len(state_dict['current_combat']['hand'])} cards")
            
            emit("game_state", state_dict)
    
    @socketio.on("play_card")
    def handle_play_card(data):
        """Play a card in combat."""
        session_id = data.get("session_id")
        card_index = data.get("card_index", 0)
        target_idx = data.get("target_idx", 0)
        
        success, message = engine.play_card(session_id, card_index, target_idx)
        game_state = engine.get_session(session_id)
        
        emit("action_result", {"success": success, "message": message})
        emit("game_state", game_state.to_dict())
    
    @socketio.on("end_turn")
    def handle_end_turn(data):
        """End player turn."""
        session_id = data.get("session_id")
        
        success, message = engine.end_turn(session_id)
        game_state = engine.get_session(session_id)
        
        emit("action_result", {"success": success, "message": message})
        emit("game_state", game_state.to_dict())
    
    @socketio.on("move_to_node")
    def handle_move_to_node(data):
        """Move to a map node."""
        session_id = data.get("session_id")
        node_id = data.get("node_id")
        
        success, message = engine.move_to_node(session_id, node_id)
        game_state = engine.get_session(session_id)
        
        emit("action_result", {"success": success, "message": message})
        emit("game_state", game_state.to_dict())
    
    @socketio.on("get_game_state")
    def handle_get_game_state(data):
        """Get current game state."""
        session_id = data.get("session_id")
        game_state = engine.get_session(session_id)
        
        if game_state:
            emit("game_state", game_state.to_dict())
        else:
            emit("error", {"message": "Session not found"})
