class Constants:
    LOGGER_COLOR_RESET: str = "\033[0m"
    LOGGER_COLOR_WHITE: str = "\033[60m"
    LOGGER_COLOR_ORANGE: str = "\033[33m"
    LOGGER_COLOR_DARK_RED: str = "\033[31m"

    POOL_MIN_CONNECTIONS: int = 1
    POOL_MAX_CONNECTIONS: int = 5

    class Queries:
        ## ======================================================== CREATE TABLE QUERIES ======================================================== ##

        CREATE_PLAYER_TABLE_SCHEMA_QUERY_STR: str = """
            CREATE TABLE IF NOT EXISTS player (
                id SERIAL PRIMARY KEY,
                player_name VARCHAR(100) NOT NULL,
                year_debuted INTEGER NOT NULL,
                year_retired INTEGER NOT NULL,
                hall_of_fame VARCHAR(1)
            )
        """

        ## ======================================================== INSERT TABLE QUERIES ======================================================== ##

        INSERT_INTO_PLAYER_TABLE_QUERY_STR: str = """
                      INSERT INTO player (
                            player_name,
                            year_debuted,
                            year_retired,
                            hall_of_fame
                      )
                        VALUES (%s, %s, %s, %s);
            """

        ## ======================================================== QUERY TABLE QUERIES ======================================================== ##

        QUERY_PLAYER_TABLE_FOR_ALL_MLB_PLAYERS: str = """
            SELECT id, player_name
            FROM player;
        """
