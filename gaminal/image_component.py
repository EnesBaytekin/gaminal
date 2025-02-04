from gaminal.component import Component
from gaminal.screen import Screen

class ImageComponent(Component):
    def __init__(self, image):
        self.image = image
        self.pivot_x = 0
        self.pivot_y = 0
    def set_pivot(self, x, y):
        self.pivot_x = x
        self.pivot_y = y
    def draw(self, object):
        Screen().paste(self.image, object.x-self.pivot_x, object.y-self.pivot_y)
