

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.components = {}
    def add_component(self, name, component):
        self.components[name] = component
    def draw(self):
        for component in self.components.values():
            component.draw(self)
    def update(self):
        for component in self.components.values():
            component.update(self)
