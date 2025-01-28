from screen import Screen
from time import sleep

class App:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance
    def init(self):
        self.screen = Screen()
        self.running = False
        self.scenes = {}
        self.current_scene_name = None
    def stop(self):
        self.running = False
    def add_scene(self, name, scene):
        self.scenes[name] = scene
        if self.current_scene_name is None:
            self.current_scene_name = name
    def set_scene(self, name):
        self.current_scene_name = self.scenes[name]
    def run(self):
        self.running = True
        while self.running:
            scene = self.scenes[self.current_scene_name]
            # update
            scene.update()
            # draw
            self.screen.clear()
            scene.draw()
            self.screen.print()
            sleep(0.1)
