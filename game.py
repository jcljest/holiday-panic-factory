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
        
        # Elf Image
            self.elf_image = None
            if self.asset_manager:
                # We try to load it once. If it fails, it prints one warning, not infinite.
                self.elf_image = self.asset_manager.load_sprite('assets/characters/elf_head.png', (200, 200))

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

        # Build result package using ASSET MANAGER to get images
        toy_asset = self.current_order['toy_asset']
        
        # We use .get_sprite() now!
        self.round_results = {
            'toy': self.asset_manager.get_sprite('toys', toy_asset, 'good' if builder_success else 'bad'),
            'wrap': self.asset_manager.get_sprite('wraps', 'paper', 'good' if wrapper_success else 'bad'),
            'bow': self.asset_manager.get_sprite('bows', 'ribbon', 'good' if decorator_success else 'bad'),
            'toy_name': self.current_order['name'],
            'successes': [builder_success, wrapper_success, decorator_success, foreman_success],
        }

        # Calculate score (1 point per successful player)
        round_score = sum(self.round_results['successes'])
        self.score += round_score

        # Play reveal music and sound effects
        if self.sound_manager:
            self.sound_manager.stop_looping_sound('countdown')
            self.sound_manager.play_state_music('reveal')

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

        # 1. Draw the background image (Safe Check)
        bg_drawn = False
        if self.asset_manager:
            bg_image = self.asset_manager.get_background('menu')
            if bg_image:
                screen.blit(bg_image, (0, 0))
                bg_drawn = True
        
        # If no background image, fill with color so text is readable
        if not bg_drawn:
            screen.fill(Colors.BLACK)

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
        
        # Draw Background if available
        bg_name = 'briefing_easy'
        if self.current_tier == OrderTier.STANDARD: bg_name = 'briefing_standard'
        if self.current_tier == OrderTier.NIGHTMARE: bg_name = 'briefing_nightmare'
        
        if self.asset_manager:
            bg = self.asset_manager.get_background(bg_name)
            if bg:
                screen.blit(bg, (0,0))
            else:
                screen.fill(Colors.DARK_GRAY)
        else:
            screen.fill(Colors.DARK_GRAY)

        # Title
        font_large = pygame.font.Font(None, 64)
        title = font_large.render(f"ROUND {self.round_number}", True, Colors.WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Elf Graphic (Uses the pre-loaded variable)
        if self.elf_image:
            elf_rect = self.elf_image.get_rect(center=(SCREEN_WIDTH // 2, 250))
            screen.blit(self.elf_image, elf_rect)
        else:
            # Fallback text if image is missing
            font_medium = pygame.font.Font(None, 48)
            elf = font_medium.render("[ELF HEAD]", True, Colors.BLACK)
            elf_rect = elf.get_rect(center=(SCREEN_WIDTH // 2, 250))
            screen.blit(elf, elf_rect)

        # Dialog
        font_dialog = pygame.font.Font(None, 42)
        # Add a black background rect for text readability
        dialog_surf = font_dialog.render(f'"{self.current_order["dialog"]}"', True, Colors.WHITE)
        dialog_rect = dialog_surf.get_rect(center=(SCREEN_WIDTH // 2, 400))
        pygame.draw.rect(screen, (0,0,0, 180), dialog_rect.inflate(20, 20)) # Semi-transparent bg
        screen.blit(dialog_surf, dialog_rect)

        # Order details
        font_small = pygame.font.Font(None, 32)
        details = [
            f"Item: {self.current_order['name']}",
            f"Time Limit: {self.current_order['time_limit']}s",
            f"Difficulty: {['', 'EASY', 'STANDARD', 'NIGHTMARE'][self.current_tier]}",
        ]

        y_offset = 480
        for detail in details:
            text = font_small.render(detail, True, Colors.WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40

        # Timer
        font_medium = pygame.font.Font(None, 48)
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
        
        # 1. Draw Background
        # We try to load the specific 'reveal' background. 
        # If missing, we default to Dark Gray.
        if self.asset_manager:
            bg = self.asset_manager.get_background('reveal')
            if bg:
                screen.blit(bg, (0, 0))
            else:
                screen.fill(Colors.DARK_GRAY)
        else:
            screen.fill(Colors.DARK_GRAY)

        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)

        # 2. Draw Title
        title = font_large.render("QUALITY CONTROL", True, Colors.GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)

        # 3. Draw The "Conveyor Belt" Items (Toy, Wrap, Bow)
        # We define a helper function inside this method to handle drawing
        # because the logic is the same for all 3 items.
        
        center_x = SCREEN_WIDTH // 2
        start_y = 200    # Where the first item (Toy) starts
        spacing = 120    # How much space between items vertically

        def draw_item(item, y_pos):
            """Helper to draw an image, or text if the image is missing"""
            if isinstance(item, pygame.Surface):
                # It's an image! 
                # OPTIONAL: Scale it down if it's too tall (over 100px) so it fits
                w, h = item.get_size()
                if h > 100:
                    scale = 100 / h
                    item = pygame.transform.scale(item, (int(w * scale), 100))
                
                rect = item.get_rect(center=(center_x, y_pos))
                screen.blit(item, rect)
            else:
                # It's text (fallback string) or None
                text_str = str(item) if item else "MISSING ASSET"
                text = font_medium.render(text_str, True, Colors.WHITE)
                rect = text.get_rect(center=(center_x, y_pos))
                screen.blit(text, rect)

        # Draw the 3 layers separated vertically
        draw_item(self.round_results['toy'], start_y)
        draw_item(self.round_results['wrap'], start_y + spacing)
        draw_item(self.round_results['bow'], start_y + (spacing * 2))


        # 4. Elf Commentary (Based on Score)
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

        # 5. Individual Player Results (Checkmarks/X's)
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

        # 6. Continue Prompt
        continue_text = font_small.render("Press ENTER for next round", True, Colors.LIGHT_GRAY)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(continue_text, continue_rect)
