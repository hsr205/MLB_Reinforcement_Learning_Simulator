import asyncio
from logging import Logger

from playwright.async_api import async_playwright, Page

from src.config.config import Settings
from src.logger.logger import AppLogger


class WebScraper:

    def __init__(self, settings: Settings) -> None:
        self._base_url: str = settings.base_url

        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)

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

                    all_mlb_players_tuple_list.extend(await self._extract_player_data(page=page))
                    await asyncio.sleep(1)

                self._logger.info(f"Total players gathered: {len(all_mlb_players_tuple_list):,}")

            self._logger.info("Browser closed successfully")

        return all_mlb_players_tuple_list

    async def _extract_player_data(self, page: Page) -> list[tuple[str, int, int, str]]:

        player_element_locator = await page.locator("#div_players_ > p").all()
        player_tuples_list: list[tuple[str, int, int, str]] = []

        for elem in player_element_locator:
            full_text_str: str = await elem.text_content()

            name_str: str = (await elem.locator("a").text_content()).strip()

            career_years_str: str = full_text_str.replace(name_str, "").strip()

            is_in_hall_of_fame_str: str = "Y" if "+" in career_years_str else "N"

            years_partition_str: str = career_years_str.partition("(")[2].partition(")")[0]

            start_year_str, end_year_str = years_partition_str.split("-")

            year_debuted_int: int = int(start_year_str)
            year_retired_int: int = int(end_year_str)

            player_tuples_list.append(
                (name_str, year_debuted_int, year_retired_int, is_in_hall_of_fame_str)
            )

        self._logger.info(f"Scraped {len(player_tuples_list):,} player rows")

        return player_tuples_list

    async def navigate_to_base_url(self, page: Page) -> None:
        self._logger.info(f"Navigating to {self._base_url}")
        await page.goto(url=self._base_url)

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
