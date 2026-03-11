"""Enums for game types."""

from enum import Enum

class CardType(Enum):
    ATTACK = "attack"
    SKILL = "skill"
    POWER = "power"


class CardRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    SPECIAL = "special"


class NodeType(Enum):
    COMBAT = "combat"
    ELITE = "elite"
    MERCHANT = "merchant"
    REST = "rest"
    EVENT = "event"
    BOSS = "boss"
    TREASURE = "treasure"


class Intent(Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    BUFF = "buff"
    DEBUFF = "debuff"
    SPECIAL = "special"
    STUN = "stun"


class CharacterClass(Enum):
    IRONCLAD = "ironclad"
    SILENT = "silent"


class GamePhase(Enum):
    PLAYER_TURN = "player_turn"
    PLAYER_ACTION = "player_action"
    ENEMY_TURN = "enemy_turn"
    COMBAT_END = "combat_end"
    MAP = "map"
    SHOP = "shop"
    REST = "rest"
    GAME_OVER = "game_over"
    WON = "won"
