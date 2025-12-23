# Sound Manager Guide

## Overview

The Holiday Panic Factory now includes a fully modular **Sound Manager** that handles:
- Background music with looping and fade effects
- Sound effects (one-shot and looping)
- Volume control for music and SFX separately
- Mute/unmute functionality
- Graceful fallback when sound files are missing

## Directory Structure

Place your sound files in the following structure:

```
assets/
└── sounds/
    ├── music/
    │   ├── menu.ogg          # Menu screen music
    │   ├── briefing.ogg      # Order briefing music
    │   ├── gameplay.ogg      # Action phase music
    │   └── reveal.ogg        # Results reveal music
    │
    └── sfx/
        ├── button_press.wav   # UI button/menu selection
        ├── tick.wav           # Timer tick (optional)
        ├── success.wav        # Success sound
        ├── fail.wav           # Failure sound
        ├── countdown.wav      # 5-second countdown warning
        ├── siren.wav          # Nightmare order alert
        ├── whoosh.wav         # Round start transition
        ├── thump.wav          # Gift assembly sound
        ├── wrap.wav           # Wrapping sound
        ├── ribbon_tie.wav     # Bow tying sound
        ├── error.wav          # Error/mistake sound
        └── perfect.wav        # Perfect score celebration
```

## Sound File Formats

### Music Files (.ogg recommended)
- **Format**: OGG Vorbis (best compression, looping support)
- **Alternative**: MP3, WAV (larger file sizes)
- **Sample Rate**: 44.1 kHz
- **Channels**: Stereo (2 channels)
- **Bitrate**: 128-192 kbps for music

### Sound Effects (.wav recommended)
- **Format**: WAV (fast loading, no decoding overhead)
- **Alternative**: OGG for longer effects
- **Sample Rate**: 44.1 kHz
- **Channels**: Mono or Stereo
- **Bit Depth**: 16-bit

## How It Works

### Automatic Music Changes
The sound manager automatically switches music based on game state:

- **Menu State** → plays `menu.ogg` (looping)
- **Briefing State** → plays `briefing.ogg` (looping)
- **Playing State** → plays `gameplay.ogg` (looping)
- **Reveal State** → plays `reveal.ogg` (looping)

Music fades in over 500ms when changing tracks.

### Sound Effects Triggered By Events

| Event | Sound | Type |
|-------|-------|------|
| Press ENTER (menu/continue) | `button_press` | One-shot |
| Round starts | `whoosh` | One-shot |
| Nightmare order appears | `siren` | One-shot |
| Timer < 5 seconds | `countdown` | **Looping** |
| Perfect score (4/4) | `perfect` | One-shot |
| Good score (2-3/4) | `success` | One-shot |
| Bad score (0-1/4) | `fail` | One-shot |

### Looping Sounds

