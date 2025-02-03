

class InputManager:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def init(self):
        self.initialized = True
        self.keys = []
    def is_pressed(self, key):
        return key in self.keys
    def update(self, stdscr):
        self.keys.clear()
        while True:
            key = stdscr.getch()
            if key == -1:
                break
            self.keys.append(key)
        stdscr.getch()
