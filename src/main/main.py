import asyncio
from logging import Logger

from data_processor.data_processor import DataProcessor
from src.config.config import Settings
from src.logger.logger import AppLogger


async def main() -> int:
    logger: Logger = AppLogger().get_logger(class_name=str(__name__))
    # settings: Settings = Settings()

    database_processor:DataProcessor = DataProcessor()

    try:

        database_processor.display_sample_statcast_data_retrieval()

        return 0
    except Exception as e:

        logger.error(e)
        raise Exception(e)


if __name__ == "__main__":
    asyncio.run(main())