The countdown sound is a **looping sound effect** that:
- Starts when timer drops below 5 seconds
- Automatically stops when the round ends
- Only plays once (won't restart if already playing)

This creates tension and urgency during the final seconds!

## Configuration

All sound paths are defined in [config.py](config.py):

```python
# Sound Effects Map
SOUND_MAP = {
    'button_press': 'assets/sounds/sfx/button_press.wav',
    'countdown': 'assets/sounds/sfx/countdown.wav',
    # ... more sounds
}

# Music Map
MUSIC_MAP = {
    'menu': 'assets/sounds/music/menu.ogg',
    'playing': 'assets/sounds/music/gameplay.ogg',
    # ... more music
}
```

To add a new sound:
1. Add the file to `assets/sounds/sfx/` or `assets/sounds/music/`
2. Add an entry to `SOUND_MAP` or `MUSIC_MAP` in config.py
3. Use `sound_manager.play_sound('your_sound_name')` in your code

## Sound Manager API

The `SoundManager` class is available in `game.py` as `self.sound_manager`.

### Playing Sound Effects

```python
# One-shot sound
self.sound_manager.play_sound('success')

# Looping sound effect
self.sound_manager.play_looping_sound('countdown')

# Stop a looping sound
self.sound_manager.stop_looping_sound('countdown')

# Stop all looping sounds
self.sound_manager.stop_all_looping_sounds()
```

### Playing Music

```python
# Play music by state name (auto-switches)
self.sound_manager.play_state_music('menu')

# Or play specific music with custom settings
self.sound_manager.play_music(
    name='boss_music',
    path='assets/sounds/music/boss.ogg',
    loops=-1,      # -1 = infinite, 0 = once, N = N times
    fade_ms=1000   # Fade in over 1 second
)

# Stop music
self.sound_manager.stop_music(fade_ms=500)  # Fade out over 500ms

# Pause/unpause
self.sound_manager.pause_music()
self.sound_manager.unpause_music()
```

### Volume Control

```python
# Set music volume (0.0 to 1.0)
self.sound_manager.set_music_volume(0.5)  # 50%

# Set sound effects volume (0.0 to 1.0)
self.sound_manager.set_sfx_volume(0.8)  # 80%

# Toggle mute (mutes both music and SFX)
is_muted = self.sound_manager.toggle_mute()
```

## Adding Sounds to Game Events

### Example: Add sound when player succeeds at a task

In [players.py](players.py), you could add:

```python
# In the Wrapper class
def update(self, dt, keys):
    if keys[pygame.K_SPACE] and not self.has_pressed:
        self.has_pressed = True
        self.press_position = self.cursor_position

        # Play wrap sound when player presses space
        # (You'd need to pass sound_manager to player classes)
        if self.sound_manager:
            self.sound_manager.play_sound('wrap')
```

### Example: Add tick sound to timer

In [game.py](game.py) update method:

```python
elif self.state == GameState.PLAYING:
    previous_second = int(self.state_timer)
    self.state_timer -= dt
    current_second = int(self.state_timer)

    # Play tick when second changes
    if previous_second != current_second and current_second > 0:
        if self.sound_manager:
            self.sound_manager.play_sound('tick')
```

## Fallback Behavior

The sound manager handles missing files gracefully:

1. If a sound file doesn't exist, it prints a warning and continues
2. The game will work perfectly fine without any sound files
3. No crashes or errors - sounds are "nice to have"

Example output when files are missing:
```
Warning: Sound file not found: assets/sounds/sfx/button_press.wav
Warning: Music file not found: assets/sounds/music/menu.ogg
```

## Performance Tips

1. **Pre-load sounds** - All sounds are pre-loaded at startup, so there's no lag during gameplay
2. **Use OGG for music** - Better compression than WAV, smaller file sizes
3. **Use WAV for short SFX** - Fast loading, no decoding needed
4. **Limit looping sounds** - Only use for continuous effects (countdown, sirens)
5. **Keep files small** - Aim for under 1MB per music track, under 100KB per SFX

## Volume Mixing Recommendations

Suggested volume levels:

```python
# At game startup
sound_manager.set_music_volume(0.6)   # 60% - background music
sound_manager.set_sfx_volume(0.8)     # 80% - sound effects louder than music
```

This ensures SFX are prominent without drowning out the music.

## Advanced: Custom Sound Events

You can create your own sound events by modifying [config.py](config.py):

```python
SOUND_MAP = {
    # ... existing sounds ...
    'custom_explosion': 'assets/sounds/sfx/boom.wav',
    'custom_cheer': 'assets/sounds/sfx/crowd_cheer.wav',
}
```

Then in your code:
```python
if special_event_happened:
    self.sound_manager.play_sound('custom_explosion')
```

## Testing Sounds

To test if your sounds are working:

1. Run the game: `python main.py`
2. Check console output for "Loading sound effects..." messages
3. Watch for any "Warning: Sound file not found" messages
4. Listen for music when game starts
5. Press ENTER and listen for button sound
6. Play a round and listen for countdown when timer < 5 seconds

## Recommended Sound Libraries

Free sound resources for game development:

- **Freesound.org** - Huge library of CC-licensed sounds
- **OpenGameArt.org** - Game-specific assets
- **Incompetech.com** - Royalty-free music by Kevin MacLeod
- **Zapsplat.com** - Sound effects library
- **LMMS** - Free software to create your own music

## File Format Conversion

To convert audio files:

**Using FFmpeg** (free command-line tool):
```bash
# Convert to OGG
ffmpeg -i input.mp3 -c:a libvorbis -q:a 4 output.ogg

# Convert to WAV
ffmpeg -i input.mp3 output.wav
```

**Using Audacity** (free audio editor):
1. Open your audio file
2. File → Export → Export as OGG/WAV
3. Choose quality settings
4. Save to assets/sounds/ folder

## Implementation Summary

The modular sound system is integrated as follows:

1. **[sound_manager.py](sound_manager.py)** - Core sound management class
2. **[config.py](config.py)** - Sound file path definitions
3. **[main.py](main.py)** - Sound manager initialization and cleanup
4. **[game.py](game.py)** - Sound playback during game events

All sound functionality is cleanly separated and easy to extend or modify!
