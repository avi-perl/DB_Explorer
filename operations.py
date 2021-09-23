import pandas as pd
from colorama import init

from utils.sql_connection import get_engine
from utils.formatting import format_table


def table_with_column(column_name: str):
    """
    Returns a list of tables that have a column with the name passed as the column_name.
    :param column_name:
    :return:
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


twc = table_with_column
