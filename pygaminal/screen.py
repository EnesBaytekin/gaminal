import pygame


class Screen:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return
        self.initialized = True
        self.surface = None
        self.width = 0
        self.height = 0
        self.background_color = (0, 0, 0)
        self.background_image = None

    def init(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height), pygame.SCALED)

    def set_background_color(self, color):
        if isinstance(color, str):
            # Convert hex color to RGB tuple
            color = color.lstrip('#')
            self.background_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        else:
            self.background_color = color
        self.background_image = None

    def set_background_image(self, image_path):
        from pygaminal.image import Image
        self.background_image = Image.from_file(image_path)

    def clear(self):
        if self.background_image:
            # Scale background image to fill screen
            scaled = pygame.transform.scale(
                self.background_image.surface,
                (self.width, self.height)
            )
            self.surface.blit(scaled, (0, 0))
        else:
            self.surface.fill(self.background_color)

    def blit(self, image, x, y):
        self.surface.blit(image.surface, (int(x), int(y)))

    def paste(self, image, x=0, y=0):
        self.blit(image, x, y)

    def refresh(self):
        pygame.display.flip()
