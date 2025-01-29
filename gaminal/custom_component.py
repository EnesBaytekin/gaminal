from gaminal.component import Component
from importlib import import_module

class CustomComponent(Component):
    def __init__(self, file_name):
        self.script = import_module(file_name.split(".")[0])
        class_name = file_name.split(".")[0]
        self.instance = getattr(self.script, class_name)()
    def draw(self, object):
        if hasattr(self.instance, 'draw'):
            self.instance.draw(object)
    def update(self, object):
        if hasattr(self.instance, 'update'):
            self.instance.update(object)
