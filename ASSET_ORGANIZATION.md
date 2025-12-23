# Asset Organization Summary

## Quick Start Guide

Your Holiday Panic Factory game now has a **fully modular asset and sound system**!

## What You Need to Create

### 1. Directory Structure

Create this folder structure in your project:

```
holiday-game/
└── assets/
    ├── backgrounds/
    ├── characters/
    ├── toys/
    ├── wrapping/
    ├── bows/
    └── sounds/
        ├── music/
        └── sfx/
```

**Windows Command:**
```cmd
mkdir assets
mkdir assets\backgrounds
mkdir assets\characters
mkdir assets\toys
mkdir assets\wrapping
mkdir assets\bows
mkdir assets\sounds
mkdir assets\sounds\music
mkdir assets\sounds\sfx
```

**Mac/Linux Command:**
```bash
mkdir -p assets/{backgrounds,characters,toys,wrapping,bows,sounds/{music,sfx}}
```

---

## 2. Asset Checklist

### Required Sprites (22 files)

**Toys - 18 sprites** (9 items × 2 variants each)
- [ ] `assets/toys/socks_good.png` (150×150px)
- [ ] `assets/toys/socks_bad.png` (150×150px)
- [ ] `assets/toys/ball_good.png` (150×150px)
- [ ] `assets/toys/ball_bad.png` (150×150px)
- [ ] `assets/toys/box_good.png` (150×150px)
- [ ] `assets/toys/box_bad.png` (150×150px)
- [ ] `assets/toys/robot_good.png` (200×200px)
- [ ] `assets/toys/robot_bad.png` (200×200px)
- [ ] `assets/toys/doll_good.png` (200×200px)
- [ ] `assets/toys/doll_bad.png` (200×200px)
- [ ] `assets/toys/bicycle_good.png` (200×200px)
- [ ] `assets/toys/bicycle_bad.png` (200×200px)
- [ ] `assets/toys/piano_good.png` (300×300px)
- [ ] `assets/toys/piano_bad.png` (300×300px)
- [ ] `assets/toys/trex_good.png` (300×300px)
- [ ] `assets/toys/trex_bad.png` (300×300px)
- [ ] `assets/toys/spaceship_good.png` (300×300px)
- [ ] `assets/toys/spaceship_bad.png` (300×300px)

**Wrapping - 2 sprites**
- [ ] `assets/wrapping/gold_foil.png` (250×150px)
- [ ] `assets/wrapping/torn_paper.png` (250×150px)

**Bows - 2 sprites**
- [ ] `assets/bows/satin_ribbon.png` (150×100px)
- [ ] `assets/bows/toilet_paper.png` (150×100px)

**Characters - 1 sprite**
- [ ] `assets/characters/elf_head.png` (200×200px)

---

### Optional Backgrounds (6 files)

- [ ] `assets/backgrounds/menu_bg.png` (1280×720px)
- [ ] `assets/backgrounds/briefing_easy_bg.png` (1280×720px) - Green themed
- [ ] `assets/backgrounds/briefing_standard_bg.png` (1280×720px) - Yellow themed
- [ ] `assets/backgrounds/briefing_nightmare_bg.png` (1280×720px) - Red themed
- [ ] `assets/backgrounds/playing_bg.png` (1280×720px)
- [ ] `assets/backgrounds/reveal_bg.png` (1280×720px)

---

### Optional Sounds (16 files)

**Music - 4 files** (.ogg format recommended)
- [ ] `assets/sounds/music/menu.ogg` - Calm, festive menu music
- [ ] `assets/sounds/music/briefing.ogg` - Upbeat order announcement
- [ ] `assets/sounds/music/gameplay.ogg` - Fast-paced, frantic workshop music
- [ ] `assets/sounds/music/reveal.ogg` - Suspenseful reveal music

**Sound Effects - 12 files** (.wav format recommended)
- [ ] `assets/sounds/sfx/button_press.wav` - Menu button click
- [ ] `assets/sounds/sfx/tick.wav` - Timer tick (optional)
- [ ] `assets/sounds/sfx/success.wav` - Success celebration
- [ ] `assets/sounds/sfx/fail.wav` - Failure sound
- [ ] `assets/sounds/sfx/countdown.wav` - **LOOPING** countdown warning
- [ ] `assets/sounds/sfx/siren.wav` - Nightmare order alert
- [ ] `assets/sounds/sfx/whoosh.wav` - Round start transition
- [ ] `assets/sounds/sfx/thump.wav` - Gift assembly thump
- [ ] `assets/sounds/sfx/wrap.wav` - Wrapping paper sound
- [ ] `assets/sounds/sfx/ribbon_tie.wav` - Bow tying sound
- [ ] `assets/sounds/sfx/error.wav` - Mistake/error sound
- [ ] `assets/sounds/sfx/perfect.wav` - Perfect score celebration

---

## 3. How the System Works

### Automatic Asset Loading

When you run the game, it automatically:

1. **Initializes managers** - Creates AssetManager and SoundManager
2. **Pre-loads all assets** - Loads sprites and sounds into memory
3. **Caches everything** - Stores in memory for fast access
4. **Handles missing files gracefully** - Prints warnings but continues

### Graceful Fallback

**If assets are missing:**
- Sprites → Shows placeholder text (current behavior)
- Backgrounds → Shows solid colors
- Sounds → Game continues silently

**You can test without any assets!** Just run the game as-is.

---

## 4. Updating Asset Paths

### To Use Real Sprites

