from pygaminal.image import Image
from pygaminal.screen import Screen


class ImageComponent:
    def __init__(self, image_or_path, pivot_x=0, pivot_y=0):
        """
        Initialize ImageComponent.

        Args:
            image_or_path: Image object or file path string
            pivot_x: Pivot X (0, "center", "end", or pixel value)
            pivot_y: Pivot Y (0, "center", "end", or pixel value)
        """
        if isinstance(image_or_path, str):
            self.image = Image.from_file(image_or_path)
        else:
            self.image = image_or_path

        self.pivot_x = self._parse_pivot(pivot_x, self.image.width)
        self.pivot_y = self._parse_pivot(pivot_y, self.image.height)

    def _parse_pivot(self, val, max_val):
        """Parse pivot value to pixel coordinate."""
        if val == "center":
            return max_val // 2
        elif val == "end":
            return max_val - 1
        return val

    def set_pivot(self, x, y):
        """Set pivot after initialization."""
        self.pivot_x = self._parse_pivot(x, self.image.width)
        self.pivot_y = self._parse_pivot(y, self.image.height)
        return self

    def update(self, obj):
        """Static image doesn't need updates."""
        pass

    def draw(self, obj):
        """Draw the image at object position."""
        Screen().paste(self.image, obj.x - self.pivot_x, obj.y - self.pivot_y)
