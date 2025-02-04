from gaminal.component import Component

class YSortComponent(Component):
    def update(self, object):
        object.depth = object.y
