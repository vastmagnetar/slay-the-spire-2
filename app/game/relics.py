"""Relics system."""

import random


class Relic:
    """Base relic class."""
    
    _id_counter = 0
    
    def __init__(self, name, tier, description, passive_effect=None):
        Relic._id_counter += 1
        self.id = Relic._id_counter
        self.name = name
        self.tier = tier
        self.description = description
        self.passive_effect = passive_effect or {}
        self.charges = 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tier": self.tier,
            "description": self.description,
        }


class Burning(Relic):
    def __init__(self):
        super().__init__(
            "Burning Blood",
            "common",
            "Whenever you would die, heal to full instead. Lose this relic."
        )


class AncientTeaSet(Relic):
    def __init__(self):
        super().__init__(
            "Ancient Tea Set",
            "common",
            "Whenever you rest, gain 2 additional maximum HP."
        )


class Rusted(Relic):
    def __init__(self):
        super().__init__(
            "Rusted Sword",
            "common",
            "Start each combat with 1 Strength.",
            {"strength": 1}
        )


class UnionOfAffection(Relic):
    def __init__(self):
        super().__init__(
            "Union of Affection",
            "uncommon",
            "Start each combat with 1 Block."
        )


class SentryPlate(Relic):
    def __init__(self):
        super().__init__(
            "Sentry Plate",
            "uncommon",
            "Start each combat with 3 Block."
        )


class Pantograph(Relic):
    def __init__(self):
        super().__init__(
            "Pantograph",
            "uncommon",
            "Whenever you upgrade a card, increase its cost by 1."
        )


class Shuriken(Relic):
    def __init__(self):
        super().__init__(
            "Shuriken",
            "uncommon",
            "Whenever you play 3 Attacks in a single turn, gain 1 Strength."
        )


class Sneko(Relic):
    def __init__(self):
        super().__init__(
            "Snecko Eye",
            "rare",
            "Start each combat with 2 additional card draw. Cards cost 1 more to play."
        )


class MarkOfPain(Relic):
    def __init__(self):
        super().__init__(
            "Mark of Pain",
            "rare",
            "Whenever you play a Power, gain 1 Strength."
        )


class Philosopher(Relic):
    def __init__(self):
        super().__init__(
            "Philosopher's Stone",
            "rare",
            "Gain 1 additional Orb slot. Powers with a rarity appear more often."
        )


# Boss relics (rare, end-of-act rewards)
class Sozu(Relic):
    def __init__(self):
        super().__init__(
            "Sozu",
            "boss",
            "You cannot obtain Potions. Gain 1 additional Orb slot."
        )


class Runic(Relic):
    def __init__(self):
        super().__init__(
            "Runic Pyramid",
            "boss",
            "Cards are not discarded at end of turn."
        )


class FrozenCore(Relic):
    def __init__(self):
        super().__init__(
            "Frozen Core",
            "boss",
            "Whenever you discard a card, increase your maximum HP by 1."
        )
