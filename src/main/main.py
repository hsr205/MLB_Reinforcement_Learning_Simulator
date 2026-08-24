from logging import Logger

from src.logger.logger import AppLogger


def main() -> int:
    logger: Logger = AppLogger().get_logger(class_name=str(__name__))

    try:
        logger.info(f"Inside main() method")
        return 0
    except Exception as e:

        logger.error(e)
        raise Exception(e)


if __name__ == "__main__":
    main()
