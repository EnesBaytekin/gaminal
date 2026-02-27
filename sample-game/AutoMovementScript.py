from pygaminal import *


class AutoMovementScript:
    """Automatically moves player left/right to demonstrate collision."""

    def __init__(self):
        self.time = 0
        self.direction = 1  # 1 = right, -1 = left

    def update(self, obj):
        app = App()
        self.time += app.dt

        # Change direction every 2 seconds
        if self.time > 2:
            self.time = 0
            self.direction *= -1

        # Get Movability and move
        movability = obj.get_component("Movability")
        if movability:
            movability = movability.instance
            speed = 150 * app.dt * self.direction
            movability.move_x(obj, speed)
