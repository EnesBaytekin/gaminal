from gaminal.image import Image

class Screen(Image):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if hasattr(self, "initialized"):
            self.initialized = True
            super().__init__(0, 0)
    def init(self, width, height):
        super().__init__(width, height)
    def print(self, stdscr):
        terminal_height, terminal_width = stdscr.getmaxyx()
        for x in range(self.width):
            for y in range(self.height):
                if 0 <= x < terminal_width and 0 <= y < terminal_height:
                    stdscr.addch(y, x, self.data[x][y])
        stdscr.refresh()
