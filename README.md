# Holiday Panic Factory (Elf Panic!)

A 4-player local co-op party game where players act as elves on a malfunctioning assembly line. They must frantically construct, wrap, and decorate gifts before time runs out!

## Game Overview

**Core Hook**: Asymmetrical gameplay where if one player fails, the final gift is visibly ruined (e.g., a perfect T-Rex wrapped in dirty laundry).

**Dynamic Difficulty**: Orders range from simple socks (easy) to complex machinery (nightmare), drastically changing the input requirements mid-round.

## The Four Roles

### Player 1: The Builder (Button Masher)
- **Controls**: A and D keys (rapid alternating)
- **Objective**: Keep the quality bar filled above the "Quality Line"
- **Scaling**: Bar decays faster on harder orders, requiring constant stamina

### Player 2: The Wrapper (Timing Precision)
- **Controls**: SPACEBAR
- **Objective**: Hit Space when the cursor is in the Green Zone
- **Scaling**: Green zone shrinks from 30% (easy) to 5% (nightmare)

### Player 3: The Decorator (Pattern Recognition)
- **Controls**: Arrow Keys (↑↓←→)
- **Objective**: Enter the arrow sequence in exact order (mistakes reset progress)
- **Scaling**: 4-6 arrows (easy) up to 20-30 arrows (nightmare)

### Player 4: The Foreman (System Management)
- **Controls**: Numpad 4 (left) / Numpad 6 (right)
- **Objective**: Keep the needle balanced in the center zone
- **Scaling**: Needle drifts more aggressively on harder orders

## Installation

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Project Structure

```
holiday-game/
├── main.py              # Entry point - run this to start the game
├── game.py              # Main game logic and state management
├── players.py           # Individual player role classes
├── config.py            # Configuration and asset mapping
├── asset_manager.py     # Sprite loading and caching system
├── sound_manager.py     # Audio playback and music management
├── input_manager.py     # Input handling and key remapping system
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── SOUND_GUIDE.md       # Sound system documentation
├── INPUT_GUIDE.md       # Input system documentation
└── assets/              # Asset directory (create this for your files)
    ├── backgrounds/     # Background images
    ├── characters/      # Character sprites (elf head)
    ├── toys/            # Toy sprites (good/bad variants)
    ├── wrapping/        # Wrapping paper sprites
    ├── bows/            # Bow/ribbon sprites
    └── sounds/          # Audio files
        ├── music/       # Background music (.ogg)
        └── sfx/         # Sound effects (.wav)
```

## Modular Design

The game is built with a **fully modular architecture** with separate manager classes:

### Manager Classes

#### Asset Manager ([asset_manager.py](asset_manager.py))
- Handles loading and caching of all sprite assets
- Supports automatic pre-loading at startup
- Graceful fallback for missing files
- Size customization for different sprites
- Background image support

#### Sound Manager ([sound_manager.py](sound_manager.py))
- Background music with auto-switching by game state
- Sound effects (one-shot and looping)
- Volume control for music and SFX separately
- Mute/unmute toggle (press M)
- Countdown sound that loops when timer < 5 seconds
- See [SOUND_GUIDE.md](SOUND_GUIDE.md) for full documentation

#### Input Manager ([input_manager.py](input_manager.py))
- Centralized input handling for all players
- Action-based system (map actions, not raw keys)
- Easy key remapping without touching game code
- Gamepad support with auto-detection
- Frame-perfect input (pressed vs held)
- Player-specific convenience methods
- See [INPUT_GUIDE.md](INPUT_GUIDE.md) for full documentation

### Asset System
All assets are configured in [config.py](config.py) via the `ASSET_MAP` dictionary. Currently uses placeholder text, but can easily be replaced with sprites:

```python
ASSET_MAP = {
    "toys": {
        "socks": {
            "good": "PLACEHOLDER: Neat Socks",  # Replace with sprite path
            "bad": "PLACEHOLDER: Dirty Socks"   # Replace with sprite path
        },
        # ... more toys
    },
    "wraps": {
        "good": "PLACEHOLDER: Gold Foil",
        "bad": "PLACEHOLDER: Used Tissue"
    },
    "bows": {
        "good": "PLACEHOLDER: Satin Ribbon",
        "bad": "PLACEHOLDER: Live Snake"
    },
}
```

