from scene import Scene
from object import Object
from image_component import ImageComponent
from image import Image

class MyScene(Scene):
    def __init__(self):
        super().__init__()
        object = Object(0, 0)
        image = Image.from_data(" ######\n#      #\n# o  o #\n#      #\n#  __  #\n#      #\n ######\n")
        object.add_component("image", ImageComponent(image))
        self.add_object(object)
    def update(self):
        self.objects[0].x += 1
