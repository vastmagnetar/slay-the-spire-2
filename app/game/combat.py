"""Combat system."""

from app.utils.constants import INITIAL_ENERGY, MAX_HAND_SIZE
from app.utils.enums import GamePhase, CardType
from app.game.cards import Strike, Defend
from app.game.status import Poison
import copy


class Combatant:
    """Player or enemy in combat."""
    
    def __init__(self, name, max_hp=100):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.block = 0
        self.strength = 0
        self.dexterity = 0
        self.status_effects = {}
    
    def take_damage(self, amount):
        """Take damage after reductions."""
        # Apply vulnerable
        if "vulnerable" in self.status_effects:
            amount = int(amount * 1.5)
        
        # Apply weak
        if "weak" in self.status_effects:
            weak_stacks = self.status_effects["weak"].value
            amount = int(amount * (0.75 ** weak_stacks))
        
        # Apply frail to block
        block_reduction = 1.0
        if "frail" in self.status_effects:
            frail_stacks = self.status_effects["frail"].value
            block_reduction = 0.75 ** frail_stacks
        
        effective_block = int(self.block * block_reduction)
        damage_after_block = max(1, amount - effective_block)
        self.current_hp -= damage_after_block
        self.block = max(0, self.block - amount)
        
        # Clamp HP to minimum 0 for UI purposes
        if self.current_hp < 0:
            self.current_hp = 0
    
    def add_status(self, status):
        """Add status effect."""
        if status.name in self.status_effects:
            existing = self.status_effects[status.name]
            if hasattr(existing, 'value') and hasattr(status, 'value'):
                existing.value += status.value
            existing.turns = max(existing.turns, status.turns) if existing.turns != -1 else -1
        else:
            self.status_effects[status.name] = status
    
    def add_block(self, amount):
        """Add block."""
        self.block += amount
    
    def heal(self, amount):
        """Heal."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def is_alive(self):
        return self.current_hp > 0
    
    def end_turn(self):
        """Process end of turn effects."""
        # Poison damage
        if "poison" in self.status_effects:
            poison = self.status_effects["poison"]
            self.take_damage(poison.damage_per_turn)
        
        # Tick status effects
        for status_name, status in list(self.status_effects.items()):
            status.tick()
            if status.is_expired():
                del self.status_effects[status_name]
        
        # Reset block
        self.block = 0


class Combat:
    """Handles all combat logic."""
    
    def __init__(self, player, monsters, ascension=0):
        self.player = player
        self.monsters = monsters
        self.ascension = ascension
        
        # Combat state
        self.current_phase = GamePhase.PLAYER_TURN
        self.turn_number = 0
        self.player_energy = INITIAL_ENERGY
        self.max_energy = INITIAL_ENERGY
        
        # Player hand/deck management
        self.draw_pile = copy.deepcopy(player.deck)
        self.discard_pile = []
        self.hand = []
        self.exhausted_pile = []
        
        # Combat state
        self.is_combat_over = False
        self.player_won = False
        
        # Debug logging
        print(f"[COMBAT_INIT] Player deck size: {len(player.deck)}")
        print(f"[COMBAT_INIT] Draw pile size after copy: {len(self.draw_pile)}")
        
        # Draw initial hand
        self.draw_cards(5)
        
        print(f"[COMBAT_INIT] Hand size after draw: {len(self.hand)}")
    
    def draw_cards(self, count=1):
        """Draw cards from deck, reshuffling if needed."""
        for _ in range(count):
            if not self.draw_pile and self.discard_pile:
                # Reshuffle
                self.draw_pile = self.discard_pile[:]
                self.discard_pile = []
            
            if self.draw_pile:
                card = self.draw_pile.pop(0)
                if len(self.hand) < MAX_HAND_SIZE:
                    self.hand.append(card)
    
    def play_card(self, card_index, target_idx=0):
        """Play a card from hand."""
        if card_index >= len(self.hand):
            return False, "Invalid card index"
        
        card = self.hand[card_index]
        
        # Check energy
        if card.cost > self.player_energy:
            return False, "Not enough energy"
        
        # Play card
        self.player_energy -= card.cost
        self.hand.pop(card_index)
        
        # Execute card effect
        if hasattr(card, 'play'):
            card.play(self.player, self.monsters, target_idx)
        
        # Discard or exhaust
        if card.is_exhausted:
            self.exhausted_pile.append(card)
        else:
            self.discard_pile.append(card)
        
        return True, "Card played"
    
    def end_player_turn(self):
        """End player's turn and start enemy turn."""
        # Check if player is already dead
        if not self.player.is_alive():
            self.current_phase = GamePhase.COMBAT_END
            self.player_won = False
            self.is_combat_over = True
            return
        
        # Discard remaining hand
        self.discard_pile.extend(self.hand)
        self.hand = []
        
        # End of turn effects for player
        self.player.end_turn()
        
        # Check if player died from end of turn effects
        if not self.player.is_alive():
            self.current_phase = GamePhase.COMBAT_END
            self.player_won = False
            self.is_combat_over = True
            return
        
        # Draw new hand
        self.draw_cards(5)
        
        # Enemy turn
        self.current_phase = GamePhase.ENEMY_TURN
        self.execute_enemy_turn()
        
        # Check win/loss after enemy turn
        if not any(m.is_alive for m in self.monsters):
            self.current_phase = GamePhase.COMBAT_END
            self.player_won = True
            self.is_combat_over = True
        elif not self.player.is_alive():
            self.current_phase = GamePhase.COMBAT_END
            self.player_won = False
            self.is_combat_over = True
        else:
            # Next turn
            self.start_new_turn()
    
    def execute_enemy_turn(self):
        """Execute all enemy actions."""
        for monster in self.monsters:
            if monster.is_alive:
                monster.execute_action(self.player)
            monster.end_turn()
    
    def plan_enemy_turn(self):
        """Plan next enemy turn (called at end of player turn)."""
        for monster in self.monsters:
            if monster.is_alive:
                monster.plan_action()
    
    def start_new_turn(self):
        """Start a new player turn."""
        self.turn_number += 1
        self.current_phase = GamePhase.PLAYER_TURN
        self.player_energy = self.max_energy
        self.plan_enemy_turn()
    
    def to_dict(self):
        """Serialize combat state."""
        return {
            "turn": self.turn_number,
            "phase": self.current_phase.value,
            "player_energy": self.player_energy,
            "max_energy": self.max_energy,
            "player": {
                "name": self.player.name,
                "hp": self.player.current_hp,
                "max_hp": self.player.max_hp,
                "block": self.player.block,
                "strength": self.player.strength,
                "dexterity": self.player.dexterity,
                "status_effects": {name: status.to_dict() for name, status in self.player.status_effects.items()},
            },
            "hand": [card.to_dict() for card in self.hand],
            "hand_size": len(self.hand),
            "draw_pile_size": len(self.draw_pile),
            "discard_pile_size": len(self.discard_pile),
            "monsters": [m.to_dict() for m in self.monsters if m.is_alive],
            "is_combat_over": self.is_combat_over,
            "player_won": self.player_won,
        }
