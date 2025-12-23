# Holiday Panic Factory - System Architecture

## Overview

The game is built with a **fully modular, manager-based architecture** that separates concerns and makes it easy to extend functionality.

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    (Entry Point)                             │
│                                                              │
│  - Initializes pygame                                        │
│  - Creates AssetManager                                      │
│  - Creates SoundManager                                      │
│  - Creates Game instance                                     │
│  - Runs main game loop                                       │
└───────────────┬─────────────────────────────┬────────────────┘
                │                             │
                │                             │
      ┌─────────▼──────────┐        ┌─────────▼─────────┐
      │  AssetManager      │        │  SoundManager     │
      │  asset_manager.py  │        │  sound_manager.py │
      ├────────────────────┤        ├───────────────────┤
      │ • load_sprite()    │        │ • play_sound()    │
      │ • get_sprite()     │        │ • play_music()    │
      │ • load_background()│        │ • set_volume()    │
      │ • preload_all()    │        │ • toggle_mute()   │
      └──────────┬─────────┘        └─────────┬─────────┘
                 │                            │
                 │                            │
                 └────────────┬───────────────┘
                              │
                    ┌─────────▼──────────┐
                    │      Game          │
                    │     game.py        │
                    ├────────────────────┤
                    │ State Management:  │
                    │ • MENU             │
                    │ • BRIEFING         │
                    │ • PLAYING          │
                    │ • REVEAL           │
                    │                    │
                    │ Player Instances:  │
                    │ • Builder (P1)     │
                    │ • Wrapper (P2)     │
                    │ • Decorator (P3)   │
                    │ • Foreman (P4)     │
                    └──────────┬─────────┘
                               │
                    ┌──────────▼─────────────────────────┐
                    │        players.py                  │
                    ├────────────────────────────────────┤
                    │                                    │
                    │  ┌─────────────┐  ┌─────────────┐ │
                    │  │  Builder    │  │  Wrapper    │ │
                    │  │ (P1)        │  │ (P2)        │ │
                    │  │ • Quality   │  │ • Timing    │ │
                    │  │   bar       │  │   cursor    │ │
                    │  └─────────────┘  └─────────────┘ │
                    │                                    │
                    │  ┌─────────────┐  ┌─────────────┐ │
                    │  │ Decorator   │  │  Foreman    │ │
                    │  │ (P3)        │  │ (P4)        │ │
                    │  │ • Arrow     │  │ • Gauge     │ │
                    │  │   sequence  │  │   balance   │ │
                    │  └─────────────┘  └─────────────┘ │
                    └────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        config.py                             │
│                  (Configuration Hub)                         │
├─────────────────────────────────────────────────────────────┤
│ • ASSET_MAP           - Sprite file paths                   │
│ • SOUND_MAP           - Sound effect paths                  │
│ • MUSIC_MAP           - Music file paths                    │
│ • BACKGROUND_ASSETS   - Background image paths              │
│ • CHARACTER_ASSETS    - Character sprite paths              │
│ • ORDERS              - Order database (all tiers)          │
│ • Colors              - Color definitions                   │
│ • Screen layout       - Quadrant positions                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Game Initialization
```
1. main.py starts
2. Creates AssetManager
   └─> Pre-loads all sprites (toys, wraps, bows, characters)
3. Creates SoundManager
   └─> Pre-loads all sound effects
4. Creates Game(asset_manager, sound_manager)
   └─> Creates 4 player instances
   └─> Starts menu music
5. Enters game loop
```

### Round Flow
```
MENU State
   │
   ├─> User presses ENTER
   │   └─> sound_manager.play_sound('button_press')
   │
   ▼
BRIEFING State (4 seconds)
   │
   ├─> Displays order details
   ├─> Shows elf character (from asset_manager)
   ├─> Plays briefing music
   └─> Plays siren if NIGHTMARE tier
   │
   ▼
PLAYING State (8-20 seconds)
   │
   ├─> Plays gameplay music
   ├─> All 4 players update in parallel
   ├─> Timer counts down
   └─> When timer < 5s: plays looping countdown
   │
   ▼
REVEAL State (5 seconds)
   │
   ├─> Stops countdown sound
   ├─> Plays reveal music
   ├─> Evaluates each player's success/failure
   ├─> Looks up assets from ASSET_MAP
   ├─> Displays 3-layer gift (toy + wrap + bow)
   ├─> Plays success/fail sound based on score
   └─> Shows elf commentary
   │
   └─> Loop back to BRIEFING (next round)
```

## Module Responsibilities

### main.py
**Role:** Application entry point and main loop
- Initialize pygame
- Create manager instances
- Handle window events (quit, key presses)
- Run game update/draw loop at 60 FPS
- Clean up on exit

