from gaminal.screen import Screen
from time import sleep, time

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
        self.now = 0
        self.dt = 0
        self.target_fps = 30
    def stop(self):
        self.running = False
    def add_scene(self, name, scene):
        self.scenes[name] = scene
        if self.current_scene_name is None:
            self.current_scene_name = name
    def set_scene(self, name):
        self.current_scene_name = self.scenes[name]
    def run(self):
        self.now = time()
        last_time = self.now
        self.running = True
        while self.running:
            frame_start = time()
            #
            scene = self.scenes[self.current_scene_name]
            # update
            scene.update()
            # draw
            self.screen.clear()
            scene.draw()
            self.screen.print()
            # time management
            elapsed_time = time()-frame_start
            sleep(max(0, 1/self.target_fps-elapsed_time))
            self.now = time()
            self.dt = self.now-last_time
            last_time = self.now
            