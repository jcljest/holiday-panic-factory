# Input Manager Guide

## Overview

The Holiday Panic Factory now includes a **fully modular Input Manager** that handles all player input through a clean, remappable interface. This separates input handling from game logic, making it easy to support custom controls, gamepad input, and accessibility features.

## Key Features

- ✅ **Centralized Input Handling** - All input goes through one manager
- ✅ **Action-Based System** - Map actions instead of raw keys
- ✅ **Easy Remapping** - Change controls without touching game code
- ✅ **Gamepad Support** - Built-in gamepad detection and handling
- ✅ **Frame-Perfect Input** - Distinguishes between "pressed" and "held"
- ✅ **Player-Specific Methods** - Convenience methods for each player
- ✅ **Mute Toggle** - Press M to mute/unmute sound

---

## How It Works

### The Input Flow

```
Keyboard/Gamepad
       ↓
pygame.event.get()
       ↓
input_manager.update(events)
       ↓
input_manager.is_action_pressed(action)
       ↓
Player code responds
```

### Action-Based Input

Instead of checking raw keys like `pygame.K_a`, you check actions like `InputAction.P1_LEFT`.

**Before (old way):**
```python
if keys[pygame.K_a]:
    move_left()
```

**After (new way):**
```python
if input_manager.is_action_pressed(InputAction.P1_LEFT):
    move_left()
```

This means you can remap keys without changing any game code!

---

## Input Actions

All available input actions are defined in [input_manager.py](input_manager.py):

### Player 1 (Builder)
- `InputAction.P1_LEFT` - A key (default)
- `InputAction.P1_RIGHT` - D key (default)

### Player 2 (Wrapper)
- `InputAction.P2_ACTION` - SPACE key (default)

### Player 3 (Decorator)
- `InputAction.P3_UP` - Up Arrow (default)
- `InputAction.P3_DOWN` - Down Arrow (default)
- `InputAction.P3_LEFT` - Left Arrow (default)
- `InputAction.P3_RIGHT` - Right Arrow (default)

### Player 4 (Foreman)
- `InputAction.P4_LEFT` - Numpad 4 (default)
- `InputAction.P4_RIGHT` - Numpad 6 (default)

### Menu/UI
- `InputAction.MENU_CONFIRM` - ENTER or Numpad ENTER (default)
- `InputAction.MENU_BACK` - ESC (default)
- `InputAction.PAUSE` - ESC or P (default)
- `InputAction.MUTE` - M (default)

---

## API Reference

### Core Methods

#### `update(events)`
Updates input state for the current frame. Call this once per frame.

```python
events = pygame.event.get()
input_manager.update(events)
```

#### `is_action_pressed(action)`
Returns True if action was pressed **this frame** (single trigger).

```python
if input_manager.is_action_pressed(InputAction.MENU_CONFIRM):
    start_game()  # Only fires once when pressed
```

#### `is_action_held(action)`
Returns True if action is currently **held down**.

```python
if input_manager.is_action_held(InputAction.P1_LEFT):
    quality_bar += fill_rate  # Continues while held
```

#### `is_key_pressed(key)`
Check if a specific pygame key was pressed this frame.

```python
if input_manager.is_key_pressed(pygame.K_SPACE):
    # Spacebar was just pressed
```

#### `is_key_held(key)`
Check if a specific pygame key is currently held.

```python
if input_manager.is_key_held(pygame.K_a):
    # A key is being held down
```

---

### Player-Specific Methods

These convenience methods return dictionaries with all input for a specific player.

#### `get_player1_input()`
Returns Builder input state.

```python
p1 = input_manager.get_player1_input()
# {
#     'left': bool,   # Is left key held?
#     'right': bool,  # Is right key held?
#     'any': bool     # Is either key held?
# }

if p1['any']:
    quality_bar += fill_rate
```

#### `get_player2_input()`
Returns Wrapper input state.

```python
p2 = input_manager.get_player2_input()
# {
#     'pressed': bool,  # Was action pressed this frame?
#     'held': bool      # Is action currently held?
# }

if p2['pressed']:
    trigger_wrap()
```

#### `get_player3_input()`
Returns Decorator input state.

