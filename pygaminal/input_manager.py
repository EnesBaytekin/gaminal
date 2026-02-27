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

        # Mouse state
        self.mouse_x = 0
        self.mouse_y = 0
        self.pressed_mouse_buttons = set()
        self.just_pressed_mouse_buttons = set()
        self.released_mouse_buttons = set()

    def is_pressed(self, key):
        return key in self.pressed_keys

    def is_just_pressed(self, key):
        return key in self.just_pressed_keys

    def is_released(self, key):
        return key in self.released_keys

    # Mouse methods
    def get_mouse_position(self):
        """Get current mouse position as (x, y) tuple."""
        return (self.mouse_x, self.mouse_y)

    def get_mouse_x(self):
        """Get current mouse X position."""
        return self.mouse_x

    def get_mouse_y(self):
        """Get current mouse Y position."""
        return self.mouse_y

    def is_mouse_pressed(self, button):
        """
        Check if mouse button is currently pressed.

        Args:
            button: Mouse button (1=left, 2=middle, 3=right, 4/5=side)
        """
        return button in self.pressed_mouse_buttons

    def is_mouse_just_pressed(self, button):
        """
        Check if mouse button was pressed this frame.

        Args:
            button: Mouse button (1=left, 2=middle, 3=right, 4/5=side)
        """
        return button in self.just_pressed_mouse_buttons

    def is_mouse_released(self, button):
        """
        Check if mouse button was released this frame.

        Args:
            button: Mouse button (1=left, 2=middle, 3=right, 4/5=side)
        """
        return button in self.released_mouse_buttons

    def update(self):
        # Clear just_pressed and released from previous frame
        self.just_pressed_keys.clear()
        self.released_keys.clear()
        self.just_pressed_mouse_buttons.clear()
        self.released_mouse_buttons.clear()

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
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.pressed_mouse_buttons.add(event.button)
                self.just_pressed_mouse_buttons.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in self.pressed_mouse_buttons:
                    self.pressed_mouse_buttons.remove(event.button)
                self.released_mouse_buttons.add(event.button)

        # Update mouse position every frame (in case no motion event)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Pump remaining events to keep window responsive
        pygame.event.pump()
