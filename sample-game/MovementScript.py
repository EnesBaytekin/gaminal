from gaminal import *

class MovementScript:
    def __init__(self):
        self.hspeed = 40
        self.vspeed = 20
        self.timer = App().now
        self.direction = 0
    def update(self, object):
        input_manager = InputManager()
        dx = input_manager.is_pressed(ord("d"))-input_manager.is_pressed(ord("a"))
        dy = input_manager.is_pressed(ord("s"))-input_manager.is_pressed(ord("w"))

        app = App()
        object.x += dx*self.hspeed*app.dt
        object.y += dy*self.vspeed*app.dt

        image_component = object.get_component("image")
        if dx < 0:
            self.direction = -1
            image_component.image.set(0, 0, "<")
            image_component.image.set(1, 0, ")")
        elif dx > 0:
            self.direction = 1
            image_component.image.set(0, 0, "(")
            image_component.image.set(1, 0, ">")

        if input_manager.is_pressed(ord(" ")):
            new_object = Object.from_file("explosion.obj", object.x+self.direction*3, object.y)
            
            scene = app.get_current_scene()
            scene.add_object(new_object)
