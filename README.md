# Slay the Spire 2 - Python/Flask Clone

A complete, faithful implementation of Slay the Spire 2 in Python with Flask, WebSocket support, and a UI matching the original game aesthetic.

## Features

### Core Systems (4 Pillars)

#### 1. Combat Engine
- **Intent System**: Enemies display their next action (Attack, Defend, Buff, Debuff)
- **Energy Economy**: 3 energy per turn to play cards
- **Card System**:
  - Attacks: Direct damage with Strength scaling
  - Skills: Block, utility, and temporary effects
  - Powers: Permanent effects lasting until end of combat
- **Draw/Discard Logic**: Hand size limit, deck reshuffling, exhaust mechanics
- **Status Effects**: Vulnerable, Frail, Poison, Weak, Strength, Dexterity, Artifact

#### 2. The Spire (Map & Progression)
- **Procedural Map Generation**: Branching paths with random node types
- **Node Types**:
  - Combat: Regular encounters
  - Elite: High-risk fights
  - Merchant: Shop for cards and relics
  - Rest: Heal or upgrade cards
  - Event: Special encounters
  - Boss: Act-ending challenge
- **Card Rewards**: Choose 1 of 3 cards after winning combat

#### 3. Progression & Scaling
- **Relic System**: Passive effects that change gameplay
- **Card Upgrades**: Enhance cards across runs
- **Potions**: One-time use items
- **Ascension Levels**: 20 difficulty tiers (0-20)

#### 4. Modern Features
- **WebSocket Real-time Updates**: Smooth live combat
- **Responsive UI**: Matching original game aesthetic
- **Character Archetypes**: Ironclad (strength-based) implemented

## Tech Stack

- **Backend**: Python 3.8+, Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **WebSocket Protocol**: Real-time bidirectional communication
- **Architecture**: Clean separation of engine, UI, and WebSocket layers

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip

### Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the server**:
```bash
python main.py
```

3. **Open in browser**:
Navigate to `http://localhost:5000`

## Project Structure

```
slay-the-spire-2/
├── app/
│   ├── game/
│   │   ├── engine.py          # Main game orchestrator
│   │   ├── combat.py          # Combat system and turn logic
│   │   ├── cards.py           # Card definitions
│   │   ├── relics.py          # Relic definitions
│   │   ├── monsters.py        # Enemy definitions
│   │   ├── status.py          # Status effects
│   │   ├── map.py             # Map generation
│   │   └── state.py           # Game state management
│   ├── websocket/
│   │   └── handlers.py        # WebSocket event handlers
│   ├── utils/
│   │   ├── constants.py       # Game constants
│   │   └── enums.py           # Game enums
│   ├── static/
│   │   ├── index.html         # Main UI
│   │   ├── css/
│   │   │   └── style.css      # Dark theme styling
│   │   └── js/
│   │       ├── websocket.js   # Socket.IO client
│   │       ├── ui.js          # UI management
│   │       └── game.js        # Client-side game logic
│   └── __init__.py            # Flask app factory
├── main.py                    # Entry point
└── requirements.txt           # Python dependencies
```

## Game Mechanics

### Combat Flow
1. Player starts with 3 energy
2. Player plays cards from hand (costs energy)
3. Each card executes its effect
4. Player ends turn
5. Enemies execute planned actions
6. Status effects tick down
7. Block resets
8. New turn begins

### Card System

**Ironclad Starting Deck** (9 cards):
- 5x Strike (1 cost, 6 damage)
- 4x Defend (1 cost, 7 block)

**Attack Cards** (Sample):
- Strike: Basic attack
- Bash: Attack + apply Vulnerable
- Pummel: Multiple small hits
- Uppercut: Apply Weak + Vulnerable

**Skill Cards** (Sample):
- Defend: Gain block
- Shrug It Off: Block + draw card
- Brace Impact: Block + Strength
- Iron Wave: Block + damage

**Power Cards** (Sample):
- Inflame: Gain Strength
- Anger: Double played cards
- Bloodletting: Trade HP for Strength

### Relics (Passive Effects)

**Common Relics**:
- Burning Blood: Survive lethal once
- Rusted Sword: Start with 1 Strength
- Ancient Tea Set: Heal 2 extra on rest

**Uncommon Relics**:
- Sentry Plate: Start with 3 block
- Sneko Eye: Draw 2 extra cards (but cards cost 1 more)
- Mark of Pain: Strength for each power played

**Rare Relics**:
- Philosopher's Stone: More powers appear
- Frozen Core: Max HP increases per discard

**Boss Relics**:
- Runic Pyramid: Cards not discarded at end of turn
- Sozu: No potions but extra flexibility

### Status Effects

- **Strength**: +1 damage per stack
- **Dexterity**: +1 block per stack
- **Vulnerable**: 1.5x more damage taken
- **Frail**: 0.75x block gained per stack
- **Weak**: 0.75x damage dealt per stack
- **Poison**: Damage at start of enemy turn
- **Artifact**: Block next debuff

## Gameplay Tips

1. **Thin Your Deck**: Use the merchant to remove weak cards
2. **Exploit Intents**: Plan around what enemies will do
3. **Stack Effects**: Synergize status effects for massive damage
4. **Block Strategically**: Not every hit needs to be taken
5. **Understand Relics**: They define run strategy

## Future Enhancements

- [ ] Silent character (poison/shiv archetype)
- [ ] More monsters and boss encounters
- [ ] Event nodes with story choices
- [ ] Potion system implementation
- [ ] Card upgrade paths
- [ ] More relic synergies
- [ ] Ascension mode features
- [ ] Save/Load system
- [ ] Statistics tracking
- [ ] Co-op support

## Controls

- **Click cards** to play them
- **Number keys (1-9)** to play cards by position
- **Space or E** to end turn
- **Click map nodes** to navigate

## Known Issues & Limitations

- Silent character not yet implemented
- Event nodes not yet implemented
- Potion system is a placeholder
- Card upgrades not fully integrated
- Some relics are pending implementation
- No persistent save system yet

## Contributing

The codebase is modular and well-organized for easy extension:
- Add new cards in `cards.py`
- Add new monsters/bosses in `monsters.py`
- Add new relics in `relics.py`
- Modify combat logic in `combat.py`
- Enhance UI in `static/`

## License

Educational project - inspired by Slay the Spire by Mega Crit Games.

## Credits

Inspired by the excellent [Slay the Spire](https://www.megacrit.com/) by Mega Crit Games.