"""Module docstring is used as command help text"""

import typer

import pandas as pd

from utils.formatting import format_table
from utils.db_explore import get_engine

app = typer.Typer()


@app.command()
def current_time():
    """Returns the current time, powered by the DB"""
    print(format_table(pd.read_sql("SELECT NOW() as CurrentTime", con=get_engine())))
