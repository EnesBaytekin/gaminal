from gaminal.component import Component
from gaminal.screen import Screen

class AnimationComponent(Component):
    def __init__(self, animation):
        self.animation = animation
        self.pivot_x = 0
        self.pivot_y = 0
    def set_pivot(self, x, y):
        if x == "center": x = self.animation.width//2
        elif x == "end": x = self.animation.width-1
        if y == "center": y = self.animation.height//2
        elif y == "end": y = self.animation.height-1
        self.pivot_x = x
        self.pivot_y = y
        return self
    def draw(self, object):
        Screen().paste(self.animation.get_frame(), object.x-self.pivot_x, object.y-self.pivot_y)
