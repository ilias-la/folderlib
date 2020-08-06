"""
Cleaner package for Python.

To use, simply 'import cleaner' and clean away!
"""

# Standard library imports
import os
import shutil
from distutils.util import strtobool
from pathlib import Path
from typing import Dict, Union, Optional, List

# Third party imports
import numpy

# Local application imports
from folderlib.utilities.logging import get_console_logger
from folderlib.utilities.typing import BOOL_TYPES, SUP_EXC_TYPES, PATH_TYPES
from folderlib.exceptions import EmptyDirectory, EmptyPath, CleanedMatch
from folderlib.workers import BaseWorker

logger = get_console_logger(name="Cleaner")


class Cleaner(BaseWorker):

    def __init__(
        self,
        path: PATH_TYPES,
        save_to: str = "clean-folder",
        files_supported: Optional[SUP_EXC_TYPES] = None,
        files_excluded: Optional[SUP_EXC_TYPES] = None,
        group_unknowns: Optional[BOOL_TYPES] = False,
    ) -> None:
        super().__init__(name=None, path=path)

        if isinstance(save_to, str):
            self.save_to = self.path.joinpath(save_to).expanduser()
        elif isinstance(save_to, Path):
            self.save_to = save_to.expanduser()
        else:
            raise TypeError(f"Wrong type for 'save_to' option --> {type(save_to)}")

        self.files_supported = self.get_files_supported(pool=files_supported)
        self.files_excluded = self.get_files_excluded(pool=files_excluded)
        self.group_unknowns = strtobool(str(group_unknowns))

        self.analyzed = False

        self.FILES: List[Path] = list()

    def analyze_path(self):
        self.FILES = [entry for entry in self.path.iterdir() if entry.is_file()]
        if not self.FILES:
            raise EmptyDirectory()

        extensions = list()
        for file in self.FILES:
            extension = file.suffix.replace('.', '')  # omit the '.' in suffix from e.g ".exe" to "exe"
            extensions.append(extension)
        extensions, extensions_counts = numpy.unique(extensions, return_counts=True)
        logger.info(f"Found {len(extensions)} unique extensions")
        for extension, count in zip(extensions, extensions_counts):
            logger.info(f"{extension}: {count}")

    def __call__(self):
        if not self.path:
            raise EmptyPath()

        logger.info("Cleanup operation started")
        logger.info("Cleanup directory: %s" % self.path.absolute())
        logger.info("Creating %s directory" % self.save_to)

        try:
            self.save_to.mkdir(exist_ok=False)
        except FileExistsError:
            logger.debug(f"Folder {self.save_to} already exists.")

        self.analyze_path()

        for filepath in self.FILES:
            extension = filepath.suffix.replace('.', '')  # omit the '.' in suffix from e.g ".exe" to "exe"
            # check if extension is blacklisted
            try:
                for _, filetypes in self.files_excluded.items():
                    if any(name == extension for name in filetypes):
                        logger.debug(f"'.{extension}' recognized as excluded type. Skipping file..")
                        raise CleanedMatch()

                # check if extension exists in any category supported
                for category_name, filetypes in self.files_supported.items():
                    if any(name == extension for name in filetypes):
                        logger.debug(f"'.{extension}' recognized as supported type. Moving now...")
                        category_path = self.save_to.joinpath(category_name)
                        category_path.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(filepath), str(category_path))
                        raise CleanedMatch()

                # the file is unrecognized at this point
                if self.group_unknowns:
                    logger.debug(f"'.{extension}' is not recognized. Moving to unknowns now...")
                    unknowns_path = self.save_to.joinpath("unknowns")
                    unknowns_path.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(filepath), str(unknowns_path))
            except CleanedMatch:
                continue
