from logging import Logger

from logger.logger import AppLogger

# TODO: Leverage the PyBaseball library to extract relevant stat data
class DataProcessor:

    def __init__(self) -> None:
        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)