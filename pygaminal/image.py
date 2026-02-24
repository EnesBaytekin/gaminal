import pygame


class Image:
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

    @classmethod
    def from_file(cls, path):
        surface = pygame.image.load(path)
        # Only convert if display is already initialized
        if pygame.display.get_surface():
            surface = surface.convert_alpha()
        return cls(surface)

    def debug_draw(self):
        print(f"Image: {self.width}x{self.height}")
