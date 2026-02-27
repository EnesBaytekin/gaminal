import pygame


class Rect:
    """Represents a single rectangular hitbox."""

    def __init__(self, offset_x, offset_y, width, height):
        """
        Initialize a hitbox rect.

        Args:
            offset_x: X offset from object position
            offset_y: Y offset from object position
            width: Width of the hitbox
            height: Height of the hitbox
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height

    def get_world_rect(self, obj):
        """
        Get the actual rect in world coordinates.

        Args:
            obj: The object this hitbox belongs to

        Returns:
            pygame.Rect: World coordinate rect
        """
        return pygame.Rect(
            obj.x + self.offset_x,
            obj.y + self.offset_y,
            self.width,
            self.height
        )


class Hitbox:
    """Component for managing hitboxes on an object."""

    def __init__(self, hitboxes=None):
        """
        Initialize with hitboxes.

        Args:
            hitboxes: Single Rect or list of Rects, or tuple/list (offset_x, offset_y, width, height)
        """
        self.hitboxes = []

        if hitboxes is None:
            return

        if isinstance(hitboxes, Rect):
            self.hitboxes = [hitboxes]
        elif isinstance(hitboxes, list) and len(hitboxes) > 0:
            # Check if it's a list of 4 numbers (single hitbox data)
            if len(hitboxes) == 4 and all(isinstance(x, (int, float)) for x in hitboxes):
                self.hitboxes = [Rect(*hitboxes)]
            else:
                # Assume it's a list of Rects or hitbox data
                self.hitboxes = hitboxes
        elif isinstance(hitboxes, dict):
            # Create from dict (JSON support)
            self.hitboxes = [Rect(
                hitboxes["x"],
                hitboxes["y"],
                hitboxes["width"],
                hitboxes["height"]
            )]
        elif isinstance(hitboxes, tuple) and len(hitboxes) == 4:
            # Create from tuple (x, y, width, height)
            self.hitboxes = [Rect(*hitboxes)]

    def add_hitbox(self, offset_x, offset_y, width, height):
        """Add a new hitbox to this component."""
        self.hitboxes.append(Rect(offset_x, offset_y, width, height))

    def get_hitbox(self, name):
        """Get a hitbox by name (not implemented - hitboxes don't have names)."""
        # Future: if we want named hitboxes
        return None

    def get_hitboxes(self):
        """Get all hitboxes."""
        return self.hitboxes

    def get_world_rects(self, obj):
        """Get all hitbox rects in world coordinates."""
        return [hb.get_world_rect(obj) for hb in self.hitboxes]

    def collides_with(self, other_hitbox, obj1, obj2):
        """
        Check if any of this object's hitboxes collides with another hitbox.

        Args:
            other_hitbox: Another Hitbox instance
            obj1: This object
            obj2: The other object

        Returns:
            bool: True if any hitbox collides, False otherwise
        """
        rect1_list = self.get_world_rects(obj1)
        rect2_list = other_hitbox.get_world_rects(obj2)

        for rect1 in rect1_list:
            for rect2 in rect2_list:
                if rect1.colliderect(rect2):
                    return True
        return False

    def draw(self, obj):
        """Draw hitboxes for debugging (optional)."""
        # Override in subclass or add debug drawing if needed
        pass

    def update(self, obj):
        """Hitbox doesn't need updates."""
        pass
