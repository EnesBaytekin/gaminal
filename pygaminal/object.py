from pygaminal.script_component import ScriptComponent
from json import load


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.components = {}  # {name: ScriptComponent}
        self.dead = False

    @classmethod
    def from_file(cls, file_name, x, y):
        return cls.from_data(load(open(file_name)), x, y)

    @classmethod
    def from_data(cls, object_data, x, y):
        object = cls(x, y)
        for component_data in object_data["components"]:
            file_name = component_data["file"]
            name = component_data.get("name")  # Optional explicit name
            args = component_data.get("args", ())

            # Load component using ScriptComponent
            component = ScriptComponent(file_name, args)

            # Add component with name (explicit or auto-generated)
            object.add_component(file_name, component, explicit_name=name)
        return object

    def kill(self):
        self.dead = True

    def add_component(self, file_name, component, explicit_name=None):
        """
        Add a component to this object.

        Args:
            file_name: Component file name (type identifier)
            component: ScriptComponent instance
            explicit_name: Optional explicit name. If not provided, generates from file_name.
        """
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
