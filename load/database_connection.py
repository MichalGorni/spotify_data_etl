import sqlite3
import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)


class DataBaseConnector:
    """
    Provides connection to sqlite database.
    """

    def __init__(self) -> None:
        self.connection = sqlite3.connect(rf"{BASE_DIR}\database.db")
        self.cursor = self.connection.cursor()

    def load_table_to_database(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Loads data from given DataFrame into give table in sqlite database.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame object containing data to be loaded into database.
        table_name: str
            Name of table to load data.
        """
        df.to_sql(table_name, self.connection, index=False, if_exists="append")
