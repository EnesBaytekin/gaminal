from gaminal.image import Image
from gaminal.app import App

class Animation:
    def __init__(self, path, speed=1, loop=True):
        with open(path) as file:
            frames_data = file.read().split("\nnext\n")
        self.images = [Image.from_data(data) for data in frames_data]
        self.speed = speed
        self.start_at = App().now
        self.loop = loop
    def start(self):
        self.start_at = App().now
    def get_index(self):
        now = App().now
        delta_time = now-self.start_at
        delta_index = int(delta_time*self.speed)
        if not self.loop and delta_index >= len(self.images):
            return len(self.images)-1
        return delta_index % len(self.images)
    def get_frame(self):
        return self.images[self.get_index()]
    def is_over(self):
        return not self.loop and self.get_index() == len(self.images)-1