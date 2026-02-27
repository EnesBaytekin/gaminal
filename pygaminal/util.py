from os import system, name

if name == 'nt':
    def clear_terminal():
        system('cls')
else:
    def clear_terminal():
        system('clear')


def change_dir_to_main_dir():
    from sys import argv
    from os.path import dirname, abspath
    from os import chdir

    chdir(dirname(abspath(argv[0])))


def check_collision_by_tags(obj1, obj2, tags1, tags2):
    """
    Check collision between two objects using their hitboxes with specific tags.

    Args:
        obj1: First object
        obj2: Second object
        tags1: List of hitbox tags to check on obj1 (e.g., ["body"])
        tags2: List of hitbox tags to check on obj2 (e.g., ["body"])

    Returns:
        bool: True if any hitbox with matching tags collides, False otherwise
    """
    # Get hitbox components from both objects
    hitbox1_comp = obj1.get_component("Hitbox")
    hitbox2_comp = obj2.get_component("Hitbox")

    # If either doesn't have hitbox component, no collision
    if hitbox1_comp is None or hitbox2_comp is None:
        return False

    # Get the actual component instances (from ScriptComponent wrapper)
    hitbox1 = hitbox1_comp.instance if hasattr(hitbox1_comp, 'instance') else hitbox1_comp
    hitbox2 = hitbox2_comp.instance if hasattr(hitbox2_comp, 'instance') else hitbox2_comp

    # Get all world rects for both objects
    rects1 = hitbox1.get_world_rects(obj1)
    rects2 = hitbox2.get_world_rects(obj2)

    # Check all combinations
    for rect1 in rects1:
        for rect2 in rects2:
            if rect1.colliderect(rect2):
                return True

    return False


def check_collision_any(obj1, obj2):
    """
    Check collision between two objects using all their hitboxes.

    Args:
        obj1: First object
        obj2: Second object

    Returns:
        bool: True if any hitbox collides, False otherwise
    """
    return check_collision_by_tags(obj1, obj2, [], [])
