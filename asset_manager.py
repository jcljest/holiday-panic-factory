"""
Holiday Panic Factory - Asset Manager
Handles loading, caching, and retrieving sprite assets.
"""

import pygame
import os
from config import ASSET_MAP


class AssetManager:
    """Manages sprite loading and caching"""

    def __init__(self):
        self.sprites = {}  # Cache for loaded sprites
        self.backgrounds = {}  # Cache for background images
        self.fallback_mode = False  # Use text fallback if assets missing

    def load_sprite(self, path, size=None):
        """
        Load a sprite from file path with optional resizing.

        Args:
            path: File path to sprite
            size: Optional (width, height) tuple to resize

        Returns:
            pygame.Surface or None if file not found
        """
        # Check if already cached
        cache_key = f"{path}_{size}" if size else path
        if cache_key in self.sprites:
            return self.sprites[cache_key]

        # Check if file exists
        if not os.path.exists(path):
            print(f"Warning: Asset not found: {path}")
            return None

        try:
            # Load the image
            sprite = pygame.image.load(path).convert_alpha()

            # Resize if requested
            if size:
                sprite = pygame.transform.scale(sprite, size)

            # Cache it
            self.sprites[cache_key] = sprite
            return sprite

        except pygame.error as e:
            print(f"Error loading sprite {path}: {e}")
            return None

    def load_background(self, name, path, size=(1280, 720)):
        """
        Load a background image.

        Args:
            name: Identifier for the background (e.g., 'menu', 'briefing_easy')
            path: File path to background image
            size: Size to scale to (default: screen size)
        """
        if not os.path.exists(path):
            print(f"Warning: Background not found: {path}")
            return None

        try:
            bg = pygame.image.load(path).convert()
            bg = pygame.transform.scale(bg, size)
            self.backgrounds[name] = bg
            return bg
        except pygame.error as e:
            print(f"Error loading background {path}: {e}")
            return None

    def get_sprite(self, asset_type, name, variant='good'):
        """
        Get a sprite from the ASSET_MAP.

        Args:
            asset_type: 'toys', 'wraps', or 'bows'
            name: Asset name (e.g., 'socks', 'robot')
            variant: 'good' or 'bad'

        Returns:
            pygame.Surface, placeholder text string, or None
        """
        try:
            # Get the asset path/string from ASSET_MAP
            if asset_type == 'toys':
                asset_value = ASSET_MAP['toys'][name][variant]
            elif asset_type in ['wraps', 'bows']:
                asset_value = ASSET_MAP[asset_type][variant]
            else:
                return None

            # If it's a placeholder string, return as-is
            if asset_value.startswith('PLACEHOLDER:'):
                return asset_value

            # Otherwise, treat as file path and load sprite
            return self.load_sprite(asset_value)

        except KeyError:
            print(f"Warning: Asset not found in ASSET_MAP: {asset_type}/{name}/{variant}")
            return None

    def get_background(self, name):
        """
        Get a cached background image.

        Args:
            name: Background identifier

        Returns:
            pygame.Surface or None
        """
        return self.backgrounds.get(name)

    def load_all_toys(self, sizes=None):
        """
        Pre-load all toy sprites with optional size specifications.

        Args:
            sizes: Optional dict mapping toy names to (width, height) tuples
                   e.g., {'socks': (150, 150), 'piano': (300, 300)}
        """
        if sizes is None:
            # Default sizes
            sizes = {
                'socks': (150, 150),
                'ball': (150, 150),
                'box': (150, 150),
                'robot': (200, 200),
                'doll': (200, 200),
                'bicycle': (200, 200),
                'piano': (300, 300),
                'trex': (300, 300),
                'spaceship': (300, 300),
            }

        for toy_name in ASSET_MAP['toys'].keys():
            size = sizes.get(toy_name)
            for variant in ['good', 'bad']:
                asset_value = ASSET_MAP['toys'][toy_name][variant]

                # Skip placeholders
                if asset_value.startswith('PLACEHOLDER:'):
                    continue

                # Load and cache
                self.load_sprite(asset_value, size)

        print("All toy sprites loaded and cached")

    def load_all_wraps_and_bows(self):
        """Pre-load all wrapping and bow sprites"""
        wrap_size = (250, 150)
        bow_size = (150, 100)

        for variant in ['good', 'bad']:
            wrap_value = ASSET_MAP['wraps'][variant]
            bow_value = ASSET_MAP['bows'][variant]

            if not wrap_value.startswith('PLACEHOLDER:'):
                self.load_sprite(wrap_value, wrap_size)

            if not bow_value.startswith('PLACEHOLDER:'):
                self.load_sprite(bow_value, bow_size)

        print("Wrap and bow sprites loaded and cached")

    def load_all_backgrounds(self):
        """Pre-load all background images"""
        bg_paths = {
            'menu': 'assets/backgrounds/menu_bg.png',
            'briefing_easy': 'assets/backgrounds/briefing_easy_bg.png',
            'briefing_standard': 'assets/backgrounds/briefing_standard_bg.png',
            'briefing_nightmare': 'assets/backgrounds/briefing_nightmare_bg.png',
            'playing': 'assets/backgrounds/playing_bg.png',
            'reveal': 'assets/backgrounds/reveal_bg.png',
        }

        for name, path in bg_paths.items():
            self.load_background(name, path)

        print("Background images loaded")

    def load_character_sprites(self):
        """Pre-load character sprites"""
        elf_path = 'assets/characters/elf_head.png'

        if os.path.exists(elf_path):
            self.load_sprite(elf_path, (200, 200))
            print("Character sprites loaded")
        else:
            print(f"Warning: Elf character not found at {elf_path}")

    def preload_all_assets(self):
        """Pre-load all game assets at startup"""
        print("Loading all game assets...")
        self.load_all_toys()
        self.load_all_wraps_and_bows()
        self.load_all_backgrounds()
        self.load_character_sprites()
        print("Asset loading complete!")

    def create_fallback_surface(self, text, size, color=(255, 255, 255)):
        """
        Create a fallback surface with text when sprite is missing.

        Args:
            text: Text to display
            size: (width, height) of surface
            color: Text color

        Returns:
            pygame.Surface with text rendered
        """
        surface = pygame.Surface(size, pygame.SRCALPHA)
        font = pygame.font.Font(None, 24)

        # Word wrap the text
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surface = font.render(test_line, True, color)
            if text_surface.get_width() <= size[0] - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Render lines
        y_offset = (size[1] - len(lines) * 30) // 2
        for line in lines:
            text_surf = font.render(line, True, color)
            text_rect = text_surf.get_rect(center=(size[0] // 2, y_offset))
            surface.blit(text_surf, text_rect)
            y_offset += 30

        return surface
