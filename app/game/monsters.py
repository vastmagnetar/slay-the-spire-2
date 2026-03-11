"""Monster and enemy definitions."""

from app.utils.enums import Intent
from app.game.status import Strength, Vulnerable, Weak, Frail, Poison, Artifact
import random


class Behavior:
    """AI behavior pattern for enemies."""
    
    def __init__(self, action, intent, turns_between=1):
        self.action = action  # Function to call
        self.intent = intent  # Intent enum for display
        self.turns_between = turns_between
        self.turn_count = 0
    
    def should_execute(self):
        self.turn_count += 1
        if self.turn_count >= self.turns_between:
            self.turn_count = 0
            return True
        return False


class Monster:
    """Base monster class."""
    
    _id_counter = 0
    
    def __init__(self, name, max_hp, strength=0, dexterity=0):
        Monster._id_counter += 1
        self.id = Monster._id_counter
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.strength = strength
        self.dexterity = dexterity
        self.block = 0
        self.status_effects = {}
        self.is_alive = True
        self.behaviors = []
        self.intent = Intent.ATTACK
        self.intent_value = 0
        self.next_action = None
    
    def take_damage(self, amount):
        """Take damage, accounting for block and vulnerabilities."""
        # Apply vulnerable
        if "vulnerable" in self.status_effects:
            amount = int(amount * 1.5)
        
        # Apply weak (reduces damage by 25% per stack)
        if "weak" in self.status_effects:
            weak_stacks = self.status_effects["weak"].value
            amount = int(amount * (0.75 ** weak_stacks))
        
        damage_after_block = max(0, amount - self.block)
        self.current_hp -= damage_after_block
        self.block = max(0, self.block - amount)
        
        if self.current_hp <= 0:
            self.is_alive = False
    
    def add_status(self, status):
        """Add a status effect."""
        if status.name in self.status_effects:
            # Stack the effect
            existing = self.status_effects[status.name]
            existing.value += status.value
            existing.turns = max(existing.turns, status.turns)
        else:
            self.status_effects[status.name] = status
    
    def heal(self, amount):
        """Heal monster."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def add_block(self, amount):
        """Add block."""
        self.block += amount
    
    def plan_action(self):
        """Decide next action (override in subclasses)."""
        pass
    
    def execute_action(self, player):
        """Execute the planned action."""
        pass
    
    def end_turn(self):
        """Process end of turn effects."""
        # Poison damage
        if "poison" in self.status_effects:
            poison = self.status_effects["poison"]
            self.take_damage(poison.damage_per_turn)
        
        # Tick down status effects
        for status_name, status in list(self.status_effects.items()):
            status.tick()
            if status.is_expired():
                del self.status_effects[status_name]
        
        # Reset block
        self.block = 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "hp": self.current_hp,
            "max_hp": self.max_hp,
            "block": self.block,
            "strength": self.strength,
            "intent": self.intent.value,
            "intent_value": self.intent_value,
            "status_effects": {name: status.to_dict() for name, status in self.status_effects.items()},
        }


class Cultist(Monster):
    """Weak early-game enemy."""
    
    def __init__(self):
        super().__init__("Cultist", 48, 0, 0)
        self.rituals_done = 0
    
    def plan_action(self):
        if self.rituals_done < 2:
            self.intent = Intent.BUFF
            self.intent_value = 1
            self.rituals_done += 1
        else:
            self.intent = Intent.ATTACK
            self.intent_value = 6
    
    def execute_action(self, player):
        if self.rituals_done <= 2:
            self.add_status(Strength(turns=-1, value=1))
        else:
            player.take_damage(6)


class Worker(Monster):
    """Worker that gains strength."""
    
    def __init__(self):
        super().__init__("Worker", 48, 0, 0)
        self.powering_up = False
    
    def plan_action(self):
        if self.current_hp > 24:
            self.intent = Intent.BUFF
            self.intent_value = 1
            self.powering_up = True
        else:
            self.intent = Intent.ATTACK
            self.intent_value = 8
            self.powering_up = False
    
    def execute_action(self, player):
        if self.powering_up:
            self.add_status(Strength(turns=-1, value=2))
        else:
            player.take_damage(8)


class Jaw(Monster):
    """Bloated creature that drains block."""
    
    def __init__(self):
        super().__init__("Jaw Worm", 40, 0, 0)
        self.action_counter = 0
    
    def plan_action(self):
        if self.action_counter % 2 == 0:
            self.intent = Intent.ATTACK
            self.intent_value = 11
        else:
            self.intent = Intent.DEBUFF
            self.intent_value = 0  # Frail application
        self.action_counter += 1
    
    def execute_action(self, player):
        if self.action_counter % 2 == 1:
            player.take_damage(11)
        else:
            player.add_status(Frail(turns=1, value=1))


class Gremlin(Monster):
    """Fast, weak enemy."""
    
    def __init__(self):
        super().__init__("Gremlin", 22, 0, 0)
    
    def plan_action(self):
        self.intent = Intent.ATTACK
        self.intent_value = 5
    
    def execute_action(self, player):
        player.take_damage(5)


class Spheric(Monster):
    """Defensive enemy."""
    
    def __init__(self):
        super().__init__("Spheric", 45, 0, 1)
    
    def plan_action(self):
        if self.current_hp < 30:
            self.intent = Intent.DEFEND
            self.intent_value = 12
        else:
            self.intent = Intent.ATTACK
            self.intent_value = 9
    
    def execute_action(self, player):
        if self.current_hp < 30:
            self.add_block(12)
        else:
            player.take_damage(9)


class TheGuardian(Monster):
    """Boss: heavy defense and scaling."""
    
    def __init__(self):
        super().__init__("The Guardian", 200, 1, 0)
        self.attack_counter = 0
    
    def plan_action(self):
        if self.attack_counter % 3 == 0:
            self.intent = Intent.DEFEND
            self.intent_value = 25
        else:
            self.intent = Intent.ATTACK
            self.intent_value = 26
        self.attack_counter += 1
    
    def execute_action(self, player):
        if self.attack_counter % 3 == 1:
            self.add_block(25)
        else:
            damage = 26 + self.strength
            player.take_damage(damage)


class SpikeSlime(Monster):
    """Slime that splits on death."""
    
    def __init__(self, size="large"):
        self.size = size
        sizes = {"large": 55, "medium": 32, "small": 12}
        super().__init__(f"Spike Slime ({size})", sizes[size], 0, 0)
    
    def plan_action(self):
        self.intent = Intent.ATTACK
        self.intent_value = 5 if self.size == "large" else (3 if self.size == "medium" else 1)
    
    def execute_action(self, player):
        damage = {"large": 5, "medium": 3, "small": 1}[self.size]
        player.take_damage(damage)


class Avocado(Monster):
    """High HP, low damage enemy."""
    
    def __init__(self):
        super().__init__("Avocado", 60, 0, 0)
    
    def plan_action(self):
        self.intent = Intent.ATTACK
        self.intent_value = 7
    
    def execute_action(self, player):
        player.take_damage(7)


class Exploder(Monster):
    """Explodes when low health."""
    
    def __init__(self):
        super().__init__("Exploder", 35, 0, 0)
        self.has_exploded = False
    
    def plan_action(self):
        if self.current_hp <= 12 and not self.has_exploded:
            self.intent = Intent.SPECIAL
            self.intent_value = 15
        else:
            self.intent = Intent.ATTACK
            self.intent_value = 8
    
    def execute_action(self, player):
        if self.current_hp <= 12 and not self.has_exploded:
            player.take_damage(15)
            self.has_exploded = True
        else:
            player.take_damage(8)


class OgreFirehead(Monster):
    """Boss that applies vulnerable."""
    
    def __init__(self):
        super().__init__("Ogrefire Head", 180, 0, 0)
        self.turn_counter = 0
    
    def plan_action(self):
        if self.turn_counter % 2 == 0:
            self.intent = Intent.ATTACK
            self.intent_value = 30
        else:
            self.intent = Intent.DEBUFF
            self.intent_value = 2  # vulnerability stacks
        self.turn_counter += 1
    
    def execute_action(self, player):
        if self.turn_counter % 2 == 1:
            player.take_damage(30)
        else:
            for _ in range(2):
                player.add_status(Vulnerable(turns=2, value=1))

