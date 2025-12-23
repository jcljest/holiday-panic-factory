"""
Holiday Panic Factory - Configuration and Asset Mapping
This file contains all game constants, asset mappings, and order definitions.
"""

# Screen Configuration
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (220, 20, 20)
    GREEN = (20, 220, 20)
    BLUE = (20, 20, 220)
    YELLOW = (220, 220, 20)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    GOLD = (255, 215, 0)
    ORANGE = (255, 165, 0)

    # Tier colors
    TIER_EASY = (100, 200, 100)
    TIER_STANDARD = (200, 200, 100)
    TIER_NIGHTMARE = (200, 50, 50)

# Quadrant Layout (x, y, width, height)
QUADRANT_1 = (0, 100, 640, 310)  # Top Left - Builder
QUADRANT_2 = (640, 100, 640, 310)  # Top Right - Wrapper
QUADRANT_3 = (0, 410, 640, 310)  # Bottom Left - Decorator
QUADRANT_4 = (640, 410, 640, 310)  # Bottom Right - Foreman

TOP_BAR = (0, 0, 1280, 100)  # Timer and Order Briefing

# Order Tiers
class OrderTier:
    EASY = 1
    STANDARD = 2
    NIGHTMARE = 3

# Order Database
# Format: {tier: [{name, dialog, p3_arrows, time_limit, p1_decay, p2_zone}]}
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
        {
            "name": "Ball",
            "dialog": "Simple ball for little Timmy!",
            "p3_arrows": 5,
            "time_limit": 8,
            "p1_decay_rate": 0.35,
            "p2_zone_size": 0.28,
            "toy_asset": "ball",
        },
        {
            "name": "Box",
            "dialog": "Just a cardboard box. Easy!",
            "p3_arrows": 6,
            "time_limit": 9,
            "p1_decay_rate": 0.4,
            "p2_zone_size": 0.26,
            "toy_asset": "box",
        },
    ],
    OrderTier.STANDARD: [
        {
            "name": "Robot",
            "dialog": "Timmy wants a Robot!",
            "p3_arrows": 10,
            "time_limit": 12,
            "p1_decay_rate": 0.7,
            "p2_zone_size": 0.18,
            "toy_asset": "robot",
        },
        {
            "name": "Doll",
            "dialog": "Princess Sarah needs her doll!",
            "p3_arrows": 12,
            "time_limit": 13,
            "p1_decay_rate": 0.75,
            "p2_zone_size": 0.16,
            "toy_asset": "doll",
        },
        {
            "name": "Bicycle",
            "dialog": "One bicycle coming up!",
            "p3_arrows": 15,
            "time_limit": 14,
            "p1_decay_rate": 0.8,
            "p2_zone_size": 0.15,
            "toy_asset": "bicycle",
        },
    ],
    OrderTier.NIGHTMARE: [
        {
            "name": "Grand Piano",
            "dialog": "HE WANTS A GRAND PIANO!",
            "p3_arrows": 25,
            "time_limit": 18,
            "p1_decay_rate": 1.5,
            "p2_zone_size": 0.05,
            "toy_asset": "piano",
        },
        {
            "name": "T-Rex",
            "dialog": "A LIFE-SIZED T-REX! ARE YOU KIDDING ME?!",
            "p3_arrows": 30,
            "time_limit": 20,
            "p1_decay_rate": 1.8,
            "p2_zone_size": 0.05,
            "toy_asset": "trex",
        },
        {
            "name": "Spaceship",
            "dialog": "SHE WANTS A LIFE-SIZED SPACE ROCKET. MOVE IT!",
            "p3_arrows": 28,
            "time_limit": 19,
            "p1_decay_rate": 1.6,
            "p2_zone_size": 0.06,
            "toy_asset": "spaceship",
        },
    ],
}

