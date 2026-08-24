import logging
from logging import Formatter

from src.utils.constants import Constants


class LoggerColorFormatter(Formatter):
    """
    Applies ANSI color codes based on log level.
    """

    def __init__(self, fmt: str, datefmt: str) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        message: str = super().format(record)
        color: str = self._get_color(record.levelno)
        colored_message: str = f"{color}{message}{Constants.LOGGER_COLOR_RESET}"
        return colored_message

    def _get_color(self, level_num: int) -> str:
        if level_num >= logging.ERROR:
            return Constants.LOGGER_COLOR_DARK_RED

        if level_num >= logging.WARNING:
            return Constants.LOGGER_COLOR_ORANGE

        if level_num >= logging.INFO:
            return Constants.LOGGER_COLOR_WHITE

        return Constants.LOGGER_COLOR_RESET