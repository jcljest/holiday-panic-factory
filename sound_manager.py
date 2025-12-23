"""
Holiday Panic Factory - Sound Manager
Handles music, sound effects, looping, and volume control.
"""

import pygame
import os
import config


class SoundManager:
    """Manages all audio playback including music and sound effects"""

    def __init__(self):
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.music_volume = 0.7  # Music volume (0.0 to 1.0)
        self.sfx_volume = 0.8    # Sound effects volume (0.0 to 1.0)
        self.muted = False

        # Cache for loaded sounds
        self.sounds = {}

        # Currently playing music track
        self.current_music = None

        # Channel management for looping sounds
        self.sfx_channels = {}  # Map of sound names to channels for looping SFX

        print("Sound Manager initialized")

    def load_sound(self, name, path):
        """
        Load a sound effect and cache it.

        Args:
            name: Identifier for the sound (e.g., 'success', 'fail', 'tick')
            path: File path to sound file

        Returns:
            pygame.mixer.Sound or None if failed
        """
        if name in self.sounds:
            return self.sounds[name]

        if not os.path.exists(path):
            print(f"Warning: Sound file not found: {path}")
            return None

        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
            return sound
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return None

    def play_sound(self, name, loops=0):
        """
        Play a sound effect.

        Args:
            name: Sound identifier (must be loaded first)
            loops: Number of times to loop (-1 for infinite, 0 for once)

        Returns:
            pygame.mixer.Channel or None
        """
        if self.muted:
            return None

        sound = self.sounds.get(name)
        if sound:
            channel = sound.play(loops=loops)
            return channel
        else:
            print(f"Warning: Sound '{name}' not loaded")
            return None

    def play_looping_sound(self, name):
        """
        Play a sound effect on loop and track its channel.

        Args:
            name: Sound identifier

        Returns:
            pygame.mixer.Channel or None
        """
        if self.muted:
            return None

        # Stop any existing loop of this sound
        self.stop_looping_sound(name)

        sound = self.sounds.get(name)
        if sound:
            channel = sound.play(loops=-1)
            self.sfx_channels[name] = channel
            return channel
        else:
            print(f"Warning: Sound '{name}' not loaded")
            return None

    def stop_looping_sound(self, name):
        """
        Stop a looping sound effect.

        Args:
            name: Sound identifier
        """
        if name in self.sfx_channels:
            channel = self.sfx_channels[name]
            if channel:
                channel.stop()
            del self.sfx_channels[name]

    def stop_all_looping_sounds(self):
        """Stop all looping sound effects"""
        for name in list(self.sfx_channels.keys()):
            self.stop_looping_sound(name)

    def load_music(self, path):
        """
        Load a music track.

        Args:
            path: File path to music file

        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(path):
            print(f"Warning: Music file not found: {path}")
            return False

        try:
            pygame.mixer.music.load(path)
            return True
        except pygame.error as e:
            print(f"Error loading music {path}: {e}")
            return False

    def play_music(self, name, path, loops=-1, fade_ms=0):
        """
        Play a music track with optional looping and fade-in.

        Args:
            name: Identifier for the music track
            path: File path to music file
            loops: Number of times to loop (-1 for infinite, 0 for once)
            fade_ms: Fade-in time in milliseconds

        Returns:
            True if successful, False otherwise
        """
        if self.muted:
            return False

        # Only load and play if it's different from current
        if self.current_music != name:
            if self.load_music(path):
                pygame.mixer.music.set_volume(self.music_volume)

                if fade_ms > 0:
                    pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
                else:
                    pygame.mixer.music.play(loops=loops)

                self.current_music = name
                return True
            return False
        return True

    def stop_music(self, fade_ms=0):
        """
        Stop the currently playing music.

        Args:
            fade_ms: Fade-out time in milliseconds
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()

        self.current_music = None

    def pause_music(self):
        """Pause the currently playing music"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Resume paused music"""
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        """
        Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """
        Set sound effects volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def toggle_mute(self):
        """Toggle mute on/off"""
        self.muted = not self.muted

        if self.muted:
            pygame.mixer.music.set_volume(0)
            for sound in self.sounds.values():
                sound.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.music_volume)
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)

        return self.muted

    def preload_sounds(self, sound_map):
        """
        Pre-load all sounds from a sound map dictionary.

        Args:
            sound_map: Dict mapping sound names to file paths
                      e.g., {'success': 'assets/sounds/sfx/success.wav'}
        """
        print("Loading sound effects...")
        for name, path in sound_map.items():
            self.load_sound(name, path)
        print(f"Loaded {len(self.sounds)} sound effects")

    def play_state_music(self, state):
        """
        Play music appropriate for the given game state using paths from config.py.

        Args:
            state: Game state ('menu', 'briefing', 'playing', 'reveal')
        """
        # Check if the state exists in the config.MUSIC_MAP
        # This connects the manager to the settings we just fixed in config.py
        if hasattr(config, 'MUSIC_MAP') and state in config.MUSIC_MAP:
            path = config.MUSIC_MAP[state]
            
            # We create a unique name for the track (e.g. "menu_music")
            name = f"{state}_music" 
            
            # Play it!
            self.play_music(name, path, loops=-1, fade_ms=500)
        else:
            print(f"Warning: No music path found for state '{state}'")

    def cleanup(self):
        """Clean up sound resources"""
        self.stop_all_looping_sounds()
        self.stop_music()
        pygame.mixer.quit()


# Example usage patterns:
"""
# In your game initialization:
sound_manager = SoundManager()

# Pre-load all sounds at startup:
sound_map = {
    'tick': 'assets/sounds/sfx/tick.wav',
    'success': 'assets/sounds/sfx/success.wav',
    'fail': 'assets/sounds/sfx/fail.wav',
    'button_press': 'assets/sounds/sfx/button.wav',
    'countdown': 'assets/sounds/sfx/countdown.wav',
    'siren': 'assets/sounds/sfx/siren.wav',
}
sound_manager.preload_sounds(sound_map)

# Play background music for a game state:
sound_manager.play_state_music('menu')

# Play a one-shot sound effect:
sound_manager.play_sound('button_press')

# Play a looping sound effect (like a siren):
sound_manager.play_looping_sound('siren')

# Stop a looping sound:
sound_manager.stop_looping_sound('siren')

# When timer is low, play countdown loop:
if timer < 5:
    sound_manager.play_looping_sound('countdown')
else:
    sound_manager.stop_looping_sound('countdown')

# Volume controls:
sound_manager.set_music_volume(0.5)
sound_manager.set_sfx_volume(0.8)

# Mute toggle:
sound_manager.toggle_mute()
"""
