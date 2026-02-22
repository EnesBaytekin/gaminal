import pygame
from gaminal.image import Image
from gaminal.app import App


class Animation:
    def __init__(self, surfaces, speed=1, loop=True):
        self.images = [Image(surface) for surface in surfaces]
        self.width = max(img.width for img in self.images)
        self.height = max(img.height for img in self.images)
        self.speed = speed
        self.start_at = 0  # Will be set when first accessed or started
        self.loop = loop

    @classmethod
    def from_sprite_sheet(cls, path, frame_width, frame_height, frames=None, speed=1, loop=True):
        """Load animation from a sprite sheet.

        Args:
            path: Path to sprite sheet image
            frame_width: Width of each frame in pixels
            frame_height: Height of each frame in pixels
            frames: List of frame indices to use (e.g., [0,1,2,3]). If None, uses all frames.
            speed: Animation speed multiplier
            loop: Whether to loop the animation
        """
        surface = pygame.image.load(path)
        if pygame.display.get_surface():
            surface = surface.convert_alpha()
        sheet_width = surface.get_width()
        sheet_height = surface.get_height()

        cols = sheet_width // frame_width
        rows = sheet_height // frame_height

        if frames is None:
            # Use all frames in the sprite sheet, reading left-to-right, top-to-bottom
            frames = list(range(rows * cols))

        surfaces = []
        for frame_idx in frames:
            row = frame_idx // cols
            col = frame_idx % cols
            rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(surface, (0, 0), rect)
            surfaces.append(frame_surface)

        return cls(surfaces, speed, loop)

    @classmethod
    def from_files(cls, paths, speed=1, loop=True):
        """Load animation from multiple image files.

        Args:
            paths: List of image file paths
            speed: Animation speed multiplier
            loop: Whether to loop the animation
        """
        surfaces = []
        for path in paths:
            surface = pygame.image.load(path)
        if pygame.display.get_surface():
            surface = surface.convert_alpha()
            surfaces.append(surface)
        return cls(surfaces, speed, loop)

    def start(self):
        self.start_at = App().now

    def get_index(self):
        # Auto-start on first access if not started
        if self.start_at == 0:
            self.start()
        now = App().now
        delta_time = now - self.start_at
        delta_index = int(delta_time * self.speed)
        if not self.loop and delta_index >= len(self.images):
            return len(self.images) - 1
        return delta_index % len(self.images)

    def get_frame(self):
        return self.images[self.get_index()]

    def is_over(self):
        return not self.loop and self.get_index() == len(self.images) - 1
