from logging import Logger

from playwright.async_api import async_playwright
from src.web_scraper.web_scraper import WebScraper

from src.config.config import Settings
from src.database.database_client import DatabaseClient
from src.logger.logger import AppLogger


class DataLoader:

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._web_scraper: WebScraper = WebScraper(settings=self._settings)
        self._database_client: DatabaseClient = DatabaseClient(settings=settings)
        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)

    async def load_data_into_table(self, insert_query_str: str, entity_dict: dict[int, str]) -> None:

        try:
            async with async_playwright() as playwright_obj:
                async with await playwright_obj.chromium.launch(headless=False) as browser:
                    page = await browser.new_page()
                    await self._web_scraper.navigate_to_base_url(page=page)

                    for entity_id, entity_name in entity_dict.items():
                        try:
                            stats_list: list[tuple] = await self._web_scraper.scrape_stats(
                                page=page,
                                search_name=entity_name,
                            )

                            if not stats_list:
                                self._logger.warning(f"No stats found for {entity_name}, skipping")
                                continue

                            # Insert stats rows with the known entity_id
                            await self._database_client.insert_rows_into_table(
                                search_name=entity_name,
                                stats_list=stats_list,
                                entity_dict=entity_dict,
                                insert_query_str=insert_query_str
                            )

                        except Exception as entity_error:
                            self._logger.warning(
                                f"Failed to process '{entity_name}', skipping — reason: {entity_error}")
                            await self._web_scraper.navigate_to_base_url(page=page)
                            continue
        finally:
            self._logger.info("Closing connection pool")
            self._logger.info("=" * 100)
            self._database_client.close_pool()
