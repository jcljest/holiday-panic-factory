"""
Holiday Panic Factory - Player Role Classes
Each player has unique mechanics scaled by order difficulty.
"""

import pygame
import random
from config import *
from input_manager import InputAction


class Player:
    """Base player class"""
    def __init__(self, player_number, quadrant):
        self.player_number = player_number
        self.quadrant = quadrant
        self.success = False

    def reset(self):
        """Reset player state for new round"""
        self.success = False

    def update(self, dt, keys):
        """Update player state"""
        pass

    def draw(self, screen):
        """Draw player interface"""
        pass


class Builder(Player):
    """Player 1: The Builder (Button Masher)"""
    def __init__(self):
        super().__init__(1, QUADRANT_1)
        self.quality_bar = 0.0
        self.decay_rate = 0.5
        self.fill_rate = 0.15

    def reset(self):
        super().reset()
        self.quality_bar = 0.5

    def set_difficulty(self, decay_rate):
        """Set decay rate based on order difficulty"""
        self.decay_rate = decay_rate

    def update(self, dt, input_manager):
        # Decay the bar
        self.quality_bar -= self.decay_rate * dt

        # Fill on A or D press (using input manager)
        p1_input = input_manager.get_player1_input()
        if p1_input['any']:
            self.quality_bar += self.fill_rate * dt

        # Clamp between 0 and 1
        self.quality_bar = max(0, min(1, self.quality_bar))

    def check_success(self):
        """Check if quality is above threshold"""
        self.success = self.quality_bar >= BUILDER_QUALITY_LINE
        return self.success

    def draw(self, screen):
        x, y, w, h = self.quadrant

        # Background
        pygame.draw.rect(screen, Colors.DARK_GRAY, (x, y, w, h))
        pygame.draw.rect(screen, Colors.WHITE, (x, y, w, h), 3)

        # Title
        font = pygame.font.Font(None, 36)
        title = font.render("P1: BUILDER", True, Colors.WHITE)
        screen.blit(title, (x + 10, y + 10))

        # Instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Press A and D rapidly!", True, Colors.LIGHT_GRAY)
        screen.blit(instruction, (x + 10, y + 50))

        # Quality bar
        bar_x = x + 50
        bar_y = y + 120
        bar_width = w - 100
        bar_height = 100

        # Bar background
        pygame.draw.rect(screen, Colors.BLACK, (bar_x, bar_y, bar_width, bar_height))

        # Quality line
        quality_line_y = bar_y + bar_height * (1 - BUILDER_QUALITY_LINE)
        pygame.draw.line(screen, Colors.RED,
                        (bar_x, quality_line_y),
                        (bar_x + bar_width, quality_line_y), 3)

        # Fill bar
        fill_height = bar_height * self.quality_bar
        fill_y = bar_y + bar_height - fill_height
        bar_color = Colors.GREEN if self.quality_bar >= BUILDER_QUALITY_LINE else Colors.RED
        pygame.draw.rect(screen, bar_color, (bar_x, fill_y, bar_width, fill_height))

        # Border
        pygame.draw.rect(screen, Colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Percentage
        percent = font.render(f"{int(self.quality_bar * 100)}%", True, Colors.WHITE)
        screen.blit(percent, (x + w // 2 - 30, y + 240))


class Wrapper(Player):
    """Player 2: The Wrapper (Timing Precision)"""
    def __init__(self):
        super().__init__(2, QUADRANT_2)
        self.cursor_position = 0.0
        self.cursor_speed = 0.8
        self.cursor_direction = 1
        self.zone_size = 0.3
        self.zone_center = 0.5
        self.has_pressed = False
        self.press_position = None

    def reset(self):
        super().reset()
        self.cursor_position = 0.0
        self.has_pressed = False
        self.press_position = None

    def set_difficulty(self, zone_size):
        """Set green zone size based on order difficulty"""
        self.zone_size = zone_size

    def update(self, dt, input_manager):
        if not self.has_pressed:
            # Move cursor
            self.cursor_position += self.cursor_speed * self.cursor_direction * dt

            # Bounce at edges
            if self.cursor_position >= 1.0:
                self.cursor_position = 1.0
                self.cursor_direction = -1
            elif self.cursor_position <= 0.0:
                self.cursor_position = 0.0
                self.cursor_direction = 1

            # Check for spacebar press (using input manager)
            p2_input = input_manager.get_player2_input()
            if p2_input['pressed']:
                self.has_pressed = True
                self.press_position = self.cursor_position

    def check_success(self):
        """Check if cursor was in green zone"""
        if self.press_position is None:
            self.success = False
        else:
            zone_start = self.zone_center - self.zone_size / 2
            zone_end = self.zone_center + self.zone_size / 2
            self.success = zone_start <= self.press_position <= zone_end
        return self.success

    def draw(self, screen):
        x, y, w, h = self.quadrant

        # Background
        pygame.draw.rect(screen, Colors.DARK_GRAY, (x, y, w, h))
        pygame.draw.rect(screen, Colors.WHITE, (x, y, w, h), 3)

        # Title
        font = pygame.font.Font(None, 36)
        title = font.render("P2: WRAPPER", True, Colors.WHITE)
        screen.blit(title, (x + 10, y + 10))

        # Instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Hit SPACE in the green zone!", True, Colors.LIGHT_GRAY)
        screen.blit(instruction, (x + 10, y + 50))

        # Timing bar
        bar_x = x + 50
        bar_y = y + 120
        bar_width = w - 100
        bar_height = 100

        # Bar background
        pygame.draw.rect(screen, Colors.BLACK, (bar_x, bar_y, bar_width, bar_height))

        # Green zone
        zone_start = self.zone_center - self.zone_size / 2
        zone_end = self.zone_center + self.zone_size / 2
        zone_x = bar_x + bar_width * zone_start
        zone_width = bar_width * self.zone_size
        pygame.draw.rect(screen, Colors.GREEN, (zone_x, bar_y, zone_width, bar_height))

        # Cursor
        if not self.has_pressed:
            cursor_x = bar_x + bar_width * self.cursor_position
            pygame.draw.line(screen, Colors.YELLOW,
                           (cursor_x, bar_y),
                           (cursor_x, bar_y + bar_height), 5)
        else:
            # Show where they pressed
            press_x = bar_x + bar_width * self.press_position
            color = Colors.GREEN if self.success else Colors.RED
            pygame.draw.line(screen, color,
                           (press_x, bar_y),
                           (press_x, bar_y + bar_height), 5)

        # Border
        pygame.draw.rect(screen, Colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 2)


class Decorator(Player):
    """Player 3: The Decorator (Pattern Recognition)"""
    def __init__(self):
        super().__init__(3, QUADRANT_3)
        self.arrow_sequence = []
        self.current_index = 0
        self.completed = False

    def reset(self):
        super().reset()
        self.current_index = 0
        self.completed = False

    def set_difficulty(self, arrow_count):
        """Generate arrow sequence based on order difficulty"""
        self.arrow_sequence = [random.choice(ARROW_DIRECTIONS) for _ in range(arrow_count)]

    def update(self, dt, input_manager):
        """Update using input manager"""
        if self.completed:
            return

        if self.current_index >= len(self.arrow_sequence):
            self.completed = True
            self.success = True
            return

        expected = self.arrow_sequence[self.current_index]

        # Get arrow keys pressed this frame from input manager
        p3_input = input_manager.get_player3_input()
        arrows_pressed = p3_input['keys_pressed']

        # Check if expected arrow was pressed
        if expected in arrows_pressed:
            self.current_index += 1
        elif len(arrows_pressed) > 0:
            # Wrong key pressed - reset sequence
            self.current_index = 0

    def check_success(self):
        """Check if sequence was completed"""
        return self.success

    def draw(self, screen):
        x, y, w, h = self.quadrant

        # Background
        pygame.draw.rect(screen, Colors.DARK_GRAY, (x, y, w, h))
        pygame.draw.rect(screen, Colors.WHITE, (x, y, w, h), 3)

        # Title
        font = pygame.font.Font(None, 36)
        title = font.render("P3: DECORATOR", True, Colors.WHITE)
        screen.blit(title, (x + 10, y + 10))

        # Instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Enter arrow sequence! (Error = Reset)", True, Colors.LIGHT_GRAY)
        screen.blit(instruction, (x + 10, y + 50))

        # Progress
        progress_text = f"Progress: {self.current_index}/{len(self.arrow_sequence)}"
        progress = font_small.render(progress_text, True, Colors.YELLOW)
        screen.blit(progress, (x + 10, y + 80))

        # Draw arrow sequence (with wrapping for long sequences)
        arrow_symbols = {'UP': '↑', 'DOWN': '↓', 'LEFT': '←', 'RIGHT': '→'}
        arrow_size = 40
        arrows_per_row = 12
        start_x = x + 30
        start_y = y + 120

        for i, direction in enumerate(self.arrow_sequence):
            row = i // arrows_per_row
            col = i % arrows_per_row
            arrow_x = start_x + col * arrow_size
            arrow_y = start_y + row * arrow_size

            # Determine color
            if i < self.current_index:
                color = Colors.GREEN  # Completed
            elif i == self.current_index:
                color = Colors.YELLOW  # Current
            else:
                color = Colors.LIGHT_GRAY  # Upcoming

            arrow_text = font.render(arrow_symbols[direction], True, color)
            screen.blit(arrow_text, (arrow_x, arrow_y))


class Foreman(Player):
    """Player 4: The Foreman (System Management)"""
    def __init__(self):
        super().__init__(4, QUADRANT_4)
        self.needle_position = 0.5
        self.drift_speed = 0.3
        self.control_speed = 0.6
        self.drift_multiplier = 1.0

    def reset(self):
        super().reset()
        self.needle_position = 0.5

    def set_difficulty(self, tier):
        """Set drift based on order tier"""
        if tier == OrderTier.NIGHTMARE:
            self.drift_multiplier = ForemanSettings.NIGHTMARE_DRIFT_MULTIPLIER
        elif tier == OrderTier.STANDARD:
            self.drift_multiplier = ForemanSettings.STANDARD_DRIFT_MULTIPLIER
        else:
            self.drift_multiplier = ForemanSettings.EASY_DRIFT_MULTIPLIER

    def update(self, dt, input_manager):
        # Random drift
        drift = random.uniform(-1, 1) * self.drift_speed * self.drift_multiplier * dt
        self.needle_position += drift

        # Player control (using input manager)
        p4_input = input_manager.get_player4_input()
        if p4_input['left']:
            self.needle_position -= self.control_speed * dt
        if p4_input['right']:
            self.needle_position += self.control_speed * dt

        # Clamp
        self.needle_position = max(0, min(1, self.needle_position))

    def check_success(self):
        """Check if needle is reasonably centered"""
        # Consider success if within 30% of center
        self.success = abs(self.needle_position - 0.5) < 0.3
        return self.success

    def draw(self, screen):
        x, y, w, h = self.quadrant

        # Background
        pygame.draw.rect(screen, Colors.DARK_GRAY, (x, y, w, h))
        pygame.draw.rect(screen, Colors.WHITE, (x, y, w, h), 3)

        # Title
        font = pygame.font.Font(None, 36)
        title = font.render("P4: FOREMAN", True, Colors.WHITE)
        screen.blit(title, (x + 10, y + 10))

        # Instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Numpad 4/6 to balance!", True, Colors.LIGHT_GRAY)
        screen.blit(instruction, (x + 10, y + 50))

        # Gauge
        gauge_x = x + 50
        gauge_y = y + 120
        gauge_width = w - 100
        gauge_height = 100

        # Gauge background
        pygame.draw.rect(screen, Colors.BLACK, (gauge_x, gauge_y, gauge_width, gauge_height))

        # Center zone (green)
        center_zone_width = gauge_width * 0.3
        center_x = gauge_x + gauge_width * 0.35
        pygame.draw.rect(screen, Colors.GREEN, (center_x, gauge_y, center_zone_width, gauge_height))

        # Center line
        center_line_x = gauge_x + gauge_width * 0.5
        pygame.draw.line(screen, Colors.WHITE,
                        (center_line_x, gauge_y),
                        (center_line_x, gauge_y + gauge_height), 2)

        # Needle
        needle_x = gauge_x + gauge_width * self.needle_position
        pygame.draw.line(screen, Colors.RED,
                        (needle_x, gauge_y),
                        (needle_x, gauge_y + gauge_height), 5)

        # Border
        pygame.draw.rect(screen, Colors.WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 2)
