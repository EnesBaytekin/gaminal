from image import Image
from util import clear_terminal

class Screen(Image):
    def __init__(self, width=80, height=24):
        super().__init__(width, height)
    def print(self):
        clear_terminal()
        for y in range(self.height):
            for x in range(self.width):
                print(self.data[x][y], end="")
            print()
