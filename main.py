import glob
import importlib
from pathlib import Path
from typing import List
import pandas as pd

import typer
from utils.formatting import format_table
from utils.db_explore import get_engine

from utils.db_explore import DBSelect, DBOperation
from settings import settings as conf

app = typer.Typer()

# Import user defined commands
for item in glob.glob(f'{conf.user_defined_commands_dir_name}/*'):
    item = Path(item)
    if item.suffix == ".py":
        module_name = item.stem  # Name of file. Will be used as the command name.
        full_module_name = f"{conf.user_defined_commands_dir_name}.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
            if isinstance(module.app, typer.main.Typer):
                app.add_typer(module.app, name=module_name, help=module.__doc__)
        except AttributeError:
            # An attribute error will occur when a .py file does not have an app object.
            pass


@app.command()
def select(
        table: str,
        columns: List[str] = typer.Option([]),
        comma_columns: str = None,
        where: str = "",
):
    """Select data from database"""
    col = comma_columns.split(",") if comma_columns else []
    col = col + list(columns)

    db_explore = DBSelect(
        table_name=table,
        columns=set(col),
        where=where,
    )
    output = db_explore.get_output()

    typer.echo(output)


@app.command()
def table_with_column(column_name: str):
    """
    Returns a list of tables that have a column with the name passed as the column_name.
    """
    sql = f"""SELECT
              `COLUMN_NAME`,
              `TABLE_SCHEMA` as 'DATABASE',
              `TABLE_NAME`
            FROM
              `INFORMATION_SCHEMA`.`COLUMNS`
            WHERE
              `COLUMN_NAME` LIKE '{column_name}'"""

    df = pd.read_sql(sql, con=get_engine())

    return format_table(df)


@app.command()
def table_size(database: str = typer.Option("", help="Name of the database you want to examine")):
    """Returns the number of rows in each table, how much memory its using, and more"""
    query = """SELECT
                  CONCAT(table_schema, '.', table_name) table_name,
                  CONCAT(ROUND(table_rows / 1000000, 2), 'M') table_rows,
                  CONCAT(ROUND(data_length / (1024 * 1024 * 1024), 2), 'G') DATA,
                  CONCAT(ROUND(index_length / (1024 * 1024 * 1024), 2), 'G') idx,
                  CONCAT(
                    ROUND((data_length + index_length) / (1024 * 1024 * 1024), 2),
                    'G'
                  ) total_size,
                  ROUND(index_length / data_length, 2) idxfrac
                FROM
                  information_schema.TABLES"""
    query = f" {query} WHERE table_schema = '{database}'" if database else query
    query = f" {query} ORDER BY data_length + index_length DESC"

    df = pd.read_sql(query, con=get_engine())
    print(format_table(df))


if __name__ == "__main__":
    app()
