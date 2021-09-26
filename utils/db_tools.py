import pandas as pd

import typer
from .engine import get_engine
from .formatting import format_table


class DBSelect:
    def __init__(self, table_name: str, columns: set, where: str = None):
        self.source = table_name
        self.columns = columns
        self.where = where

    def prepare_query(self) -> str:
        query = f"SELECT {','.join(self.columns)} FROM {self.source}"
        if self.where:
            query = f"{query} WHERE {self.where}"
        return query

    def get_output(self) -> str:
        query = self.prepare_query()
        df = pd.read_sql(query, con=get_engine())
        return format_table(df)