# Asset Mapping System
# The final gift is composed of: TOY + WRAP + BOW
ASSET_MAP = {
    # Toy Assets (Player 1 - Builder)
    "toys": {
        # Easy Tier
        "socks": {
            "good": "PLACEHOLDER: Neat Socks",
            "bad": "PLACEHOLDER: Dirty Socks"
        },
        "ball": {
            "good": "PLACEHOLDER: Shiny Ball",
            "bad": "PLACEHOLDER: Deflated Ball"
        },
        "box": {
            "good": "PLACEHOLDER: Nice Box",
            "bad": "PLACEHOLDER: Crushed Box"
        },
        # Standard Tier
        "robot": {
            "good": "PLACEHOLDER: Cool Robot",
            "bad": "PLACEHOLDER: Broken Robot"
        },
        "doll": {
            "good": "PLACEHOLDER: Pretty Doll",
            "bad": "PLACEHOLDER: Creepy Doll"
        },
        "bicycle": {
            "good": "PLACEHOLDER: Shiny Bike",
            "bad": "PLACEHOLDER: Rusty Wheels"
        },
        # Nightmare Tier
        "piano": {
            "good": "PLACEHOLDER: Grand Piano",
            "bad": "PLACEHOLDER: Broken Piano"
        },
        "trex": {
            "good": "PLACEHOLDER: Cool T-Rex",
            "bad": "PLACEHOLDER: Angry Lizard"
        },
        "spaceship": {
            "good": "PLACEHOLDER: Spaceship",
            "bad": "PLACEHOLDER: Scrap Metal"
        },
    },

    # Wrap Assets (Player 2 - Wrapper)
    "wraps": {
        "good": "PLACEHOLDER: Gold Foil",
        "bad": "PLACEHOLDER: Torn Wrapping Paper"
    },

    # Bow Assets (Player 3 - Decorator)
    "bows": {
        "good": "PLACEHOLDER: Satin Ribbon",
        "bad": "PLACEHOLDER: Toilet Paper Ribbon"
    },
}

# Arrow sequences for Player 3
ARROW_DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# Player 4 Foreman Settings
class ForemanSettings:
    NIGHTMARE_DRIFT_MULTIPLIER = 2.5
    STANDARD_DRIFT_MULTIPLIER = 1.5
    EASY_DRIFT_MULTIPLIER = 1.0

# Game States
class GameState:
    MENU = "menu"
    BRIEFING = "briefing"
    PLAYING = "playing"
    REVEAL = "reveal"
    GAME_OVER = "game_over"

# Timing
BRIEFING_DURATION = 4  # seconds
REVEAL_DURATION = 5  # seconds

# Success Thresholds
BUILDER_QUALITY_LINE = 0.5  # Builder must keep bar above 50%
WRAPPER_TOLERANCE = 0.02  # Small tolerance for timing

# Sound Asset Paths
SOUND_MAP = {
    # Sound Effects
    'button_press': 'assets/sounds/sfx/button_press.wav',
    'tick': 'assets/sounds/sfx/tick.wav',
    'success': 'assets/sounds/sfx/success.wav',
    'fail': 'assets/sounds/sfx/fail.wav',
    'countdown': 'assets/sounds/sfx/countdown.wav',
    'siren': 'assets/sounds/sfx/siren.wav',
    'whoosh': 'assets/sounds/sfx/whoosh.wav',
    'thump': 'assets/sounds/sfx/thump.wav',
    'wrap': 'assets/sounds/sfx/wrap.wav',
    'ribbon_tie': 'assets/sounds/sfx/ribbon_tie.wav',
    'error': 'assets/sounds/sfx/error.wav',
    'perfect': 'assets/sounds/sfx/perfect.wav',
}

# Music Asset Paths
MUSIC_MAP = {
    'menu': 'assets/sounds/music/menu.ogg',
    'briefing': 'assets/sounds/music/briefing.ogg',
    'playing': 'assets/sounds/music/gameplay.ogg',
    'reveal': 'assets/sounds/music/reveal.ogg',
}

# Character Asset Paths
CHARACTER_ASSETS = {
    'elf_head': 'assets/characters/elf_head.png',
}

# Background Asset Paths
BACKGROUND_ASSETS = {
    'menu': 'assets/backgrounds/menu_bg.png',
    'briefing_easy': 'assets/backgrounds/briefing_easy_bg.png',
    'briefing_standard': 'assets/backgrounds/briefing_standard_bg.png',
    'briefing_nightmare': 'assets/backgrounds/briefing_nightmare_bg.png',
    'playing': 'assets/backgrounds/playing_bg.png',
    'reveal': 'assets/backgrounds/reveal_bg.png',
}

# Input Configuration
# Note: Actual key mappings are in InputManager class
# These are just display strings for UI
PLAYER_CONTROLS = {
    'P1': {
        'name': 'Builder',
        'controls': 'A/D keys',
        'description': 'Rapid alternating presses',
    },
    'P2': {
        'name': 'Wrapper',
        'controls': 'SPACE',
        'description': 'Press when cursor is in green zone',
    },
    'P3': {
        'name': 'Decorator',
        'controls': 'Arrow Keys',
        'description': 'Enter sequence in exact order',
    },
    'P4': {
        'name': 'Foreman',
        'controls': 'Numpad 4/6',
        'description': 'Balance the needle',
    },
}
