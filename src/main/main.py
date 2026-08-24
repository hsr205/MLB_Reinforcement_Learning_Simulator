import asyncio
from logging import Logger

from src.config.config import Settings
from src.database.database_client import DatabaseClient
from src.logger.logger import AppLogger


async def main() -> int:
    logger: Logger = AppLogger().get_logger(class_name=str(__name__))
    settings: Settings = Settings()

    database_client: DatabaseClient = DatabaseClient(settings=settings)

    try:

        await database_client.insert_rows_into_player_table()

        return 0
    except Exception as e:

        logger.error(e)
        raise Exception(e)


if __name__ == "__main__":
    asyncio.run(main())
