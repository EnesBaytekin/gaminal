import pygame
import random
from pygaminal.audio_manager import AudioManager


class SoundEffect:
    """Sound effect component for playing short audio clips."""

    def __init__(self, sound_path, volume=1.0, auto_play=False, loop=False, pitch_variation=0.0):
        """
        Initialize sound effect.

        Args:
            sound_path: Path to sound file (wav, ogg, etc.)
            volume: Volume level (0.0 to 1.0)
            auto_play: Play sound automatically when object is created
            loop: Loop the sound continuously
            pitch_variation: Random pitch variation amount (0.0 = none, higher = more variation)
        """
        self.sound_path = sound_path
        self.base_volume = volume
        self.loop = loop
        self.pitch_variation = pitch_variation
        self.audio_manager = AudioManager()

        try:
            self.sound = pygame.mixer.Sound(sound_path)
            self.channel = None

            if auto_play:
                self.play()

        except Exception as e:
            print(f"Error loading sound '{sound_path}': {e}")
            self.sound = None

    def play(self, volume=None):
        """
        Play the sound effect.

        Args:
            volume: Override volume (0.0 to 1.0, None = use base_volume)
        """
        if self.sound is None:
            return

        try:
            # Calculate volume with SFX master volume
            vol = volume if volume is not None else self.base_volume
            final_volume = vol * self.audio_manager.get_sfx_volume()

            # Play sound
            if self.loop:
                self.channel = self.sound.play(loops=-1)
            else:
                self.channel = self.sound.play()

            # Set volume
            if self.channel:
                self.channel.set_volume(final_volume)

        except Exception as e:
            print(f"Error playing sound '{self.sound_path}': {e}")

    def stop(self):
        """Stop the sound effect."""
        if self.channel:
            self.channel.stop()
            self.channel = None

    def pause(self):
        """Pause the sound effect."""
        if self.channel:
            self.channel.pause()

    def resume(self):
        """Resume the paused sound effect."""
        if self.channel:
            self.channel.unpause()

    def is_playing(self):
        """Check if sound is currently playing."""
        return self.channel is not None and self.channel.get_busy()

    def set_volume(self, volume):
        """
        Set sound volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.base_volume = max(0.0, min(1.0, volume))
        if self.channel:
            final_volume = self.base_volume * self.audio_manager.get_sfx_volume()
            self.channel.set_volume(final_volume)

    def get_volume(self):
        """Get current base volume."""
        return self.base_volume

    def update(self, obj):
        """SoundEffect doesn't need updates (unless implementing 3D positional audio)."""
        pass

    def draw(self, obj):
        """SoundEffect doesn't need drawing."""
        pass
