from gaminal import *

class ExplosionScript:
    def __init__(self, duration):
        self.timer = duration
    def update(self, object):
        self.timer -= App().dt
        if self.timer <= 0:
            object.kill()
