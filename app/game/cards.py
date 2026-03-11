"""Card system."""

from app.utils.enums import CardType, CardRarity
import json


class Card:
    """Base card class."""
    
    _id_counter = 0
    
    def __init__(self, name, card_type, cost, description, rarity=CardRarity.COMMON, upgrades=0):
        Card._id_counter += 1
        self.id = Card._id_counter
        self.name = name
        self.type = card_type
        self.cost = cost
        self.base_cost = cost
        self.description = description
        self.rarity = rarity
        self.upgrades = upgrades
        self.is_exhausted = False
        self.target_enemy = None
    
    def play(self, player, enemies, target_idx=0):
        """Execute card effect."""
        pass
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "cost": self.cost,
            "description": self.description,
            "rarity": self.rarity.value,
            "upgrades": self.upgrades,
        }


# IRONCLAD ATTACK CARDS
class Strike(Card):
    def __init__(self, upgrades=0):
        cost = 1
        damage = 6 + upgrades
        super().__init__(
            "Strike", CardType.ATTACK, cost,
            f"Deal {damage} damage.",
            CardRarity.COMMON, upgrades
        )
        self.damage = damage
    
    def play(self, player, enemies, target_idx=0):
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)


class Bash(Card):
    def __init__(self, upgrades=0):
        cost = 1
        damage = 8 + upgrades * 2
        vulnerable = 1
        super().__init__(
            "Bash", CardType.ATTACK, cost,
            f"Deal {damage} damage. Apply {vulnerable} Vulnerable.",
            CardRarity.COMMON, upgrades
        )
        self.damage = damage
        self.vulnerable = vulnerable
    
    def play(self, player, enemies, target_idx=0):
        from app.game.status import Vulnerable
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)
        enemies[target_idx].add_status(Vulnerable(2, self.vulnerable))


class Pummel(Card):
    def __init__(self, upgrades=0):
        cost = 1
        hits = 4 + upgrades
        super().__init__(
            "Pummel", CardType.ATTACK, cost,
            f"Deal 1 damage {hits} times.",
            CardRarity.COMMON, upgrades
        )
        self.hits = hits
    
    def play(self, player, enemies, target_idx=0):
        damage_per_hit = 1
        if player.strength > 0:
            damage_per_hit += player.strength
        for _ in range(self.hits):
            enemies[target_idx].take_damage(damage_per_hit)


class Headbutt(Card):
    def __init__(self, upgrades=0):
        cost = 1
        damage = 9 + upgrades * 3
        super().__init__(
            "Headbutt", CardType.ATTACK, cost,
            f"Deal {damage} damage. Draw 1 card.",
            CardRarity.COMMON, upgrades
        )
        self.damage = damage
    
    def play(self, player, enemies, target_idx=0):
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)
        player.draw_cards(1)


class Clothesline(Card):
    def __init__(self, upgrades=0):
        cost = 2
        damage = 12 + upgrades * 3
        super().__init__(
            "Clothesline", CardType.ATTACK, cost,
            f"Deal {damage} damage. Apply 1 Weak.",
            CardRarity.UNCOMMON, upgrades
        )
        self.damage = damage
    
    def play(self, player, enemies, target_idx=0):
        from app.game.status import Weak
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)
        enemies[target_idx].add_status(Weak(1, 1))


class Uppercut(Card):
    def __init__(self, upgrades=0):
        cost = 1
        damage = 13 + upgrades * 2
        super().__init__(
            "Uppercut", CardType.ATTACK, cost,
            f"Deal {damage} damage. Apply 1 Weak and 1 Vulnerable.",
            CardRarity.UNCOMMON, upgrades
        )
        self.damage = damage
    
    def play(self, player, enemies, target_idx=0):
        from app.game.status import Weak, Vulnerable
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)
        enemies[target_idx].add_status(Weak(1, 1))
        enemies[target_idx].add_status(Vulnerable(1, 1))


class Bludgeon(Card):
    def __init__(self, upgrades=0):
        cost = 1
        damage = 32 + upgrades * 8
        super().__init__(
            "Bludgeon", CardType.ATTACK, cost,
            f"Deal {damage} damage.",
            CardRarity.RARE, upgrades
        )
        self.damage = damage
    
    def play(self, player, enemies, target_idx=0):
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)


# IRONCLAD SKILL CARDS
class Defend(Card):
    def __init__(self, upgrades=0):
        cost = 1
        block = 7 + upgrades
        super().__init__(
            "Defend", CardType.SKILL, cost,
            f"Gain {block} Block.",
            CardRarity.COMMON, upgrades
        )
        self.block = block
    
    def play(self, player, enemies, target_idx=0):
        block = self.block
        if player.dexterity > 0:
            block += player.dexterity
        player.add_block(block)


class Shrug(Card):
    def __init__(self, upgrades=0):
        cost = 1
        block = 8 + upgrades
        super().__init__(
            "Shrug It Off", CardType.SKILL, cost,
            f"Gain {block} Block. Draw 1 card.",
            CardRarity.COMMON, upgrades
        )
        self.block = block
    
    def play(self, player, enemies, target_idx=0):
        block = self.block
        if player.dexterity > 0:
            block += player.dexterity
        player.add_block(block)
        player.draw_cards(1)


class Brace(Card):
    def __init__(self, upgrades=0):
        cost = 1
        block = 12 + upgrades * 2
        super().__init__(
            "Brace Impact", CardType.SKILL, cost,
            f"Gain {block} Block and 1 Strength.",
            CardRarity.UNCOMMON, upgrades
        )
        self.block = block
    
    def play(self, player, enemies, target_idx=0):
        from app.game.status import Strength
        block = self.block
        if player.dexterity > 0:
            block += player.dexterity
        player.add_block(block)
        player.add_status(Strength(-1, 1))


class IronWave(Card):
    def __init__(self, upgrades=0):
        cost = 1
        damage = 5 + upgrades
        block = 5 + upgrades
        super().__init__(
            "Iron Wave", CardType.SKILL, cost,
            f"Gain {block} Block. Deal {damage} damage.",
            CardRarity.COMMON, upgrades
        )
        self.damage = damage
        self.block = block
    
    def play(self, player, enemies, target_idx=0):
        block = self.block
        if player.dexterity > 0:
            block += player.dexterity
        player.add_block(block)
        
        damage = self.damage
        if player.strength > 0:
            damage += player.strength
        enemies[target_idx].take_damage(damage)


# IRONCLAD POWER CARDS
class Anger(Card):
    def __init__(self, upgrades=0):
        cost = 0
        damage = 6 + upgrades
        super().__init__(
            "Anger", CardType.POWER, cost,
            f"Whenever you play a card this turn, create a copy of it in your hand.",
            CardRarity.UNCOMMON, upgrades
        )
        self.damage = damage


class Inflame(Card):
    def __init__(self, upgrades=0):
        cost = 1
        strength = 2 + upgrades
        super().__init__(
            "Inflame", CardType.POWER, cost,
            f"Gain {strength} Strength.",
            CardRarity.COMMON, upgrades
        )
        self.strength = strength
    
    def play(self, player, enemies, target_idx=0):
        from app.game.status import Strength
        player.add_status(Strength(-1, self.strength))


class BloodyMad(Card):
    def __init__(self, upgrades=0):
        cost = 1
        super().__init__(
            "Bloodletting", CardType.POWER, cost,
            "Lose 3 HP. Gain 1 Strength.",
            CardRarity.UNCOMMON, upgrades
        )
    
    def play(self, player, enemies, target_idx=0):
        from app.game.status import Strength
        player.take_damage(3)
        player.add_status(Strength(-1, 1))
