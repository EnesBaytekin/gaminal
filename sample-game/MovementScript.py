

class MovementScript:
    def __init__(self):
        self.speed = 1
        self.timer = 0
    def update(self, object):
        self.timer += 1
        if self.timer % 10 == 0:
            self.speed *= -1
        object.x += self.speed
        
        if self.speed < 0:
            list(object.components.values())[0].image.set(0, 0, "<")
            list(object.components.values())[0].image.set(1, 0, ")")
        else:
            list(object.components.values())[0].image.set(0, 0, "(")
            list(object.components.values())[0].image.set(1, 0, ">")