```python
p3 = input_manager.get_player3_input()
# {
#     'up_pressed': bool,
#     'down_pressed': bool,
#     'left_pressed': bool,
#     'right_pressed': bool,
#     'keys_pressed': list  # e.g., ['UP', 'DOWN']
# }

for arrow in p3['keys_pressed']:
    process_arrow(arrow)
```

#### `get_player4_input()`
Returns Foreman input state.

```python
p4 = input_manager.get_player4_input()
# {
#     'left': bool,   # Is left key held?
#     'right': bool   # Is right key held?
# }

if p4['left']:
    needle_position -= speed
```

---

## Key Remapping

### Remap a Single Action

```python
# Change P1 left to LEFT arrow
input_manager.remap_key(InputAction.P1_LEFT, pygame.K_LEFT)

# Change P2 action to Z key
input_manager.remap_key(InputAction.P2_ACTION, pygame.K_z)
```

### Remap to Multiple Keys

```python
# Allow SPACE or Z for P2
input_manager.remap_key(InputAction.P2_ACTION, [pygame.K_SPACE, pygame.K_z])

# Allow ENTER, SPACE, or START button
input_manager.remap_key(InputAction.MENU_CONFIRM,
    [pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER])
```

### Get Current Mapping

```python
keys = input_manager.get_mapping(InputAction.P1_LEFT)
# Returns: [pygame.K_a]

display = input_manager.get_action_display_name(InputAction.P1_LEFT)
# Returns: "A" or "A/D" if multiple keys
```

### Reset to Defaults

```python
input_manager.reset_to_defaults()
```

---

## Usage Examples

### Example 1: Basic Player Input

```python
# In Player class update method:
def update(self, dt, input_manager):
    p1_input = input_manager.get_player1_input()

    if p1_input['any']:
        self.quality_bar += self.fill_rate * dt
```

### Example 2: Menu Navigation

```python
# In menu update:
if input_manager.is_action_pressed(InputAction.MENU_CONFIRM):
    sound_manager.play_sound('button_press')
    start_game()

if input_manager.is_action_pressed(InputAction.MENU_BACK):
    exit_menu()
```

### Example 3: Mute Toggle

```python
# In main loop:
if input_manager.is_action_pressed(InputAction.MUTE):
    is_muted = sound_manager.toggle_mute()
    print(f"Sound {'muted' if is_muted else 'unmuted'}")
```

### Example 4: Settings Menu with Remapping

```python
class SettingsMenu:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.remapping = None  # Currently remapping action

    def start_remap(self, action):
        """Start listening for new key"""
        self.remapping = action
        print(f"Press new key for {action}...")

    def update(self, input_manager):
        if self.remapping and input_manager.any_key_pressed():
            keys = input_manager.get_keys_pressed_this_frame()
            if keys:
                new_key = keys[0]
                input_manager.remap_key(self.remapping, new_key)
                print(f"Remapped to {input_manager.get_key_name(new_key)}")
                self.remapping = None
```

### Example 5: Arrow Sequence Processing

```python
# In Decorator class:
def update(self, dt, input_manager):
    p3_input = input_manager.get_player3_input()

    for arrow in p3_input['keys_pressed']:
        if arrow == self.expected_arrow:
            self.advance_sequence()
        else:
            self.reset_sequence()
```

---

## Gamepad Support

The Input Manager automatically detects connected gamepads at startup.

### Check Gamepad Status

```python
if input_manager.gamepad_enabled:
    print(f"{len(input_manager.gamepads)} gamepads connected")
```

### Get Gamepad Input

```python
gamepad_data = input_manager.get_gamepad_input(player_index=0)
if gamepad_data:
    axes = gamepad_data['axes']      # List of axis values (-1 to 1)
    buttons = gamepad_data['buttons']  # List of button states (bool)
    hat = gamepad_data['hat']         # D-pad state (tuple)
```

### Implementing Gamepad Controls (Advanced)

You can extend the input manager to map gamepad buttons to actions:

```python
# Example: Map gamepad button 0 to P1_LEFT
if input_manager.gamepad_enabled:
    gamepad = input_manager.gamepads[0]
    if gamepad.get_button(0):  # Button A
        # Trigger P1_LEFT action
        pass
```

