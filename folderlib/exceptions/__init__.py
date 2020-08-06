__all__ = [
    "EmptyPath",
    "EmptyFilesList",
    "EmptyDirectory",
    "MissingJsonFile",
    "InvalidJsonFile",
    "MissingCacheFile",
    "CleanedMatch",
]

from pathlib import Path
from typing import Union


class _Error(Exception):
    """Base class for Cleaner exceptions."""

    def __init__(self, msg: str = ""):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class EmptyFilesList(_Error):
    """Raised when FILES list is empty in a Worker Object."""

    def __init__(self, msg: str = ""):
        super().__init__(msg=f"Required FILES list is empty. {msg}")


class EmptyPath(_Error):
    """Raised when path is not defined in worker"""

    def __init__(self, msg: str = ""):
        super().__init__(msg=f"Required path is empty. {msg}")


class EmptyDirectory(_Error):
    """Raised when a directory is empty in Cleaner Object."""

    def __init__(self, msg: str = "", dir_name: str = ""):
        super().__init__(msg=f"Directory {dir_name} is empty. {msg}")


class MissingJsonFile(_Error):
    """Raised when JSON file is missing"""

    def __init__(self, file: Union[str, Path], msg: str = "", ):
        super().__init__(msg=f"File {file} does not exists. {msg}")


class InvalidJsonFile(_Error):
    """Raised when JSON file is in invalid format"""

    def __init__(self, file: Union[str, Path], msg: str = "", ):
        super().__init__(msg=f"File {file} is not a valid JSON file. {msg}")


class MissingCacheFile(_Error):
    """Raised when cache file is missing"""

    def __init__(self, file: Union[str, Path], msg: str = "", ):
        super().__init__(msg=f"Cache File {file} does not exists. {msg}")


class CleanedMatch(_Error):
    """Raised when cleaner object is finished it's job"""

    def __init__(self):
        super().__init__()
