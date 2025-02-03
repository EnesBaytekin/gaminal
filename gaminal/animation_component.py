from gaminal.component import Component
from gaminal.screen import Screen

class AnimationComponent(Component):
    def __init__(self, animation):
        self.animation = animation
    def draw(self, object):
        Screen().paste(self.animation.get_frame(), object.x, object.y)

    
