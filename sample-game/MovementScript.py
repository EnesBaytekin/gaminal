from gaminal import *

class MovementScript:
    def __init__(self):
        self.speed = 10
        self.timer = App().now
    def update(self, object):
        self.timer += App().dt
        if self.timer > 2:
            self.speed *= -1
            self.timer = 0
        object.x += self.speed*App().dt
        
        image_component = object.get_component("image")
        if self.speed < 0:
            image_component.image.set(0, 0, "<")
            image_component.image.set(1, 0, ")")
        else:
            image_component.image.set(0, 0, "(")
            image_component.image.set(1, 0, ">")
