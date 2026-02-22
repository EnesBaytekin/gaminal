import pygame
from gaminal.screen import Screen
from gaminal.input_manager import InputManager
from time import time


class App:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, width=800, height=600, title="PyGamer Game"):
        self.width = width
        self.height = height
        self.title = title
        Screen().init(width, height)
        pygame.display.set_caption(title)
        InputManager().init()
        self.running = False
        self.scenes = {}
        self.current_scene_name = None
        self.now = 0
        self.dt = 0
        self.target_fps = 60
        self.clock = pygame.time.Clock()

    def stop(self):
        self.running = False

    def add_scene(self, name, scene):
        self.scenes[name] = scene
        if self.current_scene_name is None:
            self.current_scene_name = name

    def set_scene(self, name):
        self.current_scene_name = name

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

            # Update
            input_manager.update()
            scene = self.get_current_scene()
            scene.update()

            # Draw
            screen.clear()
            scene.draw()
            screen.refresh()

            # Time management
            self.clock.tick(self.target_fps)
            self.now = time()
            self.dt = self.now - last_time
            last_time = self.now
