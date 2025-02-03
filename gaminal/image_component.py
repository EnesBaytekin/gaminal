from gaminal.component import Component
from gaminal.screen import Screen

class ImageComponent(Component):
    def __init__(self, image):
        self.image = image
    def draw(self, object):
        Screen().paste(self.image, object.x, object.y)