**Option A: Use recommended file names** (no code changes needed)
- Just place files in the correct folders with the exact names listed above

**Option B: Use custom file names** (requires editing config.py)

Edit [config.py](config.py) and update the paths:

```python
ASSET_MAP = {
    "toys": {
        "socks": {
            "good": "assets/toys/my_custom_socks.png",  # Change this
            "bad": "assets/toys/my_bad_socks.png"       # And this
        },
        # ...
    },
}
```

---

## 5. File Format Requirements

### Images
- **Format**: PNG with alpha transparency
- **Color mode**: RGBA (32-bit)
- **Style**: Consistent across all assets (pixel art, cartoon, realistic, etc.)
- **Background**: Transparent (not white)

### Music
- **Format**: OGG Vorbis (best) or MP3
- **Sample Rate**: 44.1 kHz
- **Channels**: Stereo
- **Bitrate**: 128-192 kbps
- **Length**: 1-3 minutes, designed to loop seamlessly

### Sound Effects
- **Format**: WAV (uncompressed, fast loading)
- **Sample Rate**: 44.1 kHz
- **Channels**: Mono or Stereo
- **Bit Depth**: 16-bit
- **Length**: 0.1-2 seconds (short and punchy)

---

## 6. Current Configuration

All asset paths are defined in [config.py](config.py):

- **Lines 136-193**: `ASSET_MAP` - Toy, wrap, and bow sprites
- **Lines 220-235**: `SOUND_MAP` - Sound effect paths
- **Lines 237-243**: `MUSIC_MAP` - Background music paths
- **Lines 245-248**: `CHARACTER_ASSETS` - Character sprites
- **Lines 250-258**: `BACKGROUND_ASSETS` - Background images

---

## 7. Manager Classes

### AssetManager ([asset_manager.py](asset_manager.py))

**Key Methods:**
- `load_sprite(path, size)` - Load a sprite with optional resizing
- `get_sprite(type, name, variant)` - Get from ASSET_MAP
- `load_background(name, path)` - Load background image
- `preload_all_assets()` - Pre-load everything at startup

### SoundManager ([sound_manager.py](sound_manager.py))

**Key Methods:**
- `play_sound(name)` - Play one-shot sound effect
- `play_looping_sound(name)` - Start looping sound
- `stop_looping_sound(name)` - Stop looping sound
- `play_state_music(state)` - Auto-switch music by game state
- `set_music_volume(vol)` - Set music volume (0.0-1.0)
- `set_sfx_volume(vol)` - Set SFX volume (0.0-1.0)
- `toggle_mute()` - Mute/unmute all audio

See [SOUND_GUIDE.md](SOUND_GUIDE.md) for complete sound system documentation.

---

## 8. Testing Your Assets

### Test Sprites

1. Place ONE sprite in `assets/toys/socks_good.png`
2. Update [config.py](config.py):
   ```python
   "socks": {
       "good": "assets/toys/socks_good.png",  # Real file
       "bad": "PLACEHOLDER: Dirty Socks"      # Keep as placeholder
   }
   ```
3. Run the game and complete a round with socks
4. Check if your sprite appears in the reveal phase

### Test Sounds

1. Place ONE sound file in `assets/sounds/sfx/button_press.wav`
2. Run the game
3. Press ENTER at the menu
4. You should hear the button sound

### Check Console Output

Look for these messages:
```
Initializing Asset Manager...
Loading all game assets...
All toy sprites loaded and cached
Wrap and bow sprites loaded and cached
Asset loading complete!

Initializing Sound Manager...
Loading sound effects...
Loaded 12 sound effects
```

Any warnings indicate missing files.

---

## 9. Workflow Recommendations

### Phase 1: Core Sprites (Start Here)
1. Create the 18 toy sprites (good/bad variants)
2. Test in-game to see how they look
3. Adjust sizes if needed

### Phase 2: Wrapping & Bows
1. Create wrapping paper sprites (2 files)
2. Create bow sprites (2 files)
3. Test layering in reveal phase

### Phase 3: Character & UI
1. Create elf head sprite
2. Test in briefing screen
3. Add backgrounds if desired

### Phase 4: Sound Effects
1. Add critical sounds (button, success, fail)
2. Add looping countdown sound
3. Add specialty sounds (wrap, ribbon, etc.)

### Phase 5: Music
1. Add menu music
2. Add gameplay music
3. Add reveal music
4. Add briefing music

---

## 10. Quick Reference

| Asset Type | Count | Location | Format | Size |
|------------|-------|----------|--------|------|
| Toy Sprites | 18 | `assets/toys/` | PNG | 150-300px |
| Wrap Sprites | 2 | `assets/wrapping/` | PNG | 250×150px |
| Bow Sprites | 2 | `assets/bows/` | PNG | 150×100px |
| Character | 1 | `assets/characters/` | PNG | 200×200px |
| Backgrounds | 6 | `assets/backgrounds/` | PNG | 1280×720px |
| Music | 4 | `assets/sounds/music/` | OGG | 44.1kHz |
| Sound FX | 12 | `assets/sounds/sfx/` | WAV | 44.1kHz |

---

## Need Help?

- **Asset loading issues?** Check [asset_manager.py](asset_manager.py)
- **Sound not working?** Read [SOUND_GUIDE.md](SOUND_GUIDE.md)
- **Want code examples?** See [EXAMPLES.md](EXAMPLES.md)
- **General questions?** Check [README.md](README.md)

**Remember:** The game works perfectly fine without any assets! Add them at your own pace.
