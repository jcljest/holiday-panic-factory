# Code Examples for Holiday Panic Factory

## How to Add Sounds to Player Actions

### Example 1: Play Sound When Wrapper Presses Space

To add a wrapping sound when Player 2 presses the spacebar, you could modify the `Wrapper` class:

**In [players.py](players.py), Wrapper class:**

```python
class Wrapper(Player):
    def __init__(self, sound_manager=None):
        super().__init__(2, QUADRANT_2)
        self.sound_manager = sound_manager  # Add sound manager
        # ... rest of init ...

    def update(self, dt, keys):
        if not self.has_pressed:
            # Move cursor...
            # ...

            # Check for spacebar press
            if keys[pygame.K_SPACE]:
                self.has_pressed = True
                self.press_position = self.cursor_position

                # Play wrapping sound
                if self.sound_manager:
                    self.sound_manager.play_sound('wrap')
```

Then update [game.py](game.py) to pass sound_manager to players:

```python
def __init__(self, asset_manager=None, sound_manager=None):
    # ...
    self.wrapper = Wrapper(sound_manager)
```

---

### Example 2: Play Error Sound When Decorator Makes Mistake

**In [players.py](players.py), Decorator class:**

```python
def update(self, dt, keys_pressed):
    if self.completed:
        return

    # ... existing code ...

    if correct_key:
        self.current_index += 1
        # Play success tick
        if self.sound_manager:
            self.sound_manager.play_sound('tick')
    elif len(wrong_keys) > 0:
        # Wrong key pressed - reset sequence
        self.current_index = 0

        # Play error sound
        if self.sound_manager:
            self.sound_manager.play_sound('error')
```

---

### Example 3: Add Timer Tick Sound

**In [game.py](game.py), update method during PLAYING state:**

```python
elif self.state == GameState.PLAYING:
    # Track previous second
    previous_second = int(self.state_timer)

    # Update timer
    self.state_timer -= dt

    # Get current second
    current_second = int(self.state_timer)

    # Play tick when second changes (except at 0)
    if previous_second != current_second and current_second > 0:
        if self.sound_manager:
            self.sound_manager.play_sound('tick')

    # Play countdown when time is low...
    # ... rest of code
```

---

### Example 4: Add "Thump" Sounds in Reveal Phase

Make the gift layers drop with sound effects:

**In [game.py](game.py), draw_reveal method:**

```python
def draw_reveal(self, screen):
    # ... existing drawing code ...

    # Track animation state
    if not hasattr(self, 'reveal_animation_time'):
        self.reveal_animation_time = 0

    self.reveal_animation_time += dt

    # Play thump sounds at specific times
    if 0.5 < self.reveal_animation_time < 0.6:  # First thump
        if self.sound_manager:
            self.sound_manager.play_sound('thump')
    elif 1.0 < self.reveal_animation_time < 1.1:  # Second thump
        if self.sound_manager:
            self.sound_manager.play_sound('thump')
    elif 1.5 < self.reveal_animation_time < 1.6:  # Third thump
        if self.sound_manager:
            self.sound_manager.play_sound('thump')
```

---

### Example 5: Mute Toggle with M Key

**In [main.py](main.py), event handling:**

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        keys_pressed.append(event.key)

        # ESC to quit
        if event.key == pygame.K_ESCAPE:
            running = False

        # M to toggle mute
        elif event.key == pygame.K_m:
            is_muted = sound_manager.toggle_mute()
            print(f"Sound {'muted' if is_muted else 'unmuted'}")
```

---

### Example 6: Volume Slider (Advanced)

Here's how you could add volume controls in a settings menu:

```python
class SettingsMenu:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.music_volume = 0.7
        self.sfx_volume = 0.8

    def increase_music_volume(self):
        self.music_volume = min(1.0, self.music_volume + 0.1)
        self.sound_manager.set_music_volume(self.music_volume)

    def decrease_music_volume(self):
        self.music_volume = max(0.0, self.music_volume - 0.1)
        self.sound_manager.set_music_volume(self.music_volume)

    def increase_sfx_volume(self):
        self.sfx_volume = min(1.0, self.sfx_volume + 0.1)
        self.sound_manager.set_sfx_volume(self.sfx_volume)

    def decrease_sfx_volume(self):
        self.sfx_volume = max(0.0, self.sfx_volume - 0.1)
        self.sound_manager.set_sfx_volume(self.sfx_volume)
