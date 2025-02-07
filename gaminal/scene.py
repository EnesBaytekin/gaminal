from gaminal.object import Object
from gaminal.image import Image
from gaminal.image_component import ImageComponent
from gaminal.animation import Animation
from gaminal.animation_component import AnimationComponent
from gaminal.custom_component import CustomComponent
from gaminal.ysort_component import YSortComponent
from json import load

class Scene:
    def __init__(self):
        self.objects = []
    def add_object(self, object):
        self.objects.append(object)
    def draw(self):
        for object in sorted(self.objects, key=lambda obj: obj.depth):
            object.draw()
    def update(self):
        dead_objects = []
        for object in self.objects:
            object.update()
            if object.dead:
                dead_objects.append(object)
        for object in dead_objects:
            self.objects.remove(object)
    @classmethod
    def get_scene_from_json(cls, json_file):
        scene = cls()

        scene_data = load(open(json_file))

        for object_data in scene_data:
            object = Object(object_data["x"], object_data["y"])

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

            scene.add_object(object)

        return scene
