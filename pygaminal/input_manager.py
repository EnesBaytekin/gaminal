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

        # Joystick state
        pygame.joystick.init()
        self.joysticks = {}  # {joystick_id: pygame.joystick.Joystick}
        self.joystick_axes = {}  # {joystick_id: [axis_values]}
        self.joystick_buttons = {}  # {joystick_id: {button_index: pressed}}
        self.joystick_hats = {}  # {joystick_id: [hat_values]}
        self.just_pressed_joystick_buttons = {}  # {joystick_id: set(button_indices)}
        self.released_joystick_buttons = {}  # {joystick_id: set(button_indices)}

        # Initialize all connected joysticks
        self._init_joysticks()

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

    # Joystick methods
    def get_joystick_count(self):
        """Get number of connected joysticks."""
        return len(self.joysticks)

    def is_joystick_connected(self, joystick_id=0):
        """Check if a joystick is connected."""
        return joystick_id in self.joysticks

    def get_joystick_name(self, joystick_id=0):
        """Get the name of a joystick."""
        if joystick_id in self.joysticks:
            return self.joysticks[joystick_id].get_name()
        return None

    def get_axis(self, axis_index, joystick_id=0):
        """
        Get joystick axis value.

        Args:
            axis_index: Axis index (0=left stick X, 1=left stick Y, 2=right stick X, 3=right stick Y, etc.)
            joystick_id: Joystick ID (default: 0)

        Returns:
            float: Axis value from -1.0 to 1.0 (0.0 = centered)
        """
        if joystick_id in self.joystick_axes:
            axes = self.joystick_axes[joystick_id]
            if axis_index < len(axes):
                return axes[axis_index]
        return 0.0

    def get_button_pressed(self, button_index, joystick_id=0):
        """
        Check if joystick button is currently pressed.

        Args:
            button_index: Button index (0=A, 1=B, 2=X, 3=Y on Xbox controllers)
            joystick_id: Joystick ID (default: 0)
        """
        if joystick_id in self.joystick_buttons:
            return self.joystick_buttons[joystick_id].get(button_index, False)
        return False

    def get_button_just_pressed(self, button_index, joystick_id=0):
        """
        Check if joystick button was pressed this frame.

        Args:
            button_index: Button index
            joystick_id: Joystick ID (default: 0)
        """
        if joystick_id in self.just_pressed_joystick_buttons:
            return button_index in self.just_pressed_joystick_buttons[joystick_id]
        return False

    def get_button_released(self, button_index, joystick_id=0):
        """
        Check if joystick button was released this frame.

        Args:
            button_index: Button index
            joystick_id: Joystick ID (default: 0)
        """
        if joystick_id in self.released_joystick_buttons:
            return button_index in self.released_joystick_buttons[joystick_id]
        return False

    def get_hat(self, hat_index=0, joystick_id=0):
        """
        Get joystick hat (D-pad) value.

        Args:
            hat_index: Hat index (default: 0)
            joystick_id: Joystick ID (default: 0)

        Returns:
            tuple: (x, y) where x and y are -1, 0, or 1
                   (0, 0) = centered, (1, 0) = right, (-1, 0) = left, etc.
        """
        if joystick_id in self.joystick_hats:
            hats = self.joystick_hats[joystick_id]
            if hat_index < len(hats):
                return hats[hat_index]
        return (0, 0)

    def _init_joysticks(self):
        """Initialize all connected joysticks."""
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            self._add_joystick(i)

    def _add_joystick(self, joystick_id):
        """Add a joystick to the tracking system."""
        joystick = pygame.joystick.Joystick(joystick_id)
        joystick.init()

        self.joysticks[joystick_id] = joystick
        self.joystick_axes[joystick_id] = [0.0] * joystick.get_numaxes()
        self.joystick_buttons[joystick_id] = {}
        self.joystick_hats[joystick_id] = [(0, 0)] * joystick.get_numhats()
        self.just_pressed_joystick_buttons[joystick_id] = set()
        self.released_joystick_buttons[joystick_id] = set()

    def _remove_joystick(self, joystick_id):
        """Remove a joystick from the tracking system."""
        if joystick_id in self.joysticks:
            del self.joysticks[joystick_id]
            del self.joystick_axes[joystick_id]
            del self.joystick_buttons[joystick_id]
            del self.joystick_hats[joystick_id]
            del self.just_pressed_joystick_buttons[joystick_id]
            del self.released_joystick_buttons[joystick_id]

    def update(self):
        # Clear just_pressed and released from previous frame
        self.just_pressed_keys.clear()
        self.released_keys.clear()
        self.just_pressed_mouse_buttons.clear()
        self.released_mouse_buttons.clear()

        # Clear joystick just_pressed/released
        for joy_id in self.just_pressed_joystick_buttons:
            self.just_pressed_joystick_buttons[joy_id].clear()
        for joy_id in self.released_joystick_buttons:
            self.released_joystick_buttons[joy_id].clear()

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
            # Joystick events
            elif event.type == pygame.JOYDEVICEADDED:
                # A new joystick was connected
                self._add_joystick(event.device_index)
                print(f"Joystick {event.device_index} connected: {self.get_joystick_name(event.device_index)}")
            elif event.type == pygame.JOYDEVICEREMOVED:
                # A joystick was disconnected
                self._remove_joystick(event.instance_id)
                print(f"Joystick {event.instance_id} disconnected")
            elif event.type == pygame.JOYAXISMOTION:
                # Axis moved
                joy_id = event.joy
                axis = event.axis
                value = event.value
                if joy_id in self.joystick_axes:
                    if axis < len(self.joystick_axes[joy_id]):
                        self.joystick_axes[joy_id][axis] = value
            elif event.type == pygame.JOYBUTTONDOWN:
                # Button pressed
                joy_id = event.joy
                button = event.button
                if joy_id in self.joystick_buttons:
                    self.joystick_buttons[joy_id][button] = True
                    self.just_pressed_joystick_buttons[joy_id].add(button)
            elif event.type == pygame.JOYBUTTONUP:
                # Button released
                joy_id = event.joy
                button = event.button
                if joy_id in self.joystick_buttons:
                    self.joystick_buttons[joy_id][button] = False
                    self.released_joystick_buttons[joy_id].add(button)
            elif event.type == pygame.JOYHATMOTION:
                # Hat (D-pad) moved
                joy_id = event.joy
                hat = event.hat
                value = event.value
                if joy_id in self.joystick_hats:
                    if hat < len(self.joystick_hats[joy_id]):
                        self.joystick_hats[joy_id][hat] = value

        # Update mouse position every frame (in case no motion event)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Pump remaining events to keep window responsive
        pygame.event.pump()
