#!/usr/bin/env python3
"""Visual test for collision system - automated movement."""

import sys
sys.path.insert(0, '/home/imns/Desktop/pygamer')

from pygaminal.app import App
from pygaminal.scene import Scene
from pygaminal.object import Object
from pygaminal.script_component import ScriptComponent

# Initialize app
app = App()
app.init(800, 600, "Visual Collision Test")

# Load scene
scene = Scene.get_scene_from_json("scene_data.json")
app.add_scene("test", scene)

# Apply pending updates
scene._apply_pending_updates()

# Get player
player = scene.get_object("player")

# Replace PlayerMovementScript with AutoMovementScript
del player.components["PlayerMovementScript"]
player.add_component(ScriptComponent("AutoMovementScript", []))

print("=== Visual Collision Test ===")
print("Player will move left/right automatically")
print("Watch for:")
print("  - Player stopping at walls")
print("  - Player pushing boxes")
print("\nPress Ctrl+C or close window to stop\n")

try:
    app.run()
except KeyboardInterrupt:
    print("\nTest stopped by user")
