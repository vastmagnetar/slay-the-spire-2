#!/usr/bin/env python3
"""Test initialization of Player and Combat."""

from app.game.state import Player, GameState
from app.game.monsters import Cultist
from app.utils.enums import CharacterClass

print("=" * 60)
print("TESTING PLAYER INITIALIZATION")
print("=" * 60)

# Create player
player = Player(CharacterClass.IRONCLAD)
print(f"\n1. Player created:")
print(f"   - Name: {player.name}")
print(f"   - Class: {player.character_class.value}")
print(f"   - HP: {player.current_hp}/{player.max_hp}")
print(f"   - Deck size: {len(player.deck)}")

if len(player.deck) > 0:
    print(f"   - Cards in deck:")
    for card in player.deck:
        print(f"     * {card.name} (cost: {card.cost})")
else:
    print("   [WARNING] Deck is empty!")

print("\n" + "=" * 60)
print("TESTING COMBAT INITIALIZATION")
print("=" * 60)

# Create game state and combat
game_state = GameState(player)
game_state.start_act(1)

monsters = [Cultist()]
game_state.enter_combat(monsters)
combat = game_state.current_combat

print(f"\n2. Combat created:")
print(f"   - Phase: {combat.current_phase.value}")
print(f"   - Hand size: {len(combat.hand)}")
print(f"   - Draw pile size: {len(combat.draw_pile)}")

if len(combat.hand) > 0:
    print(f"   - Cards in hand:")
    for card in combat.hand:
        print(f"     * {card.name} (cost: {card.cost})")
else:
    print("   [ERROR] Hand is empty!")

print(f"\n   - Monsters: {[m.name for m in combat.monsters]}")
print(f"   - Player HP: {combat.player.current_hp}/{combat.player.max_hp}")

print("\n" + "=" * 60)
print("TESTING SERIALIZATION")
print("=" * 60)

state_dict = game_state.to_dict()
print(f"\n3. Game state serialized:")
print(f"   - Phase: {state_dict['phase']}")
print(f"   - Current combat hand size: {len(state_dict['current_combat']['hand']) if state_dict['current_combat'] else 'N/A'}")
print(f"   - Player HP: {state_dict['player']['hp']}/{state_dict['player']['max_hp']}")

if state_dict['current_combat']:
    print(f"   - Combat hand details:")
    for card in state_dict['current_combat']['hand']:
        print(f"     * {card['name']} (cost: {card['cost']})")
else:
    print("   [WARNING] No combat in state!")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
