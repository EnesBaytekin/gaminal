from pygaminal.script_component import ScriptComponent
from json import load


class Object:
    _id_counter = 0

    def __init__(self, x, y, name=None, tags=None):
        self.x = x
        self.y = y
        self.name = self._generate_name(name)
        self.tags = set(tags or [])
        self.components = {}  # {name: ScriptComponent}
        self.dead = False

        # Pending updates for scene sync (applied at end of frame)
        self._pending_tag_adds = set()
        self._pending_tag_removes = set()

    def _generate_name(self, name):
        """Generate a unique name for the object."""
        if name:
            return name
        generated = f"object_{Object._id_counter}"
        Object._id_counter += 1
        return generated

    def add_tag(self, tag):
        """Add a tag to this object. Takes effect in next frame for scene queries."""
        if tag in self.tags:
            return
        self.tags.add(tag)
        self._pending_tag_adds.add(tag)
        self._pending_tag_removes.discard(tag)

    def remove_tag(self, tag):
        """Remove a tag from this object. Takes effect in next frame for scene queries."""
        if tag not in self.tags:
            return
        self.tags.remove(tag)
        self._pending_tag_removes.add(tag)
        self._pending_tag_adds.discard(tag)

    def has_tag(self, tag):
        """Check if object has a specific tag. Works immediately."""
        return tag in self.tags

    def kill(self):
        """Mark object for removal at end of frame."""
        self.dead = True

    def _clear_pending_updates(self):
        """Clear pending updates (called by scene after applying)."""
        self._pending_tag_adds.clear()
        self._pending_tag_removes.clear()

    @classmethod
    def from_file(cls, file_name, x, y):
        return cls.from_data(load(open(file_name)), x, y)

    @classmethod
    def from_data(cls, object_data, x, y):
        name = object_data.get("name")
        tags = object_data.get("tags")

        object = cls(x, y, name=name, tags=tags)

        for component_data in object_data["components"]:
            file_name = component_data["file"]
            comp_name = component_data.get("name")  # Optional explicit name
            args = component_data.get("args", ())

            # Load component using ScriptComponent
            component = ScriptComponent(file_name, args)

            # Add component with name (explicit or auto-generated)
            object.add_component(component, explicit_name=comp_name)
        return object

    def add_component(self, component, explicit_name=None):
        """
        Add a component to this object.

        Args:
            component: ScriptComponent instance
            explicit_name: Optional explicit name. If not provided, generates from component.file_name.
        """
        file_name = component.file_name

        if explicit_name:
            # Use provided name directly
            name = explicit_name
        else:
            # Generate name from file_name
            # Remove @ prefix and path
            base_name = file_name.split("/")[-1].split("\\")[-1]
            if base_name.startswith("@"):
                base_name = base_name[1:]

            # Make unique if already exists
            name = base_name
            i = 2
            while name in self.components:
                name = f"{base_name}{i}"
                i += 1

        self.components[name] = component

    def get_component(self, name):
        """
        Get a component by its unique name.

        Args:
            name: Component name (unique key in components dict)

        Returns:
            ScriptComponent instance or None if not found
        """
        return self.components.get(name)

    def get_components(self, file_name):
        """
        Get all components of a specific type (file_name).

        Args:
            file_name: Component file name to filter by (e.g., "@ImageComponent", "MyScript")

        Returns:
            List of ScriptComponent instances matching the file_name
        """
        return [comp for comp in self.components.values() if comp.file_name == file_name]

    def draw(self):
        for component in self.components.values():
            component.draw(self)

    def update(self):
        for component in self.components.values():
            component.update(self)
