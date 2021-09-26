from typing import Callable, Any, Optional
import pandas as pd

import typer
from .sql_connection import get_engine
from .formatting import format_table


def import_from(module: str, name: str) -> Optional[Callable]:
    module = __import__(module, fromlist=[name])
    try:
        return getattr(module, name)
    except AttributeError as e:
        typer.echo(f"There is no function named '{name}' that can be used as an operation.")
        return None


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


class DBOperation:
    __operation_output = None

    def __init__(self, operation: str, var: Any):
        op_function = import_from("operations", operation)
        if op_function:
            self.operation_function = op_function
        else:
            exit()

        self.var = var

    def _run_operation(self):
        self.__operation_output = self.operation_function(self.var)

    def get_output(self):
        self._run_operation()
        return self.__operation_output
