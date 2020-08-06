# Standard library imports
import os
import sys
import distutils.util
from random import choice, getrandbits
from pathlib import Path
from typing import Optional, Any, Union, Dict, List, Tuple

# Local application imports
from folderlib.utilities.logging import get_console_logger
from folderlib.utilities.typing import SUP_EXC_TYPES, FILTER_TYPES
from folderlib.workers.base import BaseWorker


logger = get_console_logger(name=__name__ if __name__ != "__main__" else "populator")


class Populator(BaseWorker):

    def __init__(
        self,
        path: Union[str, Path] = None,
        amount: Optional[int] = 50,
        supported_files: Optional[SUP_EXC_TYPES] = None,
        filters: Optional[FILTER_TYPES] = None
    ) -> None:
        super().__init__(name=None, path=path)
        self.amount = amount
        self.pool = self.get_files_supported(supported_files)
        self.filters = self.validate_filters(filters)

        self.special_keyword = True if self.filters == "all" else False
        if not self.special_keyword and self.filters:
            self.pool = dict(filter(lambda elem: elem[0] in self.filters, self.pool.items()))

        self.to_produce = len(self.pool.keys()) * self.amount

    def __call__(self):
        logger.info(f"Current directory:    {Path.cwd()}")
        logger.info(f"Population directory: {self.path.absolute()}")
        logger.info(f"Population amount:    {self.amount}")
        logger.info(f"Population types:     {','.join(self.pool.keys())}")
        logger.info(f"Population total to produce: {self.to_produce}")

        if not self.path.exists():
            logger.debug(f"Directory {self.path} does not exist. Creating now...")
            self.path.mkdir()

        for pop_name, pop_list in self.pool.items():
            for n in range(self.amount):
                rand_hash = getrandbits(64)
                extn = choice(pop_list)
                f = self.path.joinpath(f"{pop_name}_%016x_{n}.{extn}" % rand_hash)
                f.touch(exist_ok=True)
                logger.debug(f"Created file: {f}")

        logger.info("Populate operation finished.")
        logger.info(
            f"{self.to_produce} files created from "
            f"{len(self.pool)} different categories"
        )


