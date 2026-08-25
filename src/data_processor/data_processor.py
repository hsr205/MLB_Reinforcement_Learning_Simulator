from datetime import datetime
from logging import Logger

from pandas import DataFrame
from pybaseball import playerid_lookup, statcast_batter

from logger.logger import AppLogger


class DataProcessor:

    def __init__(self) -> None:
        self._start_datetime_str: str = datetime(year=2026, month=3, day=25).strftime('%Y-%m-%d')
        self._current_datetime_str: str = datetime.today().strftime('%Y-%m-%d')
        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)

    def display_sample_statcast_data_retrieval(self) -> None:
        player_id_int: int = playerid_lookup(last='judge', first='aaron')['key_mlbam'][0]

        sample_stats_dataframe: DataFrame = statcast_batter(start_dt=self._start_datetime_str,
                                                            end_dt=self._current_datetime_str, player_id=player_id_int)

        self._logger.info(f"sample_stats_dataframe.columns = {sample_stats_dataframe.columns}")
