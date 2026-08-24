from logging import Logger

from src.web_scraper.web_scrapper import WebScraper

from src.config.config import Settings
from src.logger.logger import AppLogger


def main() -> int:
    logger: Logger = AppLogger().get_logger(class_name=str(__name__))
    settings: Settings = Settings()

    web_scraper: WebScraper = WebScraper(settings=settings)

    try:
        # logger.info(f"Inside main() method")

        database_client.create_player_table()

        return 0
    except Exception as e:

        logger.error(e)
        raise Exception(e)


if __name__ == "__main__":
    main()
