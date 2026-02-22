from gaminal.object import Object
from json import load


class Scene:
    def __init__(self):
        self.objects = []
        self.width = 800
        self.height = 600
        self.background_color = None
        self.background_image = None

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
        with open(json_file) as f:
            scene_data = load(f)

        scene = cls()

        # Read scene properties
        if isinstance(scene_data, dict):
            # New format with properties
            scene.width = scene_data.get("width", 800)
            scene.height = scene_data.get("height", 600)
            scene.background_color = scene_data.get("background_color")
            scene.background_image = scene_data.get("background_image")
            objects_data = scene_data.get("objects", [])
        else:
            # Old format - array of objects directly
            objects_data = scene_data

        # Create objects
        for object_data in objects_data:
            x = float(object_data["x"])
            y = float(object_data["y"])
            obj = Object.from_data(object_data, x, y)
            scene.add_object(obj)

        return scene
