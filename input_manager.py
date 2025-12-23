"""
Holiday Panic Factory - Input Manager
Handles keyboard, gamepad, and remapping functionality.
Provides a clean abstraction for player inputs.
"""

import pygame


class InputAction:
    """Enumeration of all possible input actions"""
    # Player 1 (Builder)
    P1_LEFT = "p1_left"
    P1_RIGHT = "p1_right"

    # Player 2 (Wrapper)
    P2_ACTION = "p2_action"

    # Player 3 (Decorator)
    P3_UP = "p3_up"
    P3_DOWN = "p3_down"
    P3_LEFT = "p3_left"
    P3_RIGHT = "p3_right"

    # Player 4 (Foreman)
    P4_LEFT = "p4_left"
    P4_RIGHT = "p4_right"

    # Menu/UI
    MENU_CONFIRM = "menu_confirm"
    MENU_BACK = "menu_back"
    PAUSE = "pause"
    MUTE = "mute"


class InputManager:
    """Manages all input from keyboard and gamepad with remapping support"""

    def __init__(self):
        # Default keyboard mappings
        self.key_mappings = {
            # Player 1 (Builder)
            InputAction.P1_LEFT: [pygame.K_a],
            InputAction.P1_RIGHT: [pygame.K_d],

            # Player 2 (Wrapper)
            InputAction.P2_ACTION: [pygame.K_SPACE],

            # Player 3 (Decorator)
            InputAction.P3_UP: [pygame.K_UP],
            InputAction.P3_DOWN: [pygame.K_DOWN],
            InputAction.P3_LEFT: [pygame.K_LEFT],
            InputAction.P3_RIGHT: [pygame.K_RIGHT],

            # Player 4 (Foreman)
            InputAction.P4_LEFT: [pygame.K_KP4, pygame.K_LEFTBRACKET],
            InputAction.P4_RIGHT: [pygame.K_KP6, pygame.K_RIGHTBRACKET],

            # Menu/UI
            InputAction.MENU_CONFIRM: [pygame.K_RETURN, pygame.K_KP_ENTER],
            InputAction.MENU_BACK: [pygame.K_ESCAPE],
            InputAction.PAUSE: [pygame.K_ESCAPE, pygame.K_p],
            InputAction.MUTE: [pygame.K_m],
        }

        # Gamepad support (optional)
        self.gamepad_enabled = False
        self.gamepads = []
        self.init_gamepads()

        # State tracking
        self.keys_pressed_this_frame = []
        self.keys_held = set()
        self.actions_pressed_this_frame = set()
        self.actions_held = set()

        # Combo tracking (for advanced inputs)
        self.last_key_time = {}

    def init_gamepads(self):
        """Initialize connected gamepads"""
        try:
            pygame.joystick.init()
            joystick_count = pygame.joystick.get_count()

            for i in range(joystick_count):
                try:
                    gamepad = pygame.joystick.Joystick(i)
                    gamepad.init()
                    self.gamepads.append(gamepad)
                    print(f"Gamepad {i} connected: {gamepad.get_name()}")
                except pygame.error as e:
                    print(f"Failed to initialize gamepad {i}: {e}")

            if len(self.gamepads) > 0:
                self.gamepad_enabled = True
                print(f"Gamepad support enabled ({len(self.gamepads)} controllers)")
        except Exception as e:
            print(f"Gamepad initialization failed: {e}")

    def update(self, events):
        """
        Update input state based on pygame events.
        Call this once per frame with the event list from pygame.event.get()

        Args:
            events: List of pygame events from pygame.event.get()
        """
        # Clear frame-specific data
        self.keys_pressed_this_frame = []
        self.actions_pressed_this_frame = set()

        # Process events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed_this_frame.append(event.key)
                self.keys_held.add(event.key)

                # Update action pressed
                for action, keys in self.key_mappings.items():
                    if event.key in keys:
                        self.actions_pressed_this_frame.add(action)
                        self.actions_held.add(action)

            elif event.type == pygame.KEYUP:
                self.keys_held.discard(event.key)

                # Update action held
                for action, keys in self.key_mappings.items():
                    if event.key in keys:
                        # Only remove from held if no other mapped keys are held
                        if not any(k in self.keys_held for k in keys):
                            self.actions_held.discard(action)

    def is_action_pressed(self, action):
        """
        Check if an action was pressed this frame (single trigger).

        Args:
            action: InputAction constant

        Returns:
            True if action was pressed this frame
        """
        return action in self.actions_pressed_this_frame

    def is_action_held(self, action):
        """
        Check if an action is currently held down.

        Args:
            action: InputAction constant

        Returns:
            True if action is currently held
        """
        return action in self.actions_held

    def is_key_pressed(self, key):
        """
        Check if a specific key was pressed this frame.

        Args:
            key: pygame key constant (e.g., pygame.K_a)

        Returns:
            True if key was pressed this frame
        """
        return key in self.keys_pressed_this_frame

    def is_key_held(self, key):
        """
        Check if a specific key is currently held.

        Args:
            key: pygame key constant

        Returns:
            True if key is currently held
        """
        return key in self.keys_held

    def get_keys_pressed_this_frame(self):
        """
        Get list of all keys pressed this frame.
        Useful for Player 3 (Decorator) arrow sequence.

        Returns:
            List of pygame key constants
        """
        return self.keys_pressed_this_frame.copy()

    def get_actions_pressed_this_frame(self):
        """
        Get set of all actions triggered this frame.

        Returns:
            Set of InputAction constants
        """
        return self.actions_pressed_this_frame.copy()

    def remap_key(self, action, new_keys):
        """
        Remap an action to different keys.

        Args:
            action: InputAction constant to remap
            new_keys: List of pygame key constants (or single key)

        Example:
            input_manager.remap_key(InputAction.P1_LEFT, pygame.K_LEFT)
            input_manager.remap_key(InputAction.P2_ACTION, [pygame.K_z, pygame.K_x])
        """
        if not isinstance(new_keys, list):
            new_keys = [new_keys]
        self.key_mappings[action] = new_keys
        print(f"Remapped {action} to {[pygame.key.name(k) for k in new_keys]}")

    def get_mapping(self, action):
        """
        Get current key mapping for an action.

        Args:
            action: InputAction constant

        Returns:
            List of pygame key constants
        """
        return self.key_mappings.get(action, [])

    def reset_to_defaults(self):
        """Reset all key mappings to defaults"""
        self.__init__()
        print("Input mappings reset to defaults")

    # Convenience methods for specific players

    def get_player1_input(self):
        """
        Get Player 1 (Builder) input state.

        Returns:
            dict with 'left' and 'right' booleans
        """
        return {
            # 'held' is good for holding down buttons
            'left': self.is_action_held(InputAction.P1_LEFT),
            'right': self.is_action_held(InputAction.P1_RIGHT),
            
            # 'pressed' is good for rapid tapping/mashing
            'left_pressed': self.is_action_pressed(InputAction.P1_LEFT),
            'right_pressed': self.is_action_pressed(InputAction.P1_RIGHT),
            
            'any': self.is_action_held(InputAction.P1_LEFT) or 
                   self.is_action_held(InputAction.P1_RIGHT)
        }

    def get_player2_input(self):
        """
        Get Player 2 (Wrapper) input state.

        Returns:
            dict with 'pressed' and 'held' booleans
        """
        return {
            'pressed': self.is_action_pressed(InputAction.P2_ACTION),
            'held': self.is_action_held(InputAction.P2_ACTION),
        }

    def get_player3_input(self):
        """
        Get Player 3 (Decorator) input state.

        Returns:
            dict with pressed arrows and list of keys pressed this frame
        """
        return {
            'up_pressed': self.is_action_pressed(InputAction.P3_UP),
            'down_pressed': self.is_action_pressed(InputAction.P3_DOWN),
            'left_pressed': self.is_action_pressed(InputAction.P3_LEFT),
            'right_pressed': self.is_action_pressed(InputAction.P3_RIGHT),
            'keys_pressed': self.get_arrow_keys_pressed(),
        }

    def get_player4_input(self):
        """
        Get Player 4 (Foreman) input state.

        Returns:
            dict with 'left' and 'right' booleans
        """
        return {
            'left': self.is_action_held(InputAction.P4_LEFT),
            'right': self.is_action_held(InputAction.P4_RIGHT),
        }

    def get_arrow_keys_pressed(self):
        """
        Get list of arrow directions pressed this frame.
        Specifically for Player 3 (Decorator).

        Returns:
            List of strings: ['UP', 'DOWN', 'LEFT', 'RIGHT']
        """
        arrows = []
        if self.is_action_pressed(InputAction.P3_UP):
            arrows.append('UP')
        if self.is_action_pressed(InputAction.P3_DOWN):
            arrows.append('DOWN')
        if self.is_action_pressed(InputAction.P3_LEFT):
            arrows.append('LEFT')
        if self.is_action_pressed(InputAction.P3_RIGHT):
            arrows.append('RIGHT')
        return arrows

    def any_key_pressed(self):
        """Check if any key was pressed this frame"""
        return len(self.keys_pressed_this_frame) > 0

    def get_key_name(self, key):
        """
        Get human-readable name for a key.

        Args:
            key: pygame key constant

        Returns:
            String name (e.g., "a", "space", "up")
        """
        return pygame.key.name(key)

    def get_action_display_name(self, action):
        """
        Get display name for an action showing current mapping.

        Args:
            action: InputAction constant

        Returns:
            String like "SPACE" or "A/D"
        """
        keys = self.get_mapping(action)
        if not keys:
            return "UNBOUND"

        key_names = [self.get_key_name(k).upper() for k in keys]
        return "/".join(key_names)

    # Gamepad support methods (advanced - optional to implement)

    def get_gamepad_input(self, player_index):
        """
        Get gamepad input for a specific player.

        Args:
            player_index: Player number (0-3)

        Returns:
            dict with gamepad state or None if not connected
        """
        if not self.gamepad_enabled or player_index >= len(self.gamepads):
            return None

        try:
            gamepad = self.gamepads[player_index]
            return {
                'axes': [gamepad.get_axis(i) for i in range(gamepad.get_numaxes())],
                'buttons': [gamepad.get_button(i) for i in range(gamepad.get_numbuttons())],
                'hat': gamepad.get_hat(0) if gamepad.get_numhats() > 0 else (0, 0),
            }
        except Exception as e:
            print(f"Error reading gamepad {player_index}: {e}")
            return None

    # Debug and utility methods

    def print_pressed_keys(self):
        """Print all keys pressed this frame (debug helper)"""
        if self.keys_pressed_this_frame:
            key_names = [self.get_key_name(k) for k in self.keys_pressed_this_frame]
            print(f"Keys pressed: {', '.join(key_names)}")

    def print_held_keys(self):
        """Print all currently held keys (debug helper)"""
        if self.keys_held:
            key_names = [self.get_key_name(k) for k in self.keys_held]
            print(f"Keys held: {', '.join(key_names)}")

    def print_current_mappings(self):
        """Print all current input mappings (debug helper)"""
        print("\nCurrent Input Mappings:")
        print("=" * 50)
        for action, keys in sorted(self.key_mappings.items()):
            key_names = [self.get_key_name(k) for k in keys]
            print(f"{action:20} -> {', '.join(key_names)}")
        print("=" * 50)


# Example usage:
"""
# In main.py:
input_manager = InputManager()

# In game loop:
events = pygame.event.get()
input_manager.update(events)

# In Player 1 update:
p1_input = input_manager.get_player1_input()
if p1_input['any']:
    self.quality_bar += self.fill_rate * dt

# In Player 2 update:
p2_input = input_manager.get_player2_input()
if p2_input['pressed']:
    self.has_pressed = True

# In Player 3 update:
p3_input = input_manager.get_player3_input()
for arrow in p3_input['keys_pressed']:
    # Process arrow input
    pass

# Menu handling:
if input_manager.is_action_pressed(InputAction.MENU_CONFIRM):
    start_game()

if input_manager.is_action_pressed(InputAction.MUTE):
    sound_manager.toggle_mute()

# Remapping (in settings menu):
input_manager.remap_key(InputAction.P1_LEFT, pygame.K_LEFT)
"""
