#!/usr/bin/env python3

from app import App
from my_scene import MyScene

def main():
    app = App()
    app.init()
    app.add_scene("main", MyScene())
    app.run()

if __name__ == "__main__":
    main()