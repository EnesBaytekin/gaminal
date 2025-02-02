from gaminal.image import Image
from sys import stdout

class Screen(Image):
    def __init__(self, width=80, height=24):
        super().__init__(width, height)
        self.last_data = [[" " for _ in range(height)] for _ in range(width)]
    def print(self):
        MOVE_CURSOR = "\033[{row};{col}H"
        stdout.write("\033[2J")
        for y in range(self.height):
            for x in range(self.width):
                if self.data[x][y] != self.last_data[x][y]:
                    stdout.write(MOVE_CURSOR.format(row=y, col=x))
                    stdout.write(self.data[x][y])
        stdout.write(MOVE_CURSOR.format(row=self.height, col=0))
        stdout.flush()
