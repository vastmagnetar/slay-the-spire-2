# 🎮 Quick Start Guide - Slay the Spire 2

## Installation & Launch

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Start the Server
```bash
python main.py
```

Or use the startup script:
```bash
bash start.sh
```

### 3️⃣ Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎮 How to Play

### Main Menu
- **New Run**: Start a fresh game
- **Ascension**: Select difficulty (0-20)
- **Settings**: Configure game options

### Character Selection
- **The Ironclad**: Strength-based heavy damage (implemented)
- **The Silent**: Poison & precision strikes (coming soon)

### Map Navigation
- Choose your path through the Spire
- Node types: Combat, Elite, Merchant, Rest, Event, Boss

### Combat
- **Play Cards**: Click cards or press 1-9
- **End Turn**: Click button or press Space/E
- **View Intents**: See enemy's planned action in the card at bottom

### Cards
- **Attacks**: Deal damage (scales with Strength)
- **Skills**: Gain block and utility (scales with Dexterity)
- **Powers**: Permanent game-changing effects

---

## 🧠 Strategy Tips

1. **Understand Intents**: Plan around what enemies will do
2. **Thin Your Deck**: Purchase card removals at the shop
3. **Stack Effects**: Combine status effects for massive damage
4. **Balance Block**: Defensive gameplay is key
5. **Relic Synergy**: Build your deck around relics

---

## 📊 Test the System

Run the test suite to verify all systems:
```bash
python test_game.py
```

Expected output: ✅ **10/10 TESTS PASSED**

---

## 🏗️ System Architecture

### Pillars Implemented ✅

1. **Combat Engine**
   - Intent system for fair combat
   - Energy economy (3/turn)
   - Status effects (10+ types)
   - Draw/discard with reshuffling

2. **Map & Progression**
   - Procedural map generation
   - 6 node types
   - Branching paths

3. **Progression & Scaling**
   - 15+ relics
   - 12+ potions
   - Card upgrades
   - Ascension levels (0-20)

4. **Modern Features**
   - Real-time WebSocket
   - Dark-themed UI
   - Responsive design
   - Keyboard shortcuts

---

## 📁 Project Files

```
slay-the-spire-2/
├── app/
│   ├── game/           # Core game logic
│   ├── websocket/      # Real-time communication
│   ├── utils/          # Constants & enums
│   └── static/         # Frontend (HTML/CSS/JS)
├── main.py             # Server entry point
├── test_game.py        # Test suite
└── requirements.txt    # Dependencies
```

---

## 🎯 What's Included

### Game Content
- ✅ 20+ cards (Ironclad)
- ✅ 10+ enemies with unique behaviors
- ✅ 15+ relics
- ✅ 12+ potions
- ✅ 10+ status effects

### Features
- ✅ Full combat system
- ✅ Procedural maps
- ✅ WebSocket real-time updates
- ✅ Dark-themed UI
- ✅ Session management
- ✅ Game state tracking

### Coming Soon
- 🔜 Silent character
- 🔜 Event nodes
- 🔜 Save/Load system
- 🔜 Statistics dashboard
- 🔜 Co-op support

---

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is occupied:
```bash
python -c "from app import create_app; app, socketio = create_app(); socketio.run(app, port=5001)"
```

### WebSocket Connection Issues
Check browser console (F12) for errors and ensure WebSocket is enabled.

### Python Module Errors
Ensure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

---

## 📚 Code Structure

### Game Engine
- `GameEngine`: Main orchestrator, session management
- `GameState`: Current run state
- `Player`: Player/Combatant class with deck

### Combat System
- `Combat`: Manages turn flow and hand
- `Combatant`: Base class for fighters
- `Card`: Playable effects
- `Monster`: Enemy with AI

### Game Data
- `StatusEffect`: Temporary conditions
- `Relic`: Passive abilities
- `Potion`: Consumable items

### UI & Network
- `WebSocket handlers`: Real-time game updates
- `UI management`: Canvas & DOM updates
- `Game state sync`: Client-server synchronization

---

## 💡 Development Notes

### Adding New Cards
```python
# In app/game/cards.py
class MyCard(Card):
    def __init__(self, upgrades=0):
        super().__init__(
            "Card Name", CardType.ATTACK, 
            cost=2, description="Does something"
        )
    
    def play(self, player, enemies, target_idx=0):
        # Your logic here
        pass
```

### Adding New Monsters
```python
# In app/game/monsters.py
class MyMonster(Monster):
    def __init__(self):
        super().__init__("Name", max_hp=100)
    
    def plan_action(self):
        self.intent = Intent.ATTACK
        self.intent_value = 10
    
    def execute_action(self, player):
        player.take_damage(10)
```

### Adding New Relics
```python
# In app/game/relics.py
class MyRelic(Relic):
    def __init__(self):
        super().__init__(
            "Relic Name", "tier",
            "Description of effect"
        )
```

---

## 🎓 Learning Resources

- Read `README.md` for full documentation
- Check `test_game.py` for usage examples
- Review `app/game/engine.py` for overall architecture
- Explore `app/static/js/` for UI/WebSocket patterns

---

## 🚀 Next Steps

1. **Play a Run**: Launch the game and reach Act 3
2. **Explore Code**: Read through `app/game/` modules
3. **Add Content**: Create new cards, relics, or monsters
4. **Extend UI**: Enhance visual feedback and animations
5. **Optimize**: Profile and improve performance

---

**Enjoy! 🎮 May your runs be victorious!**
