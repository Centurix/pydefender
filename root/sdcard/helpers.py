import uos
from micropython import const


TYPE_DIRECTORY = const(0x4000)
TYPE_FILE = const(0x8000)


class Helpers:
    @staticmethod
    def is_dir(path):
        try:
            results = uos.stat(path)
            return bool(results[0] & TYPE_DIRECTORY)
        except OSError:  # File/dir doesn't exist
            return False

    @staticmethod
    def is_file(path):
        try:
            results = uos.stat(path)
            return bool(results[0] & TYPE_FILE)
        except OSError:  # File/dir doesn't exist
            return False

    @staticmethod
    def exists(path):
        try:
            uos.stat(path)
            return True
        except OSError:  # File/dir doesn't exist
            return False
