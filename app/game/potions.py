"""Potion system."""


class Potion:
    """Base potion class."""
    
    _id_counter = 0
    
    def __init__(self, name, effect_type, value, description):
        Potion._id_counter += 1
        self.id = Potion._id_counter
        self.name = name
        self.effect_type = effect_type
        self.value = value
        self.description = description
    
    def use(self, target):
        """Use the potion on target."""
        pass
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "effect_type": self.effect_type,
            "value": self.value,
            "description": self.description,
        }


class HealthPotion(Potion):
    def __init__(self, value=20):
        super().__init__(
            "Health Potion",
            "heal",
            value,
            f"Restore {value} HP"
        )
    
    def use(self, target):
        target.heal(self.value)


class StrengthPotion(Potion):
    def __init__(self, value=3):
        super().__init__(
            "Strength Potion",
            "strength",
            value,
            f"Gain {value} Strength for 1 combat"
        )
    
    def use(self, target):
        from app.game.status import Strength
        target.add_status(Strength(turns=1000, value=self.value))  # Large number for combat duration


class DexterityPotion(Potion):
    def __init__(self, value=3):
        super().__init__(
            "Dexterity Potion",
            "dexterity",
            value,
            f"Gain {value} Dexterity for 1 combat"
        )
    
    def use(self, target):
        from app.game.status import Dexterity
        target.add_status(Dexterity(turns=1000, value=self.value))


class BlockPotion(Potion):
    def __init__(self, value=15):
        super().__init__(
            "Block Potion",
            "block",
            value,
            f"Gain {value} Block"
        )
    
    def use(self, target):
        target.add_block(self.value)


class LiquidMemories(Potion):
    def __init__(self):
        super().__init__(
            "Liquid Memories",
            "draw",
            3,
            "Draw 3 additional cards"
        )
    
    def use(self, target):
        # This is called in combat
        pass


class AncientPotion(Potion):
    def __init__(self):
        super().__init__(
            "Ancient Potion",
            "heal_all",
            100,
            "Heal to max HP"
        )
    
    def use(self, target):
        target.current_hp = target.max_hp


class EssenceOfSteel(Potion):
    def __init__(self):
        super().__init__(
            "Essence of Steel",
            "protection",
            10,
            "Gain 10 Block. Double this amount next turn."
        )
    
    def use(self, target):
        target.add_block(10)


class ExplosivePotion(Potion):
    def __init__(self, value=10):
        super().__init__(
            "Explosive Potion",
            "aoe_damage",
            value,
            f"Deal {value} damage to all enemies"
        )
    
    def use(self, enemies):
        for enemy in enemies:
            if enemy.is_alive:
                enemy.take_damage(self.value)


class PoisonPotion(Potion):
    def __init__(self, value=6):
        super().__init__(
            "Poison Potion",
            "poison",
            value,
            f"Apply {value} Poison to target"
        )
    
    def use(self, enemy):
        from app.game.status import Poison
        enemy.add_status(Poison(turns=-1, damage_per_turn=self.value))


class IdentifyPotion(Potion):
    def __init__(self):
        super().__init__(
            "Identify",
            "card_view",
            0,
            "See your entire deck"
        )
    
    def use(self, target):
        # UI element - would show full deck
        pass


class FocusPotion(Potion):
    def __init__(self, value=1):
        super().__init__(
            "Focus Potion",
            "focus",
            value,
            f"Gain {value} additional energy next turn"
        )
    
    def use(self, target):
        # This would be tracked for next turn
        pass
