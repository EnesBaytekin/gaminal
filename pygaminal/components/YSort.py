class YSort:
    """Component that sets object depth based on Y position for depth sorting."""

    def __init__(self):
        """No parameters needed."""
        pass

    def update(self, obj):
        """Update object depth based on Y position."""
        obj.depth = obj.y

    def draw(self, obj):
        """No drawing needed."""
        pass
