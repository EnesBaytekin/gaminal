import pygame
import threading
import time


class AudioManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def init(self):
        """Initialize audio system (called by App)."""
        if not hasattr(self, 'initialized'):
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.initialized = True
            self.music_volume = 1.0
            self.sfx_volume = 1.0
            self.current_music = None
            self.music_loop = False
            self.music_fade_timer = None

    # Music methods (Background Music)
    def play_music(self, file_path, loop=True, fade_in=0.0, volume=None):
        """
        Play background music.

        Args:
            file_path: Path to music file (mp3, ogg, etc.)
            loop: Should the music loop? (default: True)
            fade_in: Fade in duration in seconds (default: 0.0)
            volume: Volume override (0.0 to 1.0, None = use current music_volume)
        """
        try:
            # Stop current music if playing
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # Load and play music
            pygame.mixer.music.load(file_path)
            self.current_music = file_path
            self.music_loop = loop

            if volume is not None:
                self.set_music_volume(volume)

            if fade_in > 0:
                pygame.mixer.music.play(loops=-1 if loop else 0, fade_ms=int(fade_in * 1000))
            else:
                pygame.mixer.music.play(loops=-1 if loop else 0)

        except Exception as e:
            print(f"Error playing music '{file_path}': {e}")

    def stop_music(self, fade_out=0.0):
        """
        Stop background music.

        Args:
            fade_out: Fade out duration in seconds (default: 0.0)
        """
        if fade_out > 0:
            pygame.mixer.music.fadeout(int(fade_out * 1000))
        else:
            pygame.mixer.music.stop()
        self.current_music = None

    def pause_music(self):
        """Pause background music."""
        pygame.mixer.music.pause()

    def resume_music(self):
        """Resume paused background music."""
        pygame.mixer.music.unpause()

    def is_music_playing(self):
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()

    def set_music_volume(self, volume):
        """
        Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def get_music_volume(self):
        """Get current music volume."""
        return self.music_volume

    # SFX volume control
    def set_sfx_volume(self, volume):
        """
        Set global sound effect volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

    def get_sfx_volume(self):
        """Get current SFX volume."""
        return self.sfx_volume

    def get_current_music(self):
        """Get the currently playing music file path."""
        return self.current_music
