# Deep Core Quest 🪨⛏️💎

An incremental mining game where you dig deep into a procedurally generated underground world to extract valuable resources, unlock powerful upgrades, and uncover ancient secrets.

![Game Screenshot](https://via.placeholder.com/800x450?text=Deep+Core+Quest)

## 🎮 Features

### Core Mechanics
- **Manual & Automated Mining**: Start by clicking to mine blocks, then unlock drones, drills, and robotic arms for passive resource generation
- **50+ Unique Upgrades**: Comprehensive skill tree with speed boosts, power multipliers, efficiency improvements, and special abilities
- **Procedurally Generated World**: Infinite underground with 7 distinct biomes/layers, each with unique resources and challenges
- **Idle Progression**: Continue earning resources while offline (up to 8 hours)
- **Prestige System**: Reset your progress at depth 1000m for permanent multipliers

### Resources
- **Iron** 🔨: Basic material found near the surface
- **Copper** 🔶: Common metal starting at 50m depth  
- **Gold** 💛: Precious metal found below 150m
- **Crystal** 💎: Rare gems in volcanic and crystal caverns (500m+)
- **Artifact** 🏺: Ancient relics from depths beyond 750m

### World Layers
1. **Surface** (0-50m): Rocky soil with iron and sparse copper
2. **Cave** (50-150m): Dark caverns with iron, copper, and hints of gold
3. **Deep Cave** (150-300m): Dense rock formations rich in copper and gold
4. **Volcanic** (300-500m): Molten depths with abundant gold and crystal veins
5. **Crystal Caverns** (500-750m): Glittering formations packed with crystals
6. **Ancient Ruins** (750-1000m): Mysterious structures hiding artifacts
7. **Core** (1000m+): The endless abyss with maximum rewards

### Upgrade Categories
- **Mining Power**: Increase damage per click (10+ upgrades)
- **Mining Speed**: Mine faster with reduced cooldowns (8+ upgrades)
- **Automation**: Unlock passive mining systems (12+ upgrades)
- **Resource Multipliers**: Boost specific resource yields (10+ upgrades)
- **Efficiency**: Global production multipliers (6+ upgrades)
- **Depth Access**: Unlock deeper layers (5+ upgrades)
- **Special Abilities**: Seismic blasts, mineral scanners, fortune boosts (6+ upgrades)
- **Critical Strikes**: Chance for bonus damage and resources (5+ upgrades)

## 📋 Requirements

### Python Version
- **Python 3.12.x recommended** (tested and stable)
- Python 3.10+ supported
- ⚠️ **Python 3.14+** may have compatibility issues with pygame (use 3.12 if you encounter font errors)

### System Dependencies
- **Linux/Ubuntu**: `sudo apt-get install python3-dev gcc-12 libsdl2-dev`
- **macOS**: `brew install python@3.12 sdl2`
- **Windows**: Python 3.12 installer from python.org

### Python Packages
- pygame >= 2.5.0
- noise >= 1.2.2

## 🚀 Installation

### Quick Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/jeffpignataro/deep_core_quest.git
cd deep_core_quest

# Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Troubleshooting

**Font Import Error (Python 3.14+)**
```bash
# Use Python 3.12 instead
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**SDL2 Missing (Linux)**
```bash
sudo apt-get update
sudo apt-get install python3-dev gcc-12 libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

**Performance Warning (AVX2)**
```bash
# Optional: Rebuild pygame with AVX2 support
PYGAME_DETECT_AVX2=1 pip install --no-binary :all: pygame
```

## 🎯 How to Play

### Controls
- **Left Click** (on world): Mine the block in front of you
- **Left Click** (on upgrade): Purchase upgrade if you can afford it
- **ESC**: Quit game
- **Ctrl+S**: Manual save (auto-saves on exit)

### Getting Started
1. Click on the rocky world (left side of screen) to mine blocks
2. Collect iron from destroyed blocks
3. Purchase upgrades from the upgrade panel (right side)
4. Unlock automation upgrades to earn passive income
5. Descend deeper to access better resources
6. Reach 1000m depth to unlock prestige

### Tips
- Focus on mining power and speed upgrades early
- Unlock automation ASAP for passive income
- Balance depth progression with upgrade purchases
- Use prestige when you hit a wall (~1000m depth)
- Offline progression caps at 8 hours

## 🧮 Game Balance

### Resource Generation Formula
```
base_amount * depth_scaling^(depth/100) * upgrade_multipliers * prestige_multiplier
```

### Mining Power Calculation
```
total_power = base_power + Σ(power_upgrades) + combo_bonuses
damage_per_hit = total_power * (crit_multiplier if crit else 1.0)
```

### Passive Generation
```
rate_per_second = Σ(automation_upgrades) * efficiency_multipliers * prestige_mult
offline_earnings = rate_per_second * min(offline_time, 8_hours)
```

### Prestige Multiplier
```
multiplier = 1.5^prestige_level
```

## 🗺️ Gameplay Loop

```
┌──────────────────────────────────────────────────────┐
│  Manual Mining → Collect Resources → Buy Upgrades   │
│         ↓                                           │
│  Unlock Automation → Passive Income → Deeper Access │
│         ↓                                           │
│  Find Rare Resources → Unlock Special Abilities     │
│         ↓                                           │
│  Reach Core (1000m) → Prestige → Permanent Bonuses  │
│         ↓                                           │
│  Repeat with Multipliers → Faster Progression       │
└──────────────────────────────────────────────────────┘
```

## 📊 Sample Upgrade Tree

```
Manual Mining Tier 1
├─ Sharper Pickaxe (10 levels) → +1 power each
├─ Faster Swings (10 levels) → +10% speed each
└─ Iron Detector (5 levels) → +20% iron yield
    └─ Copper Unlock → Access copper resource
        └─ Gold Unlock → Access gold resource (requires depth 100m)
            └─ Crystal Unlock → Access crystals (requires depth 500m)

Automation Tier 2
├─ Basic Drill → +0.5 resources/sec
├─ Improved Drill (10 levels) → +1.0/sec each
└─ Conveyor Belt (5 levels) → +50% collection
    └─ Robotic Arm → +5/sec
        └─ Mega Drill Array → +50/sec
            └─ Hyper Drill (10 levels) → +100/sec each

Special Abilities Tier 3+
├─ Seismic Blast → Reveals hidden veins
├─ Mineral Scanner → Shows resource locations
├─ Critical Mining (10 levels) → +5% crit chance
└─ Critical Power (5 levels) → Increases crit multiplier
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Tests cover:
- Resource generation and spending
- Upgrade purchase and effects
- Save/load functionality
- Prestige mechanics
- World generation consistency

## 🔮 Future Expansions

Potential features for future versions:

### Multiplayer
- Co-op mining with shared world
- Resource trading between players
- Competitive leaderboards

### Additional Content
- Boss encounters at layer transitions
- Collectible lore items revealing story
- Seasonal events and limited-time upgrades
- Achievement system with rewards

### Polish
- Animated sprites and particle effects
- Dynamic soundtrack per biome
- Sound effects for mining, upgrades, discoveries
- Improved visual feedback for progression

## 🎨 Art & Design Philosophy

**Visual Style**: Retro pixel art with vibrant underground palettes  
**Sound Design**: Satisfying mining SFX + relaxing ambient music  
**Accessibility**: Clear UI, colorblind-friendly, keyboard/mouse support  
**Balance**: Addictive yet fair, no pay-to-win elements

## 💡 Inspiration

Deep Core Quest draws inspiration from:
- **Mr. Mine**: Deep mining mechanics and prestige system
- **Diggy's Adventure**: Layer-based progression
- **Cookie Clicker**: Incremental upgrade philosophy
- **Minecraft**: Block-breaking satisfaction

## 📄 License

MIT License - Feel free to fork, modify, and share!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📬 Contact

Created by Jeff Pignataro  
GitHub: [@jeffpignataro](https://github.com/jeffpignataro)

---

**Enjoy mining!** 🪨⛏️💎
