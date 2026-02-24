from importlib import import_module
from pygaminal.component import Component


class ScriptComponent(Component):
    """Universal component loader for both built-in and user-defined scripts."""

    def __init__(self, file_name, args=()):
        """
        Load a component script and instantiate it.

        Args:
            file_name: Script file name
                       - If starts with "@": loads from pygaminal.components (built-in)
                       - Otherwise: loads from user scripts directory
            args: Arguments to pass to component constructor
        """
        self.file_name = file_name

        # Determine if built-in or user script
        if file_name.startswith("@"):
            # Built-in component - pygaminal/components/
            module_name = file_name[1:]  # Remove @ prefix
            self.script = import_module(f"pygaminal.components.{module_name}")
            class_name = module_name
        else:
            # User script - load from current directory
            # Extract class name from file path (handle paths like "scripts/MyScript")
            path_parts = file_name.replace("\\", "/").split("/")
            class_name = path_parts[-1]  # Last part is the class name
            module_name = file_name.replace("/", ".").replace("\\", ".")
            # Remove .py extension if present
            if module_name.endswith(".py"):
                module_name = module_name[:-3]
                class_name = class_name[:-3]
            self.script = import_module(module_name)

        # Get the class and instantiate
        component_class = getattr(self.script, class_name)
        self.instance = component_class(*args)

    def draw(self, object):
        """Delegate draw to component instance if method exists."""
        if hasattr(self.instance, 'draw'):
            self.instance.draw(object)

    def update(self, object):
        """Delegate update to component instance if method exists."""
        if hasattr(self.instance, 'update'):
            self.instance.update(object)
