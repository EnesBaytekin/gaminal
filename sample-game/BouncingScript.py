from pygaminal import *


class BouncingScript:
    """Bounces object back and forth."""

    def __init__(self, speed=100, range_x=100):
        self.speed = speed
        self.range_x = range_x
        self.start_x = 0
        self.direction = 1

    def update(self, obj):
        app = App()

        # Initialize start position
        if self.start_x == 0:
            self.start_x = obj.x

        # Get Movability component
        movability = obj.get_component("Movability")

        # Calculate movement
        dx = self.direction * self.speed * app.dt

        # Try to move using Movability (collision aware)
        if movability:
            success = movability.move_x(obj, dx)
            # If blocked by collision, reverse direction
            if not success:
                self.direction *= -1
        else:
            # Fallback to direct movement if no Movability component
            obj.x += dx

        # Bounce at edges
        if obj.x > self.start_x + self.range_x:
            self.direction = -1
        elif obj.x < self.start_x - self.range_x:
            self.direction = 1

    def draw(self, obj):
        """BouncingScript doesn't need drawing."""
        pass
