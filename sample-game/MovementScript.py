import pygame
from pygaminal import *


class MovementScript:
    def __init__(self):
        self.hspeed = 200
        self.vspeed = 200
        self.direction = 0
        self.last_shot = 0

    def update(self, object):
        input_manager = InputManager()
        dx = input_manager.is_pressed(pygame.K_d) - input_manager.is_pressed(pygame.K_a)
        dy = input_manager.is_pressed(pygame.K_s) - input_manager.is_pressed(pygame.K_w)

        app = App()
        object.x += dx * self.hspeed * app.dt
        object.y += dy * self.vspeed * app.dt

        # Keep player in bounds
        object.x = max(0, min(800, object.x))
        object.y = max(0, min(600, object.y))

        # Shoot with cooldown
        if input_manager.is_pressed(pygame.K_SPACE):
            if app.now - self.last_shot > 0.3:  # 300ms cooldown
                new_object = Object.from_file("explosion.obj", object.x + self.direction * 30, object.y)
                scene = app.get_current_scene()
                scene.add_object(new_object)
                self.last_shot = app.now
