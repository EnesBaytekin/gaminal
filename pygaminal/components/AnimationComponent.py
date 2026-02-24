from pygaminal.animation import Animation
from pygaminal.screen import Screen


class AnimationComponent:
    def __init__(self, animation_or_data, pivot_x=0, pivot_y=0):
        """
        Initialize AnimationComponent.

        Args:
            animation_or_data: Animation object or dict with sprite sheet data
                               Dict format: {"file": path, "frame_width": w, "frame_height": h,
                                            "frames": [indices], "speed": s, "loop": bool}
            pivot_x: Pivot X (0, "center", "end", or pixel value)
            pivot_y: Pivot Y (0, "center", "end", or pixel value)
        """
        if isinstance(animation_or_data, Animation):
            self.animation = animation_or_data
        elif isinstance(animation_or_data, dict):
            # Load from sprite sheet data
            data = animation_or_data
            self.animation = Animation.from_sprite_sheet(
                data["file"],
                data["frame_width"],
                data["frame_height"],
                frames=data.get("frames"),
                speed=data.get("speed", 1),
                loop=data.get("loop", True)
            )
        else:
            raise ValueError(f"Invalid animation data type: {type(animation_or_data)}")

        self.pivot_x = self._parse_pivot(pivot_x, self.animation.width)
        self.pivot_y = self._parse_pivot(pivot_y, self.animation.height)

    def _parse_pivot(self, val, max_val):
        """Parse pivot value to pixel coordinate."""
        if val == "center":
            return max_val // 2
        elif val == "end":
            return max_val - 1
        return val

    def set_pivot(self, x, y):
        """Set pivot after initialization."""
        self.pivot_x = self._parse_pivot(x, self.animation.width)
        self.pivot_y = self._parse_pivot(y, self.animation.height)
        return self

    def update(self, obj):
        """Animation updates automatically via App().now."""
        pass

    def draw(self, obj):
        """Draw current animation frame at object position."""
        Screen().paste(self.animation.get_frame(), obj.x - self.pivot_x, obj.y - self.pivot_y)
