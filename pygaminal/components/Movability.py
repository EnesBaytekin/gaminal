from pygaminal.app import App
from pygaminal.util import check_collision_by_tags


class Movability:
    """Movement component with collision prevention."""

    def __init__(self, speed=200, collidables=None):
        """
        Initialize movement component.

        Args:
            speed: Movement speed (pixels per second)
            collidables: List of tags to collide with (default: ["collidable"])
        """
        self.speed = speed
        self.collidables = collidables if collidables else ["collidable"]

    def move_x(self, obj, dx):
        """
        Move object on X axis with collision detection.

        Args:
            obj: The object to move
            dx: Distance to move (can be negative)

        Returns:
            bool: True if movement successful, False if blocked
        """
        # Split large movements into smaller steps for better collision
        max_step = 10  # Maximum movement per step
        steps = max(1, int(abs(dx) / max_step))
        step_distance = dx / steps

        for i in range(steps):
            if not self._move_x_step(obj, step_distance):
                # This step was blocked, stop further movement
                return False

        return True

    def _move_x_step(self, obj, dx):
        """Single step of X movement with collision detection."""
        # Store old position
        old_x = obj.x

        # Try new position temporarily
        obj.x = old_x + dx

        # Get current scene
        scene = App().get_current_scene()

        # Check collision with collidable objects
        for tag in self.collidables:
            for other in scene.get_objects_by_tag(tag):
                if other is obj:
                    continue  # Skip self

                if check_collision_by_tags(obj, other, ["body"], ["body"]):
                    # Collision detected, restore position and don't move
                    obj.x = old_x
                    return False

        # No collision, keep new position
        return True

    def move_y(self, obj, dy):
        """
        Move object on Y axis with collision detection.

        Args:
            obj: The object to move
            dy: Distance to move (can be negative)

        Returns:
            bool: True if movement successful, False if blocked
        """
        # Split large movements into smaller steps for better collision
        max_step = 10  # Maximum movement per step
        steps = max(1, int(abs(dy) / max_step))
        step_distance = dy / steps

        for i in range(steps):
            if not self._move_y_step(obj, step_distance):
                # This step was blocked, stop further movement
                return False

        return True

    def _move_y_step(self, obj, dy):
        """Single step of Y movement with collision detection."""
        # Store old position
        old_y = obj.y

        # Try new position temporarily
        obj.y = old_y + dy

        # Get current scene
        scene = App().get_current_scene()

        # Check collision with collidable objects
        for tag in self.collidables:
            for other in scene.get_objects_by_tag(tag):
                if other is obj:
                    continue  # Skip self

                if check_collision_by_tags(obj, other, ["body"], ["body"]):
                    # Collision detected, restore position and don't move
                    obj.y = old_y
                    return False

        # No collision, keep new position
        return True

    def update(self, obj):
        """Movability doesn't need automatic updates."""
        pass

    def draw(self, obj):
        """Movability doesn't need drawing."""
        pass