### Order Database
Orders are defined in `config.py` with all difficulty parameters:

```python
ORDERS = {
    OrderTier.EASY: [
        {
            "name": "Socks",
            "dialog": "Easy one! Just socks.",
            "p3_arrows": 4,
            "time_limit": 8,
            "p1_decay_rate": 0.3,
            "p2_zone_size": 0.3,
            "toy_asset": "socks",
        },
        # ... more orders
    ],
    # ... more tiers
}
```

### Player Classes
Each player role is a self-contained class in `players.py`:
- `Builder` - Handles P1 mechanics
- `Wrapper` - Handles P2 mechanics
- `Decorator` - Handles P3 mechanics
- `Foreman` - Handles P4 mechanics

Each class handles its own:
- Update logic
- Drawing/rendering
- Success evaluation
- Difficulty scaling

## How to Add Sprites

To replace placeholder assets with actual sprites:

1. Load your sprites in the appropriate player class or game state
2. Update the asset rendering in the `draw()` methods
3. Modify the `ASSET_MAP` in `config.py` to point to sprite file paths

Example:
```python
# In config.py
"socks": {
    "good": "assets/sprites/socks_good.png",
    "bad": "assets/sprites/socks_bad.png"
}

# In your drawing code
sprite = pygame.image.load(asset_path)
screen.blit(sprite, (x, y))
```

## Game States

The game flows through these states:
1. **MENU** - Title screen and instructions
2. **BRIEFING** - Shows the order with elf dialog (4 seconds)
3. **PLAYING** - Action phase where players complete their tasks
4. **REVEAL** - Shows the final gift and results (5 seconds)

## Customization

### Adjusting Difficulty Progression
Modify the tier selection logic in `game.py`:
```python
def start_new_round(self):
    if self.round_number <= 3:
        tier = OrderTier.EASY
    elif self.round_number <= 7:
        tier = OrderTier.STANDARD
    else:
        tier = OrderTier.NIGHTMARE
```

### Adding New Orders
Add entries to the `ORDERS` dictionary in `config.py` and corresponding asset mappings.

### Screen Layout
Quadrant positions can be adjusted in `config.py`:
```python
QUADRANT_1 = (0, 100, 640, 310)  # x, y, width, height
```

## Controls Summary

| Player | Role | Controls |
|--------|------|----------|
| P1 | Builder | A, D |
| P2 | Wrapper | SPACE |
| P3 | Decorator | Arrow Keys |
| P4 | Foreman | Numpad 4, 6 |

**General**: ESC to quit, ENTER to start/continue

## License

This is a game design implementation based on the "Elf Panic" game design document.

## Quick Start: Adding Assets

### Create Asset Folders

Run this helper script to create the directory structure:

```bash
python create_asset_folders.py
```

Or see [ASSET_ORGANIZATION.md](ASSET_ORGANIZATION.md) for manual setup instructions.

### Add Your Assets

1. **Place sprite files** in `assets/toys/`, `assets/wrapping/`, `assets/bows/`
2. **Place sound files** in `assets/sounds/music/` and `assets/sounds/sfx/`
3. **Place backgrounds** in `assets/backgrounds/` (optional)

The game automatically loads all assets at startup and handles missing files gracefully!

See the complete asset checklist in [ASSET_ORGANIZATION.md](ASSET_ORGANIZATION.md).

## Documentation

- [README.md](README.md) - This file, game overview
- [ASSET_ORGANIZATION.md](ASSET_ORGANIZATION.md) - Complete asset setup guide
- [SOUND_GUIDE.md](SOUND_GUIDE.md) - Sound system documentation
- [EXAMPLES.md](EXAMPLES.md) - Code examples for extending the game

## Future Enhancements

- ✅ ~~Add sprite assets for all placeholders~~ - System implemented!
- ✅ ~~Add sound effects and music~~ - Fully working!
- Add particle effects for successes/failures
- Add conveyor belt animations in reveal phase
- Add more visual feedback (screen shake, flashing for nightmare orders)
- Add end-game statistics and high scores
- Add volume controls in settings menu
- Add player customization (avatar selection)
