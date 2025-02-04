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
        for object in self.objects:
            object.update()
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
                    if pivot_x == "center": pivot_x = image.width//2
                    elif pivot_x == "end": pivot_x = image.width-1
                    pivot_y = component_data.get("pivot_y", 0)
                    if pivot_y == "center": pivot_y = image.height//2
                    elif pivot_y == "end": pivot_y = image.height-1
                    component.set_pivot(pivot_x, pivot_y)
                    object.add_component("image", component)
                elif component_data["type"] == "animation":
                    animation = Animation(component_data["file"], component_data.get("speed", 1), component_data.get("loop", True))
                    object.add_component("animation", AnimationComponent(animation))
                elif component_data["type"] == "custom":
                    object.add_component(component_data["file"], CustomComponent(component_data["file"]))
                elif component_data["type"] == "ysort":
                    object.add_component("ysort", YSortComponent())

            scene.add_object(object)

        return scene
