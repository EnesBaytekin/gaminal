from gaminal.component import Component
from gaminal.app import App

class AnimationComponent(Component):
    def __init__(self, animation):
        self.animation = animation
    def draw(self, object):
        App().screen.paste(self.animation.get_frame(), object.x, object.y)

    
