

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.components = {}
        self.dead = False
    def kill(self):
        self.dead = True
    def add_component(self, name, component):
        self.components[name] = component
    def get_component(self, name):
        return self.components[name]
    def draw(self):
        for component in self.components.values():
            component.draw(self)
    def update(self):
        for component in self.components.values():
            component.update(self)
