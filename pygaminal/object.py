from pygaminal.script_component import ScriptComponent
from json import load


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.components = {}
        self.dead = False

    @classmethod
    def from_file(cls, file_name, x, y):
        return cls.from_data(load(open(file_name)), x, y)

    @classmethod
    def from_data(cls, object_data, x, y):
        object = cls(x, y)
        for component_data in object_data["components"]:
            file_name = component_data["file"]
            args = component_data.get("args", ())

            # Load component using ScriptComponent
            component = ScriptComponent(file_name, args)

            # Use file_name as component key (without @ and path)
            key = file_name.split("/")[-1].split("\\")[-1]
            if key.startswith("@"):
                key = key[1:]

            object.add_component(key, component)
        return object

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
