from gaminal.object import Object
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
            x = float(object_data["x"])
            y = float(object_data["y"])
            object = Object.from_data(object_data, x, y)
            scene.add_object(object)

        return scene
