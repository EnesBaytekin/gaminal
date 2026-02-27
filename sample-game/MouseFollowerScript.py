from pygaminal import *


class MouseFollowerScript:
    """Object follows mouse cursor when left mouse button is held."""

    def __init__(self, follow_speed=300):
        self.follow_speed = follow_speed

    def update(self, obj):
        app = App()
        input_manager = InputManager()

        # Get mouse position
        mouse_x, mouse_y = input_manager.get_mouse_position()

        # Check if left mouse button is pressed
        if input_manager.is_mouse_pressed(1):
            # Calculate direction to mouse
            dx = mouse_x - obj.x
            dy = mouse_y - obj.y

            # Calculate distance
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Move towards mouse if not too close
            if distance > 5:
                # Normalize and scale by speed
                move_x = (dx / distance) * self.follow_speed * app.dt
                move_y = (dy / distance) * self.follow_speed * app.dt

                obj.x += move_x
                obj.y += move_y

        # Check for mouse click (just pressed)
        if input_manager.is_mouse_just_pressed(1):
            print(f"Left click at ({mouse_x}, {mouse_y})")

        # Check for right click
        if input_manager.is_mouse_just_pressed(3):
            print(f"Right click at ({mouse_x}, {mouse_y})")

    def draw(self, obj):
        """MouseFollowerScript doesn't need drawing."""
        pass
