import os
from contextlib import closing


def save_file(file_content: bytes, path: str, file_name: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)
    with closing(open(file_name, 'wb')) as _file:
        _file.write(file_content)


def get_file_list_from_directory(directory: str) -> any:
    if not os.path.isdir(directory):
        return []
    return os.listdir(directory)
