

class Scene:
    def __init__(self):
        self.objects = []
    def add_object(self, object):
        self.objects.append(object)
    def draw(self):
        for object in self.objects:
            object.draw()
    def update(self):
        for object in self.objects:
            object.update()
