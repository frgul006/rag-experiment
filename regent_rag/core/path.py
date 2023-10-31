import os


def ensure_dir(directory: str) -> None:
    """
    Ensures that a directory exists. If it does not exist, it is created.

    Parameters:
    directory (str): The path of the directory to ensure.

    Returns:
    None
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
