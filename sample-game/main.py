#!/usr/bin/env python3

from gaminal import App, Scene

def main():
    app = App()
    app.init()
    app.add_scene("main", Scene.get_scene_from_json("scene_data.json"))
    app.run()

if __name__ == "__main__":
    main()