```

---

## How to Add Background Images

### Example 7: Display Background in Menu

**In [game.py](game.py), draw_menu method:**

```python
def draw_menu(self, screen):
    # Check if background is available
    if self.asset_manager:
        bg = self.asset_manager.get_background('menu')
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(Colors.BLACK)  # Fallback
    else:
        screen.fill(Colors.BLACK)

    # ... rest of menu drawing code
```

---

### Example 8: Dynamic Background Based on Difficulty

**In [game.py](game.py), draw_briefing method:**

```python
def draw_briefing(self, screen):
    # Select background based on tier
    if self.asset_manager:
        if self.current_tier == OrderTier.EASY:
            bg = self.asset_manager.get_background('briefing_easy')
        elif self.current_tier == OrderTier.STANDARD:
            bg = self.asset_manager.get_background('briefing_standard')
        else:
            bg = self.asset_manager.get_background('briefing_nightmare')

        if bg:
            screen.blit(bg, (0, 0))
        else:
            # Fallback to colored background
            if self.current_tier == OrderTier.EASY:
                screen.fill(Colors.TIER_EASY)
            # ... etc
    else:
        # Original colored background code
        # ...
```

---

## How to Display Sprites Instead of Text

### Example 9: Replace Elf Text with Sprite

**In [game.py](game.py), draw_briefing method:**

```python
# Old code:
# elf = font_medium.render("[ELF HEAD PLACEHOLDER]", True, Colors.BLACK)
# elf_rect = elf.get_rect(center=(SCREEN_WIDTH // 2, 250))
# screen.blit(elf, elf_rect)

# New code with sprite:
if self.asset_manager:
    elf_sprite = self.asset_manager.load_sprite(
        CHARACTER_ASSETS['elf_head'],
        size=(200, 200)
    )
    if elf_sprite:
        elf_rect = elf_sprite.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(elf_sprite, elf_rect)
    else:
        # Fallback to text
        elf = font_medium.render("[ELF HEAD]", True, Colors.BLACK)
        elf_rect = elf.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(elf, elf_rect)
```

---

### Example 10: Display Gift Sprites in Reveal

**In [game.py](game.py), draw_reveal method:**

```python
def draw_reveal(self, screen):
    # ... existing code ...

    # Get the asset strings from results
    toy_asset_string = self.round_results['toy']
    wrap_asset_string = self.round_results['wrap']
    bow_asset_string = self.round_results['bow']

    layer_y = 200
    layer_spacing = 100

    # Layer 1: Toy Sprite
    if self.asset_manager and not toy_asset_string.startswith('PLACEHOLDER:'):
        # It's a file path, load the sprite
        toy_sprite = self.asset_manager.load_sprite(toy_asset_string)
        if toy_sprite:
            toy_rect = toy_sprite.get_rect(center=(SCREEN_WIDTH // 2, layer_y))
            screen.blit(toy_sprite, toy_rect)
    else:
        # Fallback to text rendering
        toy_text = font_medium.render(toy_asset_string, True, Colors.WHITE)
        toy_rect = toy_text.get_rect(center=(SCREEN_WIDTH // 2, layer_y))
        screen.blit(toy_text, toy_rect)

    # Repeat for wrap and bow layers...
```

---

## How to Add Custom Orders

### Example 11: Add a New Nightmare Order

**In [config.py](config.py):**

```python
OrderTier.NIGHTMARE: [
    # ... existing nightmare orders ...
    {
        "name": "Live Unicorn",
        "dialog": "SHE WANTS A REAL UNICORN! WHERE ARE WE GOING TO GET THAT?!",
        "p3_arrows": 32,
        "time_limit": 22,
        "p1_decay_rate": 2.0,
        "p2_zone_size": 0.04,
        "toy_asset": "unicorn",  # Add this to ASSET_MAP too
    },
]

# Add the asset mapping
ASSET_MAP = {
    "toys": {
        # ... existing toys ...
        "unicorn": {
            "good": "assets/toys/unicorn_good.png",
            "bad": "assets/toys/unicorn_bad.png"
        },
    },
    # ...
}
```

---

## How to Add Particle Effects

### Example 12: Simple Success Particles

```python
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -2)
        self.color = color
        self.life = 1.0

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.life -= dt

    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * self.life)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

# In Game class:
def __init__(self, ...):
    # ...
    self.particles = []

def spawn_success_particles(self, x, y):
    for _ in range(20):
        self.particles.append(Particle(x, y, Colors.GOLD))

# In update():
self.particles = [p for p in self.particles if p.life > 0]
for particle in self.particles:
    particle.update(dt)

# In draw():
for particle in self.particles:
    particle.draw(screen)
```

---

These examples show how to extend the modular game architecture with your own features!
