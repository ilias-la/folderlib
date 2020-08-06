import json
import os
from typing import Union, List, Dict, Any, Optional
from pathlib import Path

# Third party modules
from appdirs import AppDirs

from folderlib.exceptions import EmptyPath, MissingJsonFile, InvalidJsonFile, MissingCacheFile
from folderlib.utilities.typing import FILTER_TYPES, SUP_EXC_TYPES
from folderlib.data import supported, excluded


class BaseWorker(object):

    def __init__(
        self,
        path: Union[str, Path],
        name=None,
    ):
        if not path:
            raise EmptyPath()
        self.path = Path(path).expanduser()
        self.dirs = AppDirs(
            appname="worker" if not name else name,
            appauthor="FolderWonder",
            roaming=False,
            multipath=False,
        )

        self.cache_dir = Path(self.dirs.user_cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.cached_supported = self.cache_dir.joinpath(".fw_supported")
        self.cached_excluded = self.cache_dir.joinpath(".fw_excluded")

    def get_files_supported(self, pool) -> Dict:
        if self.cached_supported.exists():
            if not pool:
                return self.validate_json_file_and_get_data(self.cached_supported)
            else:
                # check what type is pool
                if isinstance(pool, (str, Path)):
                    # read data from pool file and update the cache
                    data = self.validate_json_file_and_get_data(pool)
                    return self.update_cached_file(data, mode="supported")
                elif isinstance(pool, dict):
                    return self.update_cached_file(pool, mode="supported")
                else:
                    raise TypeError(f"Invalid type for 'pool' option --> '{type(pool)}'")
        else:
            if not pool:
                # just return the defaults without creating a file
                return self.get_default_supported()
            else:
                # user provided custom values so create cache file
                self.create_cache_file(items=pool, mode="supported")
                return self.validate_json_file_and_get_data(self.cached_supported)

    def get_files_excluded(self, pool):
        if self.cached_excluded.exists():
            if not pool:
                return self.validate_json_file_and_get_data(self.cached_excluded)
            else:
                # check what type is pool
                if isinstance(pool, (str, Path)):
                    # read data from pool file and update the cache
                    data = self.validate_json_file_and_get_data(pool)
                    return self.update_cached_file(data, mode="excluded")
                elif isinstance(pool, dict):
                    return self.update_cached_file(pool, mode="excluded")
                else:
                    raise TypeError(f"Invalid type for 'pool' option --> '{type(pool)}'")
        else:
            if not pool:
                # just return the defaults without creating a file
                return self.get_default_excluded()
            else:
                # user provided custom values so create cache file
                self.create_cache_file(items=pool, mode="excluded")
                return self.validate_json_file_and_get_data(self.cached_excluded)

    def create_cache_file(self, items, mode: str):
        cache_dir = Path(self.dirs.user_cache_dir)
        cache_dir.mkdir(exist_ok=True, parents=True)
        file_to_process: Path = self.supported_or_excluded_mode(choice=mode)
        with file_to_process.open("w") as f:
            json.dump(obj=items, fp=f, sort_keys=True, indent=4)

    def update_cached_file(self, data: Dict, mode: str):
        file_to_process: Path = self.supported_or_excluded_mode(choice=mode)

        if not file_to_process.exists():
            raise MissingCacheFile(file=file_to_process)
        else:
            cached_data = self.validate_json_file_and_get_data(file_to_process)
            for files_category, filetypes in data.items():
                if files_category not in cached_data:
                    cached_data[files_category] = filetypes
                else:
                    for filetype in filetypes:
                        if filetype not in cached_data[files_category]:
                            cached_data[files_category].append(filetype)
            with file_to_process.open("w") as f:
                json.dump(obj=cached_data, fp=f, sort_keys=True, indent=4)
        return self.validate_json_file_and_get_data(file_to_process)

    def supported_or_excluded_mode(self, choice: str):
        file_to_process: Path
        if choice.lower() not in ["supported", "excluded"]:
            raise ValueError(f"{choice} is not a cached file mode. Try one of [{','.join(['supported', 'excluded'])}]")
        elif choice.lower() == "supported":
            return self.cached_supported
        else:
            return self.cached_excluded

    @staticmethod
    def validate_filters(filters: FILTER_TYPES):
        if not filters:
            return "all"

        special_keywords = ["all", "random"]
        if isinstance(filters, str):
            # special keyword section
            if filters not in special_keywords:
                raise ValueError(f"Filters special keyword cannot be '{filters}'. Possible value are [{','.join(special_keywords)}]")
            return filters
        elif isinstance(filters, (list, tuple)):
            return filters
        else:
            raise TypeError(f"Invalid type for 'filters' argument --> '{type(filters)}'")

    @staticmethod
    def get_default_supported():
        return {
            "audio":       supported.audio,
            "compressed":  supported.compressed,
            "image":       supported.image,
            "spreadsheet": supported.spreadsheet,
            "text":        supported.text,
            "video":       supported.video
        }

    @staticmethod
    def get_default_excluded():
        return {
            "binaries": excluded.binaries,
            "symlinks": excluded.symlinks
        }

    @staticmethod
    def validate_json_file_and_get_data(file: Union[str, Path]):
        file = Path(file).expanduser()

        if not file.exists():
            raise MissingJsonFile(file)

        with file.open(mode="r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise InvalidJsonFile(file)
            return data
