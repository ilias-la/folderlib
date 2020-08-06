# Standard library imports
import sys
import logging
import logging.handlers
import datetime
from typing import Union, Optional
from pathlib import Path

# Third party imports
import coloredlogs


def init_logger_from_file(filepath: Union[str, Path]) -> None:
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError("Logging YAML configuration file not found.")
    with open(filepath, "r") as f:
        pass
        # configs = yaml.safe_load(f.read())
        # logging.config.dictConfig(configs)


def get_console_logger(
    level: int = logging.INFO,
    name: str = None,
    enable_colors: bool = True,
    terminator: Optional[str] = None,
    disable_stream: bool = False,
    ) -> logging.Logger:
    """Utility function that creates a console logger

    :param level: logging level that the logger will use. Default: logging.INFO
    :param name: name of the logger. Default: __name__
    :param enable_colors: if True the console formatter will be colored. Default: True
    :param terminator: Terminating character for each log message
    :param disable_stream: Disables all stream messages (for silent mode)
    :return: logging.Logger object
    """

    logger = logging.getLogger(__name__ if name is None else name)  # create basic logger object
    log_format = "[%(asctime)s][%(name)s] %(levelname)s %(message)s"
    if enable_colors and not disable_stream:
        # Auto setup the logger with coloredlogs package
        coloredlogs.install(
            logger=logger,
            level=level,
            fmt=log_format,
            stream=sys.stdout,
            field_styles={
                'asctime':   {'color': 'blue', 'bright': True},  # blue color
                'levelname': {'color': 178, 'bold': True},  # gold color
                },
            level_styles={
                'debug':    {'color': 6},
                'info':     {'color': 6},
                'warning':  {'color': 'white'},
                'error':    {'color': 'red'},
                'critical': {'color': 'red', 'bold': True},
                }
            )
    else:
        # Manually setup a console handler for the logger
        stream_formatter = logging.Formatter(log_format)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(stream_formatter)
        stream_handler.setLevel(level=level)

        logger.setLevel(level=level)
        if not disable_stream:
            logger.addHandler(stream_handler)

    if terminator and not disable_stream:
        logger.handlers[0].terminator = terminator

    return logger


def get_rotating_file_logger(
    level: int = logging.INFO,
    name: str = None,
    log_root: Union[str, Path] = None,
    log_file: str = None,
    log_file_size: int = 19 * 1024 * 1024,
    log_history_file_count: int = 5,
    ):
    """Utility function that creates a logger with a Rotating File Handler

    :param level: logging level that the logger will use. Default: logging.INFO
    :param name: name of the logger. Default: __name__
    :param log_root: log folder path. Default: None
    :param log_file: log file name that will be used. Default: [timestamp]
    :param log_file_size: Size for rotating log files. Default: 20 MB
    :param log_history_file_count: Default: 5
    :return: logging.Logger object
    """

    # check if log root exists (if argument provided)
    if not log_root:
        raise ValueError("log_root argument missing - You didn't specify logs root folder.")

    # format of log messages
    log_format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # create basic logger object
    logger = logging.getLogger(__name__ if name is None else name)

    log_root = Path(log_root)
    if not log_root.exists():
        log_root.mkdir()

    log_file = (
        log_root.joinpath(datetime.date.today().strftime("%d-%m-%Y %H_%M_%S.log"))
        if not log_file
        else log_root.joinpath(
            log_file if log_file.endswith(".log")
            else f"{log_file}.log"
            )
    )

    log_file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        mode='a',
        maxBytes=log_file_size,
        backupCount=log_history_file_count,
        encoding="utf-8",
        delay=False
        )
    log_file_handler.setFormatter(log_format)
    log_file_handler.setLevel(logging.INFO)

    logger.setLevel(level=level)
    logger.addHandler(log_file_handler)

    return logger

