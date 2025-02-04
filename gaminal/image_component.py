from gaminal.component import Component
from gaminal.screen import Screen

class ImageComponent(Component):
    def __init__(self, image):
        self.image = image
        self.pivot_x = 0
        self.pivot_y = 0
    def set_pivot(self, x, y):
        if x == "center": x = self.image.width//2
        elif x == "end": x = self.image.width-1
        if y == "center": y = self.image.height//2
        elif y == "end": y = self.image.height-1
        self.pivot_x = x
        self.pivot_y = y
        return self
    def draw(self, object):
        Screen().paste(self.image, object.x-self.pivot_x, object.y-self.pivot_y)
