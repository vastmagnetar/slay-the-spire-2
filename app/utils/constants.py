"""Game constants and configuration."""

# Combat Constants
MAX_HAND_SIZE = 10
INITIAL_ENERGY = 3
SCALING_ENERGY_INCREASE = 0.5

# Card rarity weights
CARD_RARITY_WEIGHTS = {
    "common": 0.60,
    "uncommon": 0.30,
    "rare": 0.08,
    "special": 0.02,
}

# Status effect defaults
STATUS_EFFECTS = {
    "strength": {"turns": -1, "value": 0},  # Scales damage dealt
    "vulnerable": {"turns": -1, "value": 0},  # 1.5x takes more damage
    "frail": {"turns": -1, "value": 0},  # 0.75x block gained
    "weak": {"turns": -1, "value": 0},  # 0.75x damage dealt
    "dexterity": {"turns": -1, "value": 0},  # Scales block gained
    "poison": {"turns": -1, "damage_per_turn": 0},
    "artifact": {"turns": -1, "charges": 0},  # Blocks next debuff
}

# Relic effects tiers
RELIC_TIERS = ["common", "uncommon", "rare", "boss", "shop", "special"]

# Card removal cost (in gold, at shop)
CARD_REMOVE_COST = 25

# Act bosses
BOSS_NAMES = ["Exordium", "The Champ", "Awakened One"]
ASCENSION_LEVELS = 20

# Map constants
MAP_WIDTH = 15
MAP_HEIGHT = 15
CARDS_PER_REWARD = 3