### config.py
**Role:** Central configuration hub
- All game constants
- Asset path definitions
- Order database
- Color palette
- Screen layout coordinates
- No game logic, pure data

### asset_manager.py
**Role:** Sprite and image loading
- Load and cache PNG sprites
- Resize sprites to specified dimensions
- Load background images
- Provide get methods for easy access
- Handle missing files gracefully
- No rendering logic, only loading

### sound_manager.py
**Role:** Audio playback and control
- Load and cache sound files
- Play one-shot sound effects
- Play looping sound effects
- Control background music
- Volume control (music and SFX separately)
- Mute/unmute functionality
- Auto-switch music by game state

### game.py
**Role:** Game state management and orchestration
- Manages game states (MENU, BRIEFING, PLAYING, REVEAL)
- Owns all 4 player instances
- Handles order selection and tier progression
- Evaluates round results
- Triggers sound effects and music changes
- Coordinates rendering for each state
- Uses asset_manager to display sprites
- Uses sound_manager for audio

### players.py
**Role:** Individual player mechanics
- 4 independent player classes
- Each handles its own:
  - Input handling
  - State updates
  - Drawing/rendering
  - Success evaluation
  - Difficulty scaling
- No cross-player dependencies

## Key Design Patterns

### Manager Pattern
- **AssetManager** and **SoundManager** are singleton-like instances
- Passed to Game instance at creation
- Centralized resource management
- Easy to extend with new asset types

### State Pattern
- Game uses clear state machine (MENU → BRIEFING → PLAYING → REVEAL)
- Each state has its own update and draw logic
- State transitions trigger music changes

### Data-Driven Design
- All orders defined in config.py data structures
- Easy to add new orders without code changes
- Asset paths externalized to config
- Difficulty parameters tunable in data

### Graceful Degradation
- Missing sprites → fallback to text placeholders
- Missing sounds → game continues silently
- Missing backgrounds → solid color fallback
- Game always playable, assets are optional enhancements

## Extension Points

### Adding New Player Role
1. Create new class in players.py inheriting from Player
2. Implement update(), draw(), check_success()
3. Add instance to Game class
4. Add quadrant layout to config.py

### Adding New Asset Type
1. Add paths to config.py (ASSET_MAP or new dict)
2. Add loading method to asset_manager.py if needed
3. Use asset_manager.load_sprite() in game code

### Adding New Sound Event
1. Add sound file path to SOUND_MAP in config.py
2. Call sound_manager.play_sound('name') at event location
3. No changes to sound_manager.py needed

### Adding New Game State
1. Add state to GameState class in config.py
2. Add update logic in game.py update() method
3. Add draw logic in game.py draw() method
4. Add music to MUSIC_MAP if needed

## Performance Considerations

### Asset Loading
- All assets pre-loaded at startup (1-2 second load time)
- Sprites cached in memory for instant access
- No disk I/O during gameplay
- Smooth 60 FPS performance

### Sound System
- Sounds pre-loaded at startup
- Pygame mixer handles concurrent playback
- Music streamed (not fully loaded into RAM)
- Looping sounds managed via channel tracking

### Rendering
- Direct pygame drawing (rectangles, text)
- Sprite blitting when assets available
- No complex rendering pipeline
- Minimal CPU usage

## File Dependencies

```
main.py
 ├─> pygame
 ├─> config.py
 ├─> asset_manager.py
 ├─> sound_manager.py
 └─> game.py
      ├─> config.py
      └─> players.py
           └─> config.py

asset_manager.py
 ├─> pygame
 └─> config.py (ASSET_MAP)

sound_manager.py
 └─> pygame.mixer

config.py
 └─> (no dependencies)

players.py
 ├─> pygame
 └─> config.py
```

## Testing Workflow

1. **Without Assets** - Run game with placeholders
2. **Add One Sprite** - Test asset_manager loading
3. **Add One Sound** - Test sound_manager playback
4. **Add Full Set** - Test complete experience
5. **Test Graceful Degradation** - Remove files, ensure no crashes

## Memory Footprint

Approximate memory usage:
- Code: < 1 MB
- Sprites (18 toys + wraps + bows): ~2-5 MB
- Backgrounds (6 images): ~5-10 MB
- Sounds (12 effects): ~1-2 MB
- Music (4 tracks, streamed): ~1 MB in RAM

**Total:** ~10-20 MB typical, scales with asset quality

## Conclusion

This architecture provides:
- **Modularity** - Easy to understand and modify
- **Extensibility** - Simple to add new features
- **Maintainability** - Clear separation of concerns
- **Testability** - Each module can be tested independently
- **Robustness** - Graceful handling of missing resources

The manager pattern keeps resource management clean, while the data-driven design makes content updates easy without touching code!
