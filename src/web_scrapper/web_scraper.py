import asyncio
from logging import Logger

from playwright.async_api import async_playwright, Page, Locator
from src.web_scraper.data_cleanser import DataCleanser
from tqdm import tqdm

from src.config.config import Settings
from src.logger.logger import AppLogger
from src.utils.constants import Constants


class WebScraper:

    def __init__(self, settings: Settings) -> None:
        self._base_url: str = settings.base_url

        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)

    async def insert_rows_into_player_table(self) -> None:
        mlb_players_list: list[tuple] = await self._web_scraper.get_all_mlb_players_list()

        conn: connection = self._get_connection()
        try:
            self._logger.info(f"Inserting {len(mlb_players_list):,} rows in player table")
            with conn.cursor() as cursor:
                cursor.executemany(query=Constants.Queries.INSERT_INTO_PLAYER_QUERY_STR, vars_list=mlb_players_list)
                conn.commit()
            self._logger.info(f"Successfully inserted {len(mlb_players_list):,} rows in player table")
        finally:
            self._release_connection(conn)
        self._logger.info("=" * 100)

    async def get_all_mlb_players_list(self) -> list[tuple]:
        all_mlb_players_tuple_list: list[tuple] = []

        async with async_playwright() as playwright_obj:
            self._logger.info("Launching Chromium browser")
            self._logger.info("=" * 100)

            async with await playwright_obj.chromium.launch(headless=False) as browser:
                page: Page = await browser.new_page()

                alphabet_list: list[str] = self._get_alphabet_list()

                for letter in alphabet_list:
                    await self.navigate_to_base_url(page=page)
                    await self._navigate_to_players_page(page=page, first_letter_of_last_name_str=letter)

                    all_mlb_players_tuple_list.extend(await self._extract_players_data(page=page))
                    await asyncio.sleep(1)

                self._logger.info(f"Total players gathered: {len(all_mlb_players_tuple_list):,}")

            self._logger.info("Browser closed successfully")

        return all_mlb_players_tuple_list

    async def _navigate_to_players_page(self, page: Page, first_letter_of_last_name_str: str) -> None:
        await page.get_by_role(role="link", name="Players", exact=False).first.click()
        self._logger.info("Players Link Clicked")
        await asyncio.sleep(1)
        await page.locator("#div_alphabet").get_by_role(role="link", name=first_letter_of_last_name_str.upper(),
                                                        exact=True).click()
        await asyncio.sleep(1)
        self._logger.info(
            f"Clicked on Players with last names starting with: '{first_letter_of_last_name_str.upper()}'")

    def _get_alphabet_list(self) -> list[str]:

        alphabet_list: list[str] = []

        for element in range(65, 91):
            ascii_character: str = chr(element)

            alphabet_list.append(ascii_character)

        return alphabet_list
