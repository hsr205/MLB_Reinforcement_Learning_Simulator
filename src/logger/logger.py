import logging
import sys
from logging import Formatter
from logging import Logger
from logging import StreamHandler

from src.logger.logger_color_formatter import LoggerColorFormatter


class AppLogger:
    _is_configured: bool = False

    @classmethod
    def _configure_root_logger(cls) -> None:
        if cls._is_configured:
            return

        root_logger: Logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        formatter: Formatter = cls._create_formatter()
        handler: StreamHandler = cls._create_stream_handler(formatter)

        root_logger.addHandler(handler)

        cls._is_configured = True

    @staticmethod
    def _create_formatter() -> Formatter:
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format: str = "%Y-%m-%d %H:%M:%S"
        formatter: Formatter = LoggerColorFormatter(
            fmt=log_format,
            datefmt=date_format
        )
        return formatter

    @staticmethod
    def _create_stream_handler(formatter: Formatter) -> StreamHandler:
        handler: StreamHandler = StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        return handler

    @classmethod
    def get_logger(cls, class_name: str) -> Logger:
        cls._configure_root_logger()
        return logging.getLogger(class_name)