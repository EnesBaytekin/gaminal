

class Image:
    def __init__(self, width, height, alphachar=" "):
        self.width = width
        self.height = height
        self.alphachar = alphachar
        self.data = [[self.alphachar for y in range(self.height)] for x in range(self.width)]
    @classmethod
    def from_file(cls, path):
        with open(path) as file:
            first_line = file.readline()
            if first_line.startswith("alphachar="):
                alphachar = first_line[len("alphachar=")]
            else:
                alphachar = " "
                file.seek(0)
            data = file.read()
            while data[-1] == "\n":
                data = data[:-1]
            return cls.from_data(data, alphachar)
    @classmethod
    def from_data(cls, data, alphachar=" "):
        data = data.split("\n")
        width = max(len(line) for line in data)
        height = len(data)
        image = cls(width, height, alphachar)
        image.data = [[data[y][x] if x < len(data[y]) else image.alphachar for y in range(image.height)] for x in range(image.width)]
        return image
    def fill(self, char):
        for x in range(self.width):
            for y in range(self.height):
                self.data[x][y] = char
    def clear(self):
        self.fill(self.alphachar)
    def set(self, x, y, char):
        if not (0 <= x < self.width and 0 <= y < self.height): return
        self.data[x][y] = char
    def paste(self, image, x=0, y=0):
        """
        Paste `image` onto this image (`self`) at the given coordinates (x, y).
        """
        for dx in range(image.width):
            for dy in range(image.height):
                char = image.data[dx][dy]
                if char == image.alphachar: continue
                self.set(int(x+dx), int(y+dy), char)
    def debug_draw(image):
        print("+", "-" * image.width, "+", sep="")
        for y in range(image.height):
            print("|", end="")
            for x in range(image.width):
                print(image.data[x][y], end="")
            print("|")
        print("+", "-" * image.width, "+", sep="")

if __name__ == "__main__":
    image = Image.from_data("""\
 ######
##    ##
#,,,,,,#
#......#
########""")
    image.debug_draw()

    image2 = Image(4, 2)
    image2.debug_draw()
    
    image2.set(0, 0, "A")
    image2.set(1, 1, "B")
    image2.set(2, 0, "C")
    image2.set(3, 1, "D")
    image2.debug_draw()
    
    image.paste(image2, 4, 1)
    image.debug_draw()
    
    image.paste(image2, 4, 2)
    image.debug_draw()
    
    image2.fill("O")
    image2.debug_draw()

    image2.alphachar = "@"
    image2.set(1, 1, image2.alphachar)
    image2.set(2, 1, " ")
    image2.debug_draw()

    image.fill("*")
    image.paste(image2, 0, 2)
    image.debug_draw()
