from pygaminal import *


class GamepadMovementScript:
    """Gamepad joystick movement with collision support."""

    def __init__(self, speed=200, joystick_id=0, deadzone=0.15):
        """
        Initialize gamepad movement.

        Args:
            speed: Movement speed (pixels per second)
            joystick_id: Which joystick to use (default: 0)
            deadzone: Axis deadzone (0.0 to 1.0) to prevent drift
        """
        self.speed = speed
        self.joystick_id = joystick_id
        self.deadzone = deadzone

    def update(self, obj):
        app = App()
        input_manager = InputManager()

        # Check if joystick is connected
        if not input_manager.is_joystick_connected(self.joystick_id):
            return

        # Get left stick axis values (0=X, 1=Y)
        axis_x = input_manager.get_axis(0, self.joystick_id)
        axis_y = input_manager.get_axis(1, self.joystick_id)

        # Apply deadzone
        if abs(axis_x) < self.deadzone:
            axis_x = 0
        if abs(axis_y) < self.deadzone:
            axis_y = 0

        # Get Movability component
        movability = obj.get_component("Movability")
        if movability:
            move_distance = self.speed * app.dt

            # Move X and Y separately for better collision handling
            if axis_x != 0:
                movability.move_x(obj, axis_x * move_distance)
            if axis_y != 0:
                movability.move_y(obj, axis_y * move_distance)
        else:
            # Fallback to simple movement if no Movability component
            obj.x += axis_x * self.speed * app.dt
            obj.y += axis_y * self.speed * app.dt

        # Keep in bounds
        obj.x = max(0, min(800, obj.x))
        obj.y = max(0, min(600, obj.y))

        # Check button presses for debug/info
        if input_manager.get_button_just_pressed(0, self.joystick_id):  # A button
            print(f"A button pressed at ({obj.x:.1f}, {obj.y:.1f})")
        if input_manager.get_button_just_pressed(1, self.joystick_id):  # B button
            print(f"B button pressed at ({obj.x:.1f}, {obj.y:.1f})")

    def draw(self, obj):
        """GamepadMovementScript doesn't need drawing."""
        pass
