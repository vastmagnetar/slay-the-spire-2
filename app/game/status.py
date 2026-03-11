"""Status effects system."""

class StatusEffect:
    """Base class for status effects."""
    
    def __init__(self, name, turns=-1, value=0, damage_per_turn=0):
        self.name = name
        self.turns = turns  # -1 = infinite
        self.value = value
        self.damage_per_turn = damage_per_turn
    
    def apply(self, target):
        """Apply effect to target."""
        pass
    
    def tick(self):
        """Reduce duration."""
        if self.turns > 0:
            self.turns -= 1
    
    def is_expired(self):
        """Check if effect has expired."""
        return self.turns == 0
    
    def to_dict(self):
        return {
            "name": self.name,
            "turns": self.turns,
            "value": self.value,
            "damage_per_turn": self.damage_per_turn,
        }


class Strength(StatusEffect):
    """Increases damage dealt by value."""
    def __init__(self, turns=-1, value=1):
        super().__init__("strength", turns, value)


class Vulnerable(StatusEffect):
    """Takes 1.5x more damage when value stacks."""
    def __init__(self, turns=1, value=1):
        super().__init__("vulnerable", turns, value)


class Frail(StatusEffect):
    """Block gain is reduced by 25% per stack."""
    def __init__(self, turns=1, value=1):
        super().__init__("frail", turns, value)


class Weak(StatusEffect):
    """Damage dealt is reduced by 25% per stack."""
    def __init__(self, turns=1, value=1):
        super().__init__("weak", turns, value)


class Dexterity(StatusEffect):
    """Increases block gained by value."""
    def __init__(self, turns=-1, value=1):
        super().__init__("dexterity", turns, value)


class Poison(StatusEffect):
    """Deals damage at start of enemy turn."""
    def __init__(self, turns=-1, damage_per_turn=1):
        super().__init__("poison", turns, 0, damage_per_turn)


class Artifact(StatusEffect):
    """Blocks next debuff application."""
    def __init__(self, charges=1):
        super().__init__("artifact", -1, charges)
