"""
Holiday Panic Factory - Main Game Logic
Manages game states, order progression, and round flow.
"""

import pygame
import random
from config import *
from players import Builder, Wrapper, Decorator, Foreman
from input_manager import InputAction


class Game:
    """Main game controller"""
    def __init__(self, asset_manager=None, sound_manager=None, input_manager=None):
        self.state = GameState.MENU
        self.current_order = None
        self.current_tier = None
        self.round_number = 0
        self.score = 0

        # Managers
        self.asset_manager = asset_manager
        self.sound_manager = sound_manager
        self.input_manager = input_manager

        # Timers
        self.state_timer = 0

        # Players
        self.builder = Builder()
        self.wrapper = Wrapper()
        self.decorator = Decorator()
        self.foreman = Foreman()

        # Results
        self.round_results = {
            'toy': None,
            'wrap': None,
            'bow': None,
        }

        # For tracking key presses (needed for Decorator)
        self.previous_keys = set()

        # Start menu music if sound manager available
        if self.sound_manager:
            self.sound_manager.play_state_music('menu')

    def start_new_round(self):
        """Start a new round with an order"""
        self.round_number += 1

        # Select order tier (you can customize this logic)
        # For now: rounds 1-3 = EASY, 4-7 = STANDARD, 8+ = NIGHTMARE
        if self.round_number <= 3:
            tier = OrderTier.EASY
        elif self.round_number <= 7:
            tier = OrderTier.STANDARD
        else:
            tier = OrderTier.NIGHTMARE

        # Randomly select order from tier
        self.current_tier = tier
        self.current_order = random.choice(ORDERS[tier])

        # Enter briefing state
        self.state = GameState.BRIEFING
        self.state_timer = BRIEFING_DURATION

        # Play briefing music
        if self.sound_manager:
            self.sound_manager.play_state_music('briefing')
            # Play siren for nightmare orders
            if tier == OrderTier.NIGHTMARE:
                self.sound_manager.play_sound('siren')

    def start_action_phase(self):
        """Start the action phase with configured difficulty"""
        self.state = GameState.PLAYING
        self.state_timer = self.current_order['time_limit']

        # Reset all players
        self.builder.reset()
        self.wrapper.reset()
        self.decorator.reset()
        self.foreman.reset()

        # Configure difficulty
        self.builder.set_difficulty(self.current_order['p1_decay_rate'])
        self.wrapper.set_difficulty(self.current_order['p2_zone_size'])
        self.decorator.set_difficulty(self.current_order['p3_arrows'])
        self.foreman.set_difficulty(self.current_tier)

        # Play gameplay music and whoosh sound effect
        if self.sound_manager:
            self.sound_manager.play_state_music('playing')
            self.sound_manager.play_sound('whoosh')

    def end_action_phase(self):
        """End the action phase and evaluate results"""
        self.state = GameState.REVEAL
        self.state_timer = REVEAL_DURATION

        # Check success for each player
        builder_success = self.builder.check_success()
        wrapper_success = self.wrapper.check_success()
        decorator_success = self.decorator.check_success()
        foreman_success = self.foreman.check_success()

        # Build result package
        toy_asset = self.current_order['toy_asset']
        self.round_results = {
            'toy': ASSET_MAP['toys'][toy_asset]['good' if builder_success else 'bad'],
            'wrap': ASSET_MAP['wraps']['good' if wrapper_success else 'bad'],
            'bow': ASSET_MAP['bows']['good' if decorator_success else 'bad'],
            'toy_name': self.current_order['name'],
            'successes': [builder_success, wrapper_success, decorator_success, foreman_success],
        }

        # Calculate score (1 point per successful player)
        round_score = sum(self.round_results['successes'])
        self.score += round_score

        # Play reveal music and sound effects
        if self.sound_manager:
            self.sound_manager.stop_looping_sound('countdown')  # Stop countdown if playing
            self.sound_manager.play_state_music('reveal')

            # Play appropriate sound based on success
            if round_score == 4:
                self.sound_manager.play_sound('perfect')
            elif round_score >= 2:
                self.sound_manager.play_sound('success')
            else:
                self.sound_manager.play_sound('fail')

    def update(self, dt, input_manager):
        """Update game state"""
        if self.state == GameState.MENU:
            # Press ENTER to start
            if input_manager.is_action_pressed(InputAction.MENU_CONFIRM):
                if self.sound_manager:
                    self.sound_manager.play_sound('button_press')
                self.start_new_round()

        elif self.state == GameState.BRIEFING:
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.start_action_phase()

        elif self.state == GameState.PLAYING:
            self.state_timer -= dt

            # Play countdown sound when time is low
            if self.sound_manager:
                if self.state_timer <= 5 and self.state_timer > 0:
                    # Start looping countdown if not already playing
                    if 'countdown' not in self.sound_manager.sfx_channels:
                        self.sound_manager.play_looping_sound('countdown')

            # Update all players with input manager
            self.builder.update(dt, input_manager)
            self.wrapper.update(dt, input_manager)
            self.decorator.update(dt, input_manager)
            self.foreman.update(dt, input_manager)

            # Check if time is up
            if self.state_timer <= 0:
                self.end_action_phase()

        elif self.state == GameState.REVEAL:
            self.state_timer -= dt
            if self.state_timer <= 0:
                # Continue to next round (or game over)
                if input_manager.is_action_pressed(InputAction.MENU_CONFIRM):
                    if self.sound_manager:
                        self.sound_manager.play_sound('button_press')
                    self.start_new_round()

    def draw(self, screen):
        """Draw current game state"""
        screen.fill(Colors.BLACK)

        if self.state == GameState.MENU:
            self.draw_menu(screen)

        elif self.state == GameState.BRIEFING:
            self.draw_briefing(screen)

        elif self.state == GameState.PLAYING:
            self.draw_top_bar(screen)
            self.builder.draw(screen)
            self.wrapper.draw(screen)
            self.decorator.draw(screen)
            self.foreman.draw(screen)

        elif self.state == GameState.REVEAL:
            self.draw_reveal(screen)

    def draw_menu(self, screen):
        """Draw main menu"""
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)

        # Title
        title = font_large.render("HOLIDAY PANIC FACTORY", True, Colors.GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        # Subtitle
        subtitle = font_medium.render("Elf Panic!", True, Colors.WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(subtitle, subtitle_rect)

        # Instructions
        instructions = [
            "4-Player Local Co-op",
            "",
            "P1 (Builder): A/D keys",
            "P2 (Wrapper): SPACE",
            "P3 (Decorator): Arrow Keys",
            "P4 (Foreman): Numpad 4/6",
            "",
            "Press ENTER to Start",
        ]

        y_offset = 350
        for line in instructions:
            text = font_small.render(line, True, Colors.LIGHT_GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 35

    def draw_briefing(self, screen):
        """Draw briefing screen with order details"""
        # Background color based on tier
        if self.current_tier == OrderTier.EASY:
            bg_color = Colors.TIER_EASY
        elif self.current_tier == OrderTier.STANDARD:
            bg_color = Colors.TIER_STANDARD
        else:
            bg_color = Colors.TIER_NIGHTMARE

        screen.fill(bg_color)

        # Title
        font_large = pygame.font.Font(None, 64)
        title = font_large.render(f"ROUND {self.round_number}", True, Colors.WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # Elf placeholder
        font_medium = pygame.font.Font(None, 48)
        elf = font_medium.render("[ELF HEAD PLACEHOLDER]", True, Colors.BLACK)
        elf_rect = elf.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(elf, elf_rect)

        # Dialog
        font_dialog = pygame.font.Font(None, 42)
        dialog = font_dialog.render(f'"{self.current_order["dialog"]}"', True, Colors.WHITE)
        dialog_rect = dialog.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(dialog, dialog_rect)

        # Order details
        font_small = pygame.font.Font(None, 32)
        details = [
            f"Item: {self.current_order['name']}",
            f"Time Limit: {self.current_order['time_limit']}s",
            f"Difficulty: {['', 'EASY', 'STANDARD', 'NIGHTMARE'][self.current_tier]}",
        ]

        y_offset = 450
        for detail in details:
            text = font_small.render(detail, True, Colors.WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40

        # Timer
        timer_text = font_medium.render(f"Starting in {int(self.state_timer) + 1}...", True, Colors.YELLOW)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 600))
        screen.blit(timer_text, timer_rect)

    def draw_top_bar(self, screen):
        """Draw top bar with timer and order info"""
        x, y, w, h = TOP_BAR

        # Background
        pygame.draw.rect(screen, Colors.GRAY, (x, y, w, h))
        pygame.draw.rect(screen, Colors.WHITE, (x, y, w, h), 3)

        # Round number
        font_large = pygame.font.Font(None, 48)
        round_text = font_large.render(f"Round {self.round_number}", True, Colors.WHITE)
        screen.blit(round_text, (x + 20, y + 10))

        # Order name
        order_text = font_large.render(f"Order: {self.current_order['name']}", True, Colors.GOLD)
        screen.blit(order_text, (x + 300, y + 10))

        # Timer
        timer_color = Colors.RED if self.state_timer < 5 else Colors.GREEN
        timer_text = font_large.render(f"Time: {self.state_timer:.1f}s", True, timer_color)
        screen.blit(timer_text, (x + 800, y + 10))

        # Score
        score_text = font_large.render(f"Score: {self.score}", True, Colors.WHITE)
        screen.blit(score_text, (x + 1080, y + 10))

    def draw_reveal(self, screen):
        """Draw the reveal screen showing the final gift"""
        screen.fill(Colors.DARK_GRAY)

        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)

        # Title
        title = font_large.render("QUALITY CONTROL", True, Colors.GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)

        # The conveyor belt effect - show the three layers
        layer_y = 200
        layer_spacing = 100

        # Layer 1: Toy
        toy_text = font_medium.render(self.round_results['toy'], True, Colors.WHITE)
        toy_rect = toy_text.get_rect(center=(SCREEN_WIDTH // 2, layer_y))
        screen.blit(toy_text, toy_rect)

        layer_y += layer_spacing

        # Layer 2: Wrap
        wrap_text = font_medium.render(self.round_results['wrap'], True, Colors.WHITE)
        wrap_rect = wrap_text.get_rect(center=(SCREEN_WIDTH // 2, layer_y))
        screen.blit(wrap_text, wrap_rect)

        layer_y += layer_spacing

        # Layer 3: Bow
        bow_text = font_medium.render(self.round_results['bow'], True, Colors.WHITE)
        bow_rect = bow_text.get_rect(center=(SCREEN_WIDTH // 2, layer_y))
        screen.blit(bow_text, bow_rect)

        # Elf commentary
        successes = sum(self.round_results['successes'])
        if successes == 4:
            comment = "PERFECT! This kid is gonna love it!"
            color = Colors.GREEN
        elif successes == 3:
            comment = "Not bad, but we can do better!"
            color = Colors.YELLOW
        elif successes == 2:
            comment = "Yikes... this might cause some tears."
            color = Colors.ORANGE
        else:
            comment = "You RUINED CHRISTMAS!"
            color = Colors.RED

        comment_text = font_medium.render(comment, True, color)
        comment_rect = comment_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        screen.blit(comment_text, comment_rect)

        # Individual results
        player_results = [
            ("Builder", self.round_results['successes'][0]),
            ("Wrapper", self.round_results['successes'][1]),
            ("Decorator", self.round_results['successes'][2]),
            ("Foreman", self.round_results['successes'][3]),
        ]

        result_y = 620
        for player, success in player_results:
            status = "✓" if success else "✗"
            status_color = Colors.GREEN if success else Colors.RED
            result_text = font_small.render(f"{player}: {status}", True, status_color)
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, result_y))
            screen.blit(result_text, result_rect)
            result_y += 30

        # Continue prompt
        continue_text = font_small.render("Press ENTER for next round", True, Colors.LIGHT_GRAY)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(continue_text, continue_rect)
