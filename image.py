

class Image:
    def __init__(self, width, height, alphachar=" "):
        self.width = width
        self.height = height
        self.alphachar = alphachar
        self.data = [[self.alphachar for y in range(self.height)] for x in range(self.width)]
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
                self.set(x + dx, y + dy, char)

if __name__ == "__main__":
    def draw(image):
        print("+", "-" * image.width, "+", sep="")
        for y in range(image.height):
            print("|", end="")
            for x in range(image.width):
                print(image.data[x][y], end="")
            print("|")
        print("+", "-" * image.width, "+", sep="")

    image = Image.from_data("""\
 ######
##    ##
#,,,,,,#
#......#
########""")
    draw(image)

    image2 = Image(4, 2)
    draw(image2)
    
    image2.set(0, 0, "A")
    image2.set(1, 1, "B")
    image2.set(2, 0, "C")
    image2.set(3, 1, "D")
    draw(image2)
    
    image.paste(image2, 4, 1)
    draw(image)
    
    image.paste(image2, 4, 2)
    draw(image)
    
    image2.fill("O")
    draw(image2)

    image2.alphachar = "@"
    image2.set(1, 1, image2.alphachar)
    image2.set(2, 1, " ")
    draw(image2)

    image.fill("*")
    image.paste(image2, 0, 2)
    draw(image)
