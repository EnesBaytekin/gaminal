from gaminal.image import Image
from gaminal.image_component import ImageComponent
from gaminal.animation import Animation
from gaminal.animation_component import AnimationComponent
from gaminal.custom_component import CustomComponent
from gaminal.ysort_component import YSortComponent
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
            if component_data["type"] == "image":
                image = Image.from_file(component_data["file"])
                component = ImageComponent(image)
                pivot_x = component_data.get("pivot_x", 0)
                pivot_y = component_data.get("pivot_y", 0)
                component.set_pivot(pivot_x, pivot_y)
                object.add_component("image", component)
            elif component_data["type"] == "animation":
                animation = Animation(component_data["file"], component_data.get("speed", 1), component_data.get("loop", True))
                component = AnimationComponent(animation)
                pivot_x = component_data.get("pivot_x", 0)
                pivot_y = component_data.get("pivot_y", 0)
                component.set_pivot(pivot_x, pivot_y)
                object.add_component("animation", component)
            elif component_data["type"] == "custom":
                component = CustomComponent(component_data["file"], component_data.get("args", ()))
                object.add_component(component_data["file"], component)
            elif component_data["type"] == "ysort":
                object.add_component("ysort", YSortComponent())
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
