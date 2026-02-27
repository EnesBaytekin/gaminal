import pygame
from pygaminal import *


class PlayerMovementScript:
    """Player movement script using Movability component for collision."""

    def __init__(self, speed=200):
        self.speed = speed

    def update(self, obj):
        input_manager = InputManager()
        app = App()

        # Get input direction
        dx = input_manager.is_pressed(pygame.K_d) - input_manager.is_pressed(pygame.K_a)
        dy = input_manager.is_pressed(pygame.K_s) - input_manager.is_pressed(pygame.K_w)

        # Get Movability component
        movability = obj.get_component("Movability")
        if movability:
            movability = movability.instance
            # Use Movability component for collision-aware movement
            move_distance = self.speed * app.dt

            # Move X and Y separately for better collision handling
            if dx != 0:
                movability.move_x(obj, dx * move_distance)
            if dy != 0:
                movability.move_y(obj, dy * move_distance)
        else:
            # Fallback to simple movement if no Movability component
            obj.x += dx * self.speed * app.dt
            obj.y += dy * self.speed * app.dt

        # Keep player in bounds
        obj.x = max(0, min(800, obj.x))
        obj.y = max(0, min(600, obj.y))


class WASDMovementScript:
    """Simple WASD movement without collision (for comparison)."""

    def __init__(self, speed=200):
        self.speed = speed

    def update(self, obj):
        input_manager = InputManager()
        app = App()

        dx = input_manager.is_pressed(pygame.K_d) - input_manager.is_pressed(pygame.K_a)
        dy = input_manager.is_pressed(pygame.K_s) - input_manager.is_pressed(pygame.K_w)

        obj.x += dx * self.speed * app.dt
        obj.y += dy * self.speed * app.dt

        # Keep in bounds
        obj.x = max(0, min(800, obj.x))
        obj.y = max(0, min(600, obj.y))


class ArrowKeyMovementScript:
    """Arrow key movement with collision."""

    def __init__(self, speed=150):
        self.speed = speed

    def update(self, obj):
        input_manager = InputManager()
        app = App()

        dx = input_manager.is_pressed(pygame.K_RIGHT) - input_manager.is_pressed(pygame.K_LEFT)
        dy = input_manager.is_pressed(pygame.K_DOWN) - input_manager.is_pressed(pygame.K_UP)

        movability = obj.get_component("Movability")
        if movability:
            movability = movability.instance
            move_distance = self.speed * app.dt

            if dx != 0:
                movability.move_x(obj, dx * move_distance)
            if dy != 0:
                movability.move_y(obj, dy * move_distance)
        else:
            obj.x += dx * self.speed * app.dt
            obj.y += dy * self.speed * app.dt

        # Keep in bounds
        obj.x = max(0, min(800, obj.x))
        obj.y = max(0, min(600, obj.y))
