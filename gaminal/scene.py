from gaminal.object import Object
from gaminal.image import Image
from gaminal.image_component import ImageComponent
from gaminal.custom_component import CustomComponent
from json import load

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
    @classmethod
    def get_scene_from_json(cls, json_file):
        scene = cls()

        scene_data = load(open(json_file))

        for object_data in scene_data:
            object = Object(object_data["x"], object_data["y"])

            for component_data in object_data["components"]:
                if component_data["type"] == "image":
                    image = Image.from_file(component_data["file"])
                    object.add_component("image", ImageComponent(image))
                elif component_data["type"] == "custom":
                    object.add_component(component_data["file"], CustomComponent(component_data["file"]))

            scene.add_object(object)

        return scene
