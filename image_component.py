from component import Component
from app import App

class ImageComponent(Component):
    def __init__(self, image):
        self.image = image
    def draw(self, object):
        App().screen.paste(self.image, object.x, object.y)
    def update(self, object):
        pass
