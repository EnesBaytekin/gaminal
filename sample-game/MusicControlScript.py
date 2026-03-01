from pygaminal import *


class MusicControlScript:
    """Test script for music control."""

    def __init__(self):
        pass

    def update(self, obj):
        input_manager = InputManager()
        audio = AudioManager()

        # M: Toggle music play/stop
        if input_manager.is_just_pressed(pygame.K_m):
            if audio.is_music_playing():
                audio.stop_music(fade_out=1.0)
                print("Music stopped")
            else:
                audio.play_music("sounds/music.ogg", loop=True, fade_in=1.0, volume=0.6)
                print("Music started")

        # UP/DOWN: Volume control
        if input_manager.is_pressed(pygame.K_UP):
            vol = audio.get_music_volume()
            new_vol = min(1.0, vol + 0.02)
            audio.set_music_volume(new_vol)
            print(f"Volume: {new_vol:.2f}")

        if input_manager.is_pressed(pygame.K_DOWN):
            vol = audio.get_music_volume()
            new_vol = max(0.0, vol - 0.02)
            audio.set_music_volume(new_vol)
            print(f"Volume: {new_vol:.2f}")

        # P: Pause/Resume
        if input_manager.is_just_pressed(pygame.K_p):
            if audio.is_music_playing():
                audio.pause_music()
                print("Music paused")
            else:
                audio.resume_music()
                print("Music resumed")

        # Current status every second (approximately)
        import time
        if not hasattr(self, 'last_status_time'):
            self.last_status_time = 0

        current_time = time.time()
        if current_time - self.last_status_time > 2.0:
            self.last_status_time = current_time
            playing = audio.is_music_playing()
            vol = audio.get_music_volume()
            current_music = audio.get_current_music()
            print(f"Status: Playing={playing}, Volume={vol:.2f}, Music={current_music}")

    def draw(self, obj):
        """MusicControlScript doesn't need drawing."""
        pass
