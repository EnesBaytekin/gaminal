from .app import App
from .component import Component
from .script_component import ScriptComponent
from .animation import Animation
from .image import Image
from .object import Object
from .scene import Scene
from .screen import Screen
from .util import *
from .input_manager import InputManager
from .audio_manager import AudioManager

import os as _pyg_os

# When pygaminal is imported from the build-tool CLI or from a compiled
# game binary we skip change_dir_to_main_dir() because:
#   - build tool  → CWD should stay wherever the user invoked it
#   - compiled exe → argv[0] resolves to the PyInstaller temp dir which
#                     doesn't contain the extracted data files
# import pygame is kept unconditional — run_app() and every sub-module
# need it in the module namespace.
if not _pyg_os.environ.get("_PYGAMINAL_BUILD"):
    change_dir_to_main_dir()

import pygame  # noqa: E402


def run_app(*scene_file_names):
    # Initialize pygame first
    pygame.init()

    # Load scenes to get dimensions
    scenes = {}
    for scene_file_name in scene_file_names:
        name = scene_file_name.split(".")[0]
        scene = Scene.get_scene_from_json(scene_file_name)
        scenes[name] = scene

    # Initialize app with the first scene's dimensions
    if scenes:
        first_scene = list(scenes.values())[0]
        width = first_scene.width
        height = first_scene.height
    else:
        width, height = 800, 600

    app = App()
    app.init(width=width, height=height, title="PyGamer Game")

    # Set background color from first scene
    if first_scene.background_color:
        Screen().set_background_color(first_scene.background_color)
    if first_scene.background_image:
        Screen().set_background_image(first_scene.background_image)

    # Add all scenes
    for name, scene in scenes.items():
        app.add_scene(name, scene)

    # Run the game
    try:
        app.run()
    finally:
        pygame.quit()
