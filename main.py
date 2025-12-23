"""
Holiday Panic Factory - Main Entry Point
Run this file to start the game.
"""

import pygame
from config import *
from game import Game
from asset_manager import AssetManager
from sound_manager import SoundManager
from input_manager import InputManager, InputAction


def main():
    """Main game loop"""
    # Initialize pygame
    pygame.init()

    # Create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Holiday Panic Factory - Elf Panic!")

    # Clock for FPS
    clock = pygame.time.Clock()

    # Initialize managers
    print("Initializing Asset Manager...")
    asset_manager = AssetManager()

    print("Initializing Sound Manager...")
    sound_manager = SoundManager()

    print("Initializing Input Manager...")
    input_manager = InputManager()

    # Pre-load assets (optional - will gracefully handle missing files)
    try:
        asset_manager.preload_all_assets()
    except Exception as e:
        print(f"Warning: Some assets failed to load: {e}")

    # Pre-load sounds
    try:
        sound_manager.preload_sounds(SOUND_MAP)
    except Exception as e:
        print(f"Warning: Some sounds failed to load: {e}")

    # Create game instance with managers
    game = Game(asset_manager, sound_manager, input_manager)

    # Main loop
    running = True
    while running:
        # Calculate delta time
        dt = clock.tick(FPS) / 1000.0  # Convert to seconds

        # Event handling
        events = pygame.event.get()

        # Check for quit event
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update input manager
        input_manager.update(events)

        # Check for ESC to quit (using input manager)
        if input_manager.is_action_pressed(InputAction.MENU_BACK):
            running = False

        # Check for mute toggle
        if input_manager.is_action_pressed(InputAction.MUTE):
            is_muted = sound_manager.toggle_mute()
            print(f"Sound {'muted' if is_muted else 'unmuted'}")

        # Update game (now uses input_manager internally)
        game.update(dt, input_manager)

        # Draw game
        game.draw(screen)

        # Update display
        pygame.display.flip()

    # Cleanup
    print("Cleaning up...")
    sound_manager.cleanup()
    pygame.quit()


if __name__ == "__main__":
    main()
