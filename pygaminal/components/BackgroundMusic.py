from pygaminal.audio_manager import AudioManager


class BackgroundMusic:
    """Component for playing background music."""

    def __init__(self, music_file, loop=True, fade_in=0.0, volume=None):
        """
        Initialize background music.

        Args:
            music_file: Path to music file (mp3, ogg, etc.)
            loop: Should the music loop? (default: True)
            fade_in: Fade in duration in seconds (default: 0.0)
            volume: Volume level (0.0 to 1.0, None = use current music_volume)
        """
        self.music_file = music_file
        self.loop = loop
        self.fade_in = fade_in
        self.volume = volume
        self.audio_manager = AudioManager()

        # Auto-play when component is created
        if self.music_file:
            self.audio_manager.play_music(
                self.music_file,
                loop=self.loop,
                fade_in=self.fade_in,
                volume=self.volume
            )

    def play(self):
        """Play the music."""
        if self.music_file:
            self.audio_manager.play_music(
                self.music_file,
                loop=self.loop,
                fade_in=self.fade_in,
                volume=self.volume
            )

    def stop(self, fade_out=0.0):
        """
        Stop the music.

        Args:
            fade_out: Fade out duration in seconds (default: 0.0)
        """
        self.audio_manager.stop_music(fade_out=fade_out)

    def pause(self):
        """Pause the music."""
        self.audio_manager.pause_music()

    def resume(self):
        """Resume the music."""
        self.audio_manager.resume_music()

    def set_volume(self, volume):
        """
        Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = volume
        self.audio_manager.set_music_volume(volume)

    def update(self, obj):
        """
        Update background music.
        If object dies, optionally stop music.
        """
        # If object is dead, we could stop music here
        # But usually music continues even if object dies
        pass

    def draw(self, obj):
        """BackgroundMusic doesn't need drawing."""
        pass
