"""
Comprehensive test suite for Slay the Spire 2
Tests all major game systems
"""

from app.game.engine import GameEngine
from app.game.cards import Strike, Bash, Defend
from app.game.monsters import Cultist, Worker
from app.game.relics import Burning, Rusted
from app.game.potions import HealthPotion, StrengthPotion
from app.utils.enums import GamePhase


def test_player_creation():
    """Test player initialization."""
    engine = GameEngine(ascension=0)
    player = engine.player
    
    assert player.max_hp == 80, "Ironclad should have 80 max HP"
    assert len(player.deck) == 9, "Starting deck should have 9 cards"
    assert len(player.relics) == 1, "Should start with 1 relic"
    print("✓ Player creation test passed")


def test_combat_initialization():
    """Test combat engine initialization."""
    engine = GameEngine()
    session = engine.create_session("test_session_1")
    
    assert session is not None, "Session should be created"
    assert session.act == 1, "Should start on Act 1"
    assert session.current_phase == GamePhase.MAP, "Should start on map"
    print("✓ Combat initialization test passed")


def test_combat_flow():
    """Test basic combat flow."""
    engine = GameEngine()
    session = engine.create_session("test_session_2")
    
    # Start combat
    engine.start_combat("test_session_2")
    
    assert session.current_combat is not None, "Combat should be started"
    assert len(session.current_combat.hand) > 0, "Should have hand"
    assert len(session.current_combat.monsters) > 0, "Should have enemies"
    print("✓ Combat flow test passed")


def test_card_playing():
    """Test playing cards in combat."""
    engine = GameEngine()
    engine.create_session("test_session_3")
    engine.start_combat("test_session_3")
    
    game_state = engine.get_session("test_session_3")
    initial_energy = game_state.current_combat.player_energy
    initial_hand_size = len(game_state.current_combat.hand)
    
    # Play first card
    success, message = engine.play_card("test_session_3", 0, 0)
    
    assert success == True, "Should successfully play card"
    assert game_state.current_combat.player_energy < initial_energy, "Energy should decrease"
    assert len(game_state.current_combat.hand) == initial_hand_size - 1, "Hand size should decrease"
    print("✓ Card playing test passed")


def test_turn_flow():
    """Test turn progression."""
    engine = GameEngine()
    engine.create_session("test_session_4")
    engine.start_combat("test_session_4")
    
    game_state = engine.get_session("test_session_4")
    initial_turn = game_state.current_combat.turn_number
    
    # Play until end of turn
    while game_state.current_combat.player_energy > 0 and len(game_state.current_combat.hand) > 0:
        engine.play_card("test_session_4", 0, 0)
    
    # End turn
    success, message = engine.end_turn("test_session_4")
    
    assert success == True, "Should end turn successfully"
    assert game_state.current_combat.turn_number > initial_turn, "Turn should increment"
    print("✓ Turn flow test passed")


def test_status_effects():
    """Test status effect system."""
    from app.game.status import Strength, Vulnerable, Poison
    
    engine = GameEngine()
    player = engine.player
    
    # Add strength
    player.add_status(Strength(-1, 5))
    assert "strength" in player.status_effects, "Strength should be added"
    assert player.status_effects["strength"].value == 5, "Strength value should be 5"
    
    # Add vulnerable
    player.add_status(Vulnerable(1, 2))
    assert "vulnerable" in player.status_effects, "Vulnerable should be added"
    
    # Stack effects
    player.add_status(Vulnerable(1, 1))
    assert player.status_effects["vulnerable"].value == 3, "Should stack to 3"
    
    print("✓ Status effects test passed")


def test_relics():
    """Test relic system."""
    engine = GameEngine()
    player = engine.player
    
    initial_relic_count = len(player.relics)
    relic = Rusted()
    player.add_relic(relic)
    
    assert len(player.relics) == initial_relic_count + 1, "Relic should be added"
    assert player.relics[-1].name == "Rusted Sword", "Relic name should match"
    print("✓ Relics test passed")


def test_monster_behavior():
    """Test monster AI."""
    cultist = Cultist()
    
    # Plan action
    cultist.plan_action()
    assert cultist.intent.value in ["buff", "attack"], "Intent should be set"
    
    # Execute action
    from app.game.combat import Combatant
    player = Combatant("Player", 80)
    initial_hp = player.current_hp
    
    cultist.execute_action(player)
    # HP might change depending on ritual state
    print("✓ Monster behavior test passed")


def test_deck_management():
    """Test deck operations."""
    engine = GameEngine()
    player = engine.player
    
    initial_size = len(player.deck)
    
    # Add card
    new_card = Strike()
    player.add_card(new_card)
    assert len(player.deck) == initial_size + 1, "Card should be added to deck"
    
    # Remove card
    player.remove_card(new_card.id)
    assert len(player.deck) == initial_size, "Card should be removed from deck"
    
    print("✓ Deck management test passed")


def test_potions():
    """Test potion system."""
    health_potion = HealthPotion(25)
    strength_potion = StrengthPotion(2)
    
    assert health_potion.effect_type == "heal", "Health potion type should be 'heal'"
    assert strength_potion.value == 2, "Strength potion value should be 2"
    assert health_potion.name == "Health Potion", "Name should match"
    
    print("✓ Potions test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("🧪 SLAY THE SPIRE 2 - TEST SUITE")
    print("=" * 50)
    print("")
    
    tests = [
        test_player_creation,
        test_combat_initialization,
        test_combat_flow,
        test_card_playing,
        test_turn_flow,
        test_status_effects,
        test_relics,
        test_monster_behavior,
        test_deck_management,
        test_potions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("")
    print("=" * 50)
    print(f"✅ TESTS PASSED: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ TESTS FAILED: {failed}/{len(tests)}")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
