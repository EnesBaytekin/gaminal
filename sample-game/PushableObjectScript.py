"""Script that demonstrates pushable objects."""

from pygaminal import *


class PushableObjectScript:
    """Script for pushable objects - displays visual feedback."""

    def __init__(self):
        self.original_x = 0
        self.original_y = 0
        self.pushed = False

    def update(self, obj):
        # Store original position on first update
        if self.original_x == 0:
            self.original_x = obj.x
            self.original_y = obj.y

        # Check if object has been pushed (moved from original position)
        distance = ((obj.x - self.original_x)**2 + (obj.y - self.original_y)**2)**0.5
        self.pushed = distance > 5


class RotatingScript:
    """Rotates object around in a circle."""

    def __init__(self, radius=50, speed=2):
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.center_x = 0
        self.center_y = 0

    def update(self, obj):
        app = App()

        # Initialize center on first update
        if self.center_x == 0:
            self.center_x = obj.x
            self.center_y = obj.y

        # Update angle
        self.angle += self.speed * app.dt

        # Move in circle
        obj.x = self.center_x + self.radius * 0.01 * (app.now * self.speed)
        obj.y = self.center_y + self.radius * 0.01 * (app.now * self.speed)


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

        # Move
        obj.x += self.direction * self.speed * app.dt

        # Bounce at edges
        if obj.x > self.start_x + self.range_x:
            self.direction = -1
        elif obj.x < self.start_x - self.range_x:
            self.direction = 1


class ColorChangingScript:
    """Changes object color over time (demonstrates animation)."""

    def __init__(self):
        self.hue = 0

    def update(self, obj):
        app = App()
        self.hue = (self.hue + 100 * app.dt) % 360
        # This would require modifying the Image component to support tinting
        # For now, it's just a placeholder script
