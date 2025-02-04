from gaminal.screen import Screen
from gaminal.input_manager import InputManager
from time import sleep, time

class App:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance
    def init(self, stdscr):
        self.stdscr = stdscr
        Screen().init(80, 24)
        InputManager().init()
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
    def get_current_scene(self):
        return self.scenes[self.current_scene_name]
    def run(self):
        screen = Screen()
        input_manager = InputManager()
        self.now = time()
        last_time = self.now
        self.running = True
        while self.running:
            frame_start = time()
            #
            scene = self.get_current_scene()
            # update
            input_manager.update(self.stdscr)
            scene.update()
            # draw
            screen.clear()
            scene.draw()
            screen.print(self.stdscr)
            # time management
            elapsed_time = time()-frame_start
            sleep(max(0, 1/self.target_fps-elapsed_time))
            self.now = time()
            self.dt = self.now-last_time
            last_time = self.now
