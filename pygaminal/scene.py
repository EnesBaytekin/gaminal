from pygaminal.object import Object
from json import load


class Scene:
    def __init__(self):
        self.objects = {}  # {name: Object}
        self._tags = {}  # {tag: [Object, ...]} - Fast lookup
        self._pending_objects = []  # Objects to add at end of frame
        self.width = 800
        self.height = 600
        self.background_color = None
        self.background_image = None

    def add_object(self, obj):
        """Add an object to the scene (takes effect at end of frame)."""
        self._pending_objects.append(obj)

    def remove_object(self, obj):
        """Remove an object from the scene (takes effect at end of frame)."""
        obj.kill()

    def get_object(self, name):
        """Get an object by its unique name."""
        return self.objects.get(name)

    def get_objects_by_tag(self, tag):
        """Get all objects that have a specific tag."""
        return self._tags.get(tag, [])

    def get_all_objects(self):
        """Get all objects in the scene."""
        return list(self.objects.values())

    def draw(self):
        """Draw all objects sorted by depth (lower depth = drawn first)."""
        objects = list(self.objects.values())
        for obj in sorted(objects, key=lambda o: o.depth):  # Sort by depth
            obj.draw()

    def update(self):
        """Update all objects and apply pending updates."""
        # Update all objects
        for obj in self.objects.values():
            obj.update()

        # Apply pending updates at end of frame
        self._apply_pending_updates()

    def _apply_pending_updates(self):
        """Apply all pending updates (add/remove objects, tag changes)."""
        # 1. Remove dead objects
        dead_objects = [obj for obj in self.objects.values() if obj.dead]
        for obj in dead_objects:
            self._remove_object_now(obj)

        # 2. Add pending objects
        for obj in self._pending_objects:
            self._add_object_now(obj)
        self._pending_objects.clear()

        # 3. Apply pending tag updates
        for obj in self.objects.values():
            # Add pending tags
            for tag in obj._pending_tag_adds:
                self._add_tag_now(obj, tag)

            # Remove pending tags
            for tag in obj._pending_tag_removes:
                self._remove_tag_now(obj, tag)

            # Clear pending
            obj._clear_pending_updates()

    def _add_object_now(self, obj):
        """Immediately add an object to the scene (internal use)."""
        # Handle name conflicts
        name = obj.name
        i = 2
        while name in self.objects:
            name = f"{obj.name}_{i}"
            i += 1
        obj.name = name

        # Add to objects dict
        self.objects[name] = obj

        # Add to tag index
        for tag in obj.tags:
            self._add_tag_now(obj, tag)

    def _remove_object_now(self, obj):
        """Immediately remove an object from the scene (internal use)."""
        # Remove from objects dict
        if obj.name in self.objects:
            del self.objects[obj.name]

        # Remove from tag index
        for tag in list(obj.tags):
            self._remove_tag_now(obj, tag)

    def _add_tag_now(self, obj, tag):
        """Immediately add a tag to the index (internal use)."""
        if tag not in self._tags:
            self._tags[tag] = []
        if obj not in self._tags[tag]:
            self._tags[tag].append(obj)

    def _remove_tag_now(self, obj, tag):
        """Immediately remove a tag from the index (internal use)."""
        if tag in self._tags and obj in self._tags[tag]:
            self._tags[tag].remove(obj)
            if not self._tags[tag]:
                del self._tags[tag]

    @classmethod
    def get_scene_from_json(cls, json_file):
        """Load a scene from a JSON file."""
        with open(json_file) as f:
            scene_data = load(f)

        scene = cls()

        # Read scene properties
        if isinstance(scene_data, dict):
            # New format with properties
            scene.width = scene_data.get("width", 800)
            scene.height = scene_data.get("height", 600)
            scene.background_color = scene_data.get("background_color")
            scene.background_image = scene_data.get("background_image")
            objects_data = scene_data.get("objects", [])
        else:
            # Old format - array of objects directly
            objects_data = scene_data

        # Create objects
        for object_data in objects_data:
            x = float(object_data["x"])
            y = float(object_data["y"])
            obj = Object.from_data(object_data, x, y)
            scene.add_object(obj)

        return scene
