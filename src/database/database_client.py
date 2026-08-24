from logging import Logger

from psycopg2.extensions import connection
from psycopg2.pool import SimpleConnectionPool

from src.config.config import Settings
from src.logger.logger import AppLogger
from src.utils.constants import Constants
from web_scrapper.web_scraper import WebScraper


# TODO: Add a REDIS or in-memory cache for read operations if appropriate
class DatabaseClient:

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._web_scraper: WebScraper = WebScraper(settings=self._settings)
        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)

        self._pool: SimpleConnectionPool = SimpleConnectionPool(
            minconn=Constants.POOL_MIN_CONNECTIONS,
            maxconn=Constants.POOL_MAX_CONNECTIONS,
            host=self._settings.db_host,
            port=self._settings.db_port,
            dbname=self._settings.db_name,
            user=self._settings.db_user
        )
        self._logger.info(
            f"Connection pool created — MIN: {Constants.POOL_MIN_CONNECTIONS}, MAX: {Constants.POOL_MAX_CONNECTIONS}"
        )

    def _get_connection(self) -> connection:
        return self._pool.getconn()

    def _release_connection(self, conn: connection) -> None:
        self._pool.putconn(conn)

    def close_pool(self) -> None:
        """Close all connections in the pool. Call when the application shuts down."""
        self._pool.closeall()
        self._logger.info("Connection pool closed")
        self._logger.info("=" * 100)

    ## ======================================================== CREATE TABLE METHODS ======================================================== ##

    def create_player_table(self) -> None:
        conn: connection = self._get_connection()
        try:
            self._logger.info("Creating player table")
            with conn.cursor() as cursor:
                cursor.execute(query=Constants.Queries.CREATE_PLAYER_TABLE_SCHEMA_QUERY_STR)
                conn.commit()
            self._logger.info("Successfully created player table")
        finally:
            self._release_connection(conn)
        self._logger.info("=" * 100)

    ## ======================================================== QUERY METHODS ======================================================== ##

    def get_result_dict_from_queried_table(self) -> dict[int, str]:
        conn: connection = self._get_connection()
        try:
            self._logger.info("Querying table from SQL database:")
            with conn.cursor() as cursor:
                # TODO: Find a way to do this less manually
                cursor.execute(query=Constants.Queries.QUERY_PLAYER_TABLE_FOR_ALL_MLB_PLAYERS)
                query_result_list: list[tuple] = cursor.fetchall()

            self._logger.info(f"Returned {len(query_result_list):,} rows from queried table")

            player_dict: dict[int, str] = {
                element[0]: element[1] for element in query_result_list
            }
        finally:
            self._release_connection(conn)
        self._logger.info("=" * 100)

        return player_dict

    ## ======================================================== INSERT INTO TABLE METHODS ======================================================== ##

    async def insert_rows_into_table(self,
                                     search_name: str,
                                     stats_list: list[tuple],
                                     entity_dict: dict[int, str],
                                     insert_query_str: str) -> None:
        entity_id: int | None = next(
            (entity_id for entity_id, name in entity_dict.items() if name == search_name),
            None)

        if entity_id is None:
            self._logger.warning(f"No entity_id found for '{search_name}' — skipping stats insert")
            return

        # Prepend player_id to each stats row tuple
        rows_with_entity_id: list[tuple] = [(entity_id, *row) for row in stats_list]

        conn: connection = self._get_connection()
        try:
            self._logger.info(f"Inserting {len(rows_with_entity_id):,} rows into table for {search_name}")
            with conn.cursor() as cursor:
                cursor.executemany(query=insert_query_str, vars_list=rows_with_entity_id)
                conn.commit()
            self._logger.info(f"Successfully inserted {len(rows_with_entity_id):,} rows into table")
        finally:
            self._release_connection(conn)
        self._logger.info("=" * 100)

    async def insert_rows_into_player_table(self) -> None:
        mlb_players_list: list[tuple] = await self._web_scraper.get_all_mlb_players_list()

        conn: connection = self._get_connection()
        try:
            self._logger.info(f"Inserting {len(mlb_players_list):,} rows in player table")
            with conn.cursor() as cursor:
                cursor.executemany(query=Constants.Queries.INSERT_INTO_PLAYER_TABLE_QUERY_STR,
                                   vars_list=mlb_players_list)
                conn.commit()
            self._logger.info(f"Successfully inserted {len(mlb_players_list):,} rows in player table")
        finally:
            self._release_connection(conn)
        self._logger.info("=" * 100)
