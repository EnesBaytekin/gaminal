from pygaminal.app import App
from pygaminal.util import check_collision_by_tags


class Pushable:
    """Component that allows objects to be pushed by collisions."""

    def __init__(self, push_speed=100, push_tags=None):
        """
        Initialize pushable component.

        Args:
            push_speed: Speed at which object is pushed (pixels per second)
            push_tags: List of tags that can push this object (default: None = all)
        """
        self.push_speed = push_speed
        self.push_tags = push_tags  # None means any object can push
        self.last_x = 0
        self.last_y = 0

    def update(self, obj):
        """
        Check for collisions and push object if needed.

        Args:
            obj: The object this component is attached to
        """
        # Store last position
        self.last_x = obj.x
        self.last_y = obj.y

        # Get current scene
        scene = App().get_current_scene()

        # Check for collisions with objects that can push
        if self.push_tags is None:
            # Check all objects in scene
            pushers = scene.get_all_objects()
        else:
            # Check only objects with specific tags
            pushers = []
            for tag in self.push_tags:
                pushers.extend(scene.get_objects_by_tag(tag))

        # Check each potential pusher
        for pusher in pushers:
            if pusher is obj:
                continue  # Skip self

            # Check if pusher collided with this object
            if check_collision_by_tags(pusher, obj, ["body"], ["body"]):
                # Calculate push direction based on pusher's last movement
                # We'll use simple direction detection
                dx = 0
                dy = 0

                # Determine push direction based on relative positions
                # This is a simple approach - pusher pushes this object away
                if pusher.x > obj.x:
                    dx = -1  # Push left
                elif pusher.x < obj.x:
                    dx = 1   # Push right

                if pusher.y > obj.y:
                    dy = -1  # Push up
                elif pusher.y < obj.y:
                    dy = 1   # Push down

                # Normalize diagonal movement
                if dx != 0 and dy != 0:
                    dx *= 0.707  # 1/sqrt(2)
                    dy *= 0.707

                # Apply push
                import pygame
                app = App()
                dt = app.clock.get_time() / 1000.0
                obj.x += dx * self.push_speed * dt
                obj.y += dy * self.push_speed * dt

    def draw(self, obj):
        """Pushable doesn't need drawing."""
        pass
