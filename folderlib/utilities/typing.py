"""Typing Declarations used by various components in the package

    [BOOL_TYPES]
        Many modules in the package use boolean options and in order to extend those for developers we use
        distutils.util.strtobool which "Converts a string representation of truth to true (1) or false (0)"

        True values are 'y', 'yes', 't', 'true', 'on', '1' and True
        False values are 'n', 'no', 'f', 'false', 'off', '0' and False

    [SUP_EXC_TYPES]
        Sort for supported-excluded-types, this type applies to all the arguments which need supported
        or excluded files.

        This argument can be a  PathLike object, applying to [PATH_TYPES] and also be a valid JSON file.
        It can also be a dictionary in this form:
        {
            "CATEGORY_NAME_doeS_nOT_matter":
            [
                "FILE_EXTENSION_1",
                "FILE_EXTENSION_2",
                "jpg",
                "txt",
                ...
            ]

            OR

            (
                "FILE_EXTENSION_1",
                "FILE_EXTENSION_2",
                ...
            )

        }

    [FILTER_TYPES]
        Mostly workers need this argument type to explicitly filter the files provided with [SUP_EXC_TYPES] arguments.
        For example, given an argument (or variable it does not matter) which implies to [SUP_EXC_TYPES] and another
        argument of [FILTER_TYPES] in one of these forms:

        x: FILTER_TYPES = "<special_keyword>"   # more about this below
        x: FILTER_TYPES = ["audio", "video", "custom_category1", ...]
        x: FILTER_TYPES = ("audio", "video", "custom_category1", ...)

        <special_keyword>
            The special keyword allowed in [FILTER_TYPES] specifies the filtering process which will be applied.
            Available keywords are:

                "all"       for allowing every category found in [SUP_EXC_TYPES] argument
                "random"    for choosing a random category from the ones that were found in [SUP_EXC_TYPES] argument

            The default is best to be "all" in functions that use [SUP_EXC_TYPES] and [FILTER_TYPES] combined

        Note: category names found in [FILTER_TYPES] argument that do not match ANY category name in [SUP_EXC_TYPES]
              are ignored.
"""

from typing import Union, Dict, List, Tuple
from pathlib import Path

BOOL_TYPES = Union[str, bool]

FILE_TYPES = Union[
    Dict[
        str,
        Union[
            List[str],
            Tuple[str, ...]  # For tuples of unknown size, we use one type and ellipsis
        ]
    ]
]

PATH_TYPES = Union[str, Path]

SUP_EXC_TYPES = Union[
    PATH_TYPES,
    FILE_TYPES,
]

FILTER_TYPES = Union[
    str,
    List[str],
    Tuple[str, ...]
]

