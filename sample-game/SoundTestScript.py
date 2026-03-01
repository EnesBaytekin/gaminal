from pygaminal import *


class SoundTestScript:
    """Test sound effects on key press."""

    def __init__(self, sound_path=None):
        self.sound_path = sound_path

    def update(self, obj):
        input_manager = InputManager()

        # Play sound effect on spacebar press
        if input_manager.is_just_pressed(pygame.K_SPACE) and self.sound_path:
            sound = SoundEffect(self.sound_path, auto_play=True)
            print(f"Played sound: {self.sound_path}")

        # Music controls
        audio = AudioManager()

        # M: Play music
        if input_manager.is_just_pressed(pygame.K_m):
            audio.play_music("music/bgm.mp3", loop=True, fade_in=1.0)
            print("Playing music")

        # S: Stop music
        if input_manager.is_just_pressed(pygame.K_s):
            audio.stop_music(fade_out=1.0)
            print("Stopped music")

        # P: Pause/Resume music
        if input_manager.is_just_pressed(pygame.K_p):
            if audio.is_music_playing():
                audio.pause_music()
                print("Paused music")
            else:
                audio.resume_music()
                print("Resumed music")

        # Up/Down: Volume control
        if input_manager.is_pressed(pygame.K_UP):
            vol = audio.get_music_volume()
            audio.set_music_volume(min(1.0, vol + 0.02))
        if input_manager.is_pressed(pygame.K_DOWN):
            vol = audio.get_music_volume()
            audio.set_music_volume(max(0.0, vol - 0.02))

    def draw(self, obj):
        """SoundTestScript doesn't need drawing."""
        pass
