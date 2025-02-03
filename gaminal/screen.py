from gaminal.image import Image

class Screen(Image):
    def __init__(self, width=80, height=24):
        super().__init__(width, height)
        self.last_data = [[" " for _ in range(height)] for _ in range(width)]
    def print(self, stdscr):
        terminal_height, terminal_width = stdscr.getmaxyx()
        for x in range(self.width):
            for y in range(self.height):
                if 0 <= x < terminal_width and 0 <= y < terminal_height:
                    stdscr.addch(y, x, self.data[x][y])
        stdscr.refresh()
