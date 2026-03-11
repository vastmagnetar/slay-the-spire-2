"""Game state and player management."""

from app.utils.enums import CharacterClass, GamePhase
from app.game.cards import Strike, Defend, Bash, IronWave, Shrug
from app.game.relics import Burning, Rusted
from app.game.potions import HealthPotion, StrengthPotion, BlockPotion
from app.game.combat import Combatant
import json


class Player(Combatant):
    """Player character."""
    
    def __init__(self, character_class=CharacterClass.IRONCLAD):
        super().__init__("Player", 80)
        self.character_class = character_class
        self.deck = []
        self.hand = []
        self.relics = []
        self.gold = 0
        self.potions = []
        self.potions_slots = 3  # Max potions per combat
        self.ascension = 0
        
        # Initialize based on character
        if character_class == CharacterClass.IRONCLAD:
            self.max_hp = 80
            self.current_hp = 80
            self.initialize_ironclad_deck()
        
        # Starting relics
        self.relics.append(Burning())
    
    def initialize_ironclad_deck(self):
        """Initialize Ironclad's starting deck."""
        # 5 Strike, 4 Defend
        for _ in range(5):
            self.deck.append(Strike())
        for _ in range(4):
            self.deck.append(Defend())
    
    def add_card(self, card):
        """Add card to deck."""
        self.deck.append(card)
    
    def remove_card(self, card_id):
        """Remove card from deck."""
        self.deck = [c for c in self.deck if c.id != card_id]
    
    def upgrade_card(self, card_id):
        """Upgrade a card."""
        for card in self.deck:
            if card.id == card_id:
                card.upgrades += 1
                return True
        return False
    
    def add_relic(self, relic):
        """Add relic."""
        self.relics.append(relic)
    
    def to_dict(self):
        return {
            "name": self.name,
            "class": self.character_class.value,
            "hp": self.current_hp,
            "max_hp": self.max_hp,
            "gold": self.gold,
            "ascension": self.ascension,
            "deck_size": len(self.deck),
            "relics": [relic.to_dict() for relic in self.relics],
            "potions": self.potions,
        }


class GameState:
    """Manages overall game state."""
    
    def __init__(self, player, ascension=0):
        self.player = player
        self.ascension = ascension
        self.act = 1
        self.maps = {}
        self.current_map = None
        self.current_combat = None
        self.current_phase = GamePhase.MAP
        self.game_over = False
        self.player_won = False
        self.run_stats = {
            "turns_taken": 0,
            "damage_taken": 0,
            "enemies_defeated": 0,
            "gold_earned": 0,
        }
    
    def start_act(self, act):
        """Start a new act."""
        from app.game.map import SpireMap
        
        self.act = act
        self.current_map = SpireMap(act=act, seed=None)  # No seed = random
        self.maps[act] = self.current_map
        self.current_phase = GamePhase.MAP
    
    def enter_combat(self, monsters):
        """Enter combat with monsters."""
        from app.game.combat import Combat
        
        self.current_combat = Combat(self.player, monsters, self.ascension)
        self.current_phase = GamePhase.PLAYER_TURN
    
    def end_combat(self):
        """End combat and return to map."""
        if self.current_combat and self.current_combat.player_won:
            self.player.gold += 25 * (self.act + self.ascension // 5)
            self.run_stats["enemies_defeated"] += len(self.current_combat.monsters)
        
        self.current_combat = None
        self.current_phase = GamePhase.MAP
    
    def to_dict(self):
        # Sync combat state with game state
        if self.current_combat:
            if self.current_combat.is_combat_over:
                self.game_over = self.current_combat.is_combat_over
                self.player_won = self.current_combat.player_won
                # Also update player HP from combat
                self.player.current_hp = self.current_combat.player.current_hp
                # Update phase to reflect game end
                if self.current_combat.player_won:
                    self.current_phase = GamePhase.WON
                else:
                    self.current_phase = GamePhase.GAME_OVER
        
        return {
            "act": self.act,
            "phase": self.current_phase.value,
            "player": self.player.to_dict(),
            "game_over": self.game_over or (self.current_combat and self.current_combat.is_combat_over),
            "player_won": self.player_won or (self.current_combat.player_won if self.current_combat and self.current_combat.is_combat_over else False),
            "run_stats": self.run_stats,
            "current_map": self.current_map.to_dict() if self.current_map else None,
            "current_combat": self.current_combat.to_dict() if self.current_combat else None,
        }
