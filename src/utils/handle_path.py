import os


def multiple_path_joins(paths):
    """
    Joins multiple paths together.
    """
    return os.path.join(*paths)
