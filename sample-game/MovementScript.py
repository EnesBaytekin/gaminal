

class MovementScript:
    def __init__(self):
        self.speed = 1
        self.timer = 0
    def update(self, object):
        self.timer += 1
        if self.timer % 10 == 0:
            self.speed *= -1
        object.x += self.speed
        
        image_component = object.get_component("image")
        if self.speed < 0:
            image_component.image.set(0, 0, "<")
            image_component.image.set(1, 0, ")")
        else:
            image_component.image.set(0, 0, "(")
            image_component.image.set(1, 0, ">")
