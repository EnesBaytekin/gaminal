from .app import App
from .component import Component
from .image_component import ImageComponent
from .custom_component import CustomComponent
from .animation_component import AnimationComponent
from .ysort_component import YSortComponent
from .animation import Animation
from .image import Image
from .object import Object
from .scene import Scene
from .screen import Screen
from .util import *
from .input_manager import InputManager

change_dir_to_main_dir()

import curses

def run_app(*scene_file_names):
    def run(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(1)
        
        app = App()
        app.init(stdscr)
        for scene_file_name in scene_file_names:
            name = scene_file_name.split(".")[0]
            scene = Scene.get_scene_from_json(scene_file_name)
            app.add_scene(name, scene)
        app.run()
    curses.wrapper(run)