---

## Debug Utilities

### Print All Mappings

```python
input_manager.print_current_mappings()
```

Output:
```
Current Input Mappings:
==================================================
menu_back            -> escape
menu_confirm         -> return, [enter]
mute                 -> m
p1_left              -> a
p1_right             -> d
...
==================================================
```

### Print Pressed Keys (Debug)

```python
input_manager.print_pressed_keys()
# Output: Keys pressed: a, d
```

### Print Held Keys

```python
input_manager.print_held_keys()
# Output: Keys held: space, left
```

---

## Integration in Game Code

### main.py
```python
from input_manager import InputManager, InputAction

input_manager = InputManager()

while running:
    events = pygame.event.get()
    input_manager.update(events)

    # ESC to quit
    if input_manager.is_action_pressed(InputAction.MENU_BACK):
        running = False

    # M to mute
    if input_manager.is_action_pressed(InputAction.MUTE):
        sound_manager.toggle_mute()

    game.update(dt, input_manager)
```

### game.py
```python
from input_manager import InputAction

def update(self, dt, input_manager):
    if self.state == GameState.MENU:
        if input_manager.is_action_pressed(InputAction.MENU_CONFIRM):
            self.start_game()

    elif self.state == GameState.PLAYING:
        # Players update with input_manager
        self.builder.update(dt, input_manager)
        self.wrapper.update(dt, input_manager)
        # ...
```

### players.py
```python
def update(self, dt, input_manager):
    p1_input = input_manager.get_player1_input()
    if p1_input['any']:
        self.quality_bar += self.fill_rate * dt
```

---

## Benefits

### 1. Clean Abstraction
- Game logic doesn't care about specific keys
- Actions are named semantically (`P1_LEFT` vs `pygame.K_a`)
- Easy to understand what each input does

### 2. Easy Remapping
- Change controls in one place
- Support accessibility (one-handed mode, etc.)
- Let players customize their controls

### 3. Multi-Input Support
- Same action can be triggered by multiple keys
- Support both ENTER and Numpad ENTER for confirm
- Allow arrow keys OR WASD

### 4. Frame-Perfect Input
- Distinguish between "just pressed" and "held"
- Prevents double-triggering on menu selections
- Accurate timing for Player 2 wrapper

### 5. Future-Proof
- Easy to add gamepad support
- Easy to add mouse/touch support
- Easy to add input recording/playback

---

## Advanced Features

### Custom Input Profiles

```python
# Save current mappings
profile = {
    action: input_manager.get_mapping(action)
    for action in [InputAction.P1_LEFT, InputAction.P1_RIGHT, ...]
}

# Load a profile
for action, keys in profile.items():
    input_manager.remap_key(action, keys)
```

### Input Buffering (Future Enhancement)

```python
# Could add input buffer for combo detection
class InputManager:
    def __init__(self):
        self.input_buffer = []  # Last N frames of input
        self.buffer_size = 10

    def detect_combo(self, sequence):
        # Check if sequence appears in buffer
        pass
```

### Accessibility Options

```python
# One-handed mode - remap P1 to arrow keys
def enable_one_handed_mode():
    input_manager.remap_key(InputAction.P1_LEFT, pygame.K_LEFT)
    input_manager.remap_key(InputAction.P1_RIGHT, pygame.K_RIGHT)

# Simplified controls - remap to single keys
def enable_simplified_controls():
    input_manager.remap_key(InputAction.P3_UP, pygame.K_w)
    input_manager.remap_key(InputAction.P3_DOWN, pygame.K_s)
    input_manager.remap_key(InputAction.P3_LEFT, pygame.K_a)
    input_manager.remap_key(InputAction.P3_RIGHT, pygame.K_d)
```

---

## Summary

The Input Manager provides:
- ✅ Centralized input handling
- ✅ Action-based abstraction
- ✅ Easy key remapping
- ✅ Gamepad support
- ✅ Frame-perfect input detection
- ✅ Player-specific convenience methods
- ✅ Debug utilities
- ✅ Future-proof architecture

All input now flows through a single, clean interface that separates "what the player wants to do" from "which button they pressed"!
