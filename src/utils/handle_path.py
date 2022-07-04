import os


def multiple_path_joins(paths):
    """
    Joins multiple paths together.
    """
    return os.path.join(*paths)


def create_dir(paths):
    """
    Creates directories if they don't exist.
    """
    actual_paths = []
    for path in paths:
        actual_paths.append(path)
        real_path = multiple_path_joins(actual_paths)
        if not os.path.exists(real_path):
            os.mkdir(real_path)
            with open(multiple_path_joins([real_path, "__init__.py"]), "w") as f:
                f.write("")