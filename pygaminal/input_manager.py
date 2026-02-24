import pygame


class InputManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self):
        self.initialized = True
        self.pressed_keys = set()
        self.just_pressed_keys = set()
        self.released_keys = set()

    def is_pressed(self, key):
        return key in self.pressed_keys

    def is_just_pressed(self, key):
        return key in self.just_pressed_keys

    def is_released(self, key):
        return key in self.released_keys

    def update(self):
        # Clear just_pressed and released from previous frame
        self.just_pressed_keys.clear()
        self.released_keys.clear()

        # Process pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                from pygaminal.app import App
                App().stop()
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
                self.just_pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)
                self.released_keys.add(event.key)

        # Pump remaining events to keep window responsive
        pygame.event.pump()
