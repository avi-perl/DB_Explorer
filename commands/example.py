"""Module docstring is used as command help text"""

import typer
from pathlib import Path
from typing import Optional

import pandas as pd
from rich import print

from utils.formatting import format_table, TableFormatOptions
from utils.db_tools import get_engine, QueryDataOperation
from utils.db_tools import TyperParams as tp

app = typer.Typer(hidden=True)


@app.command()
def current_time():
    """Returns the current time, powered by the DB"""
    print(format_table(pd.read_sql("SELECT NOW() as CurrentTime", con=get_engine())))


@app.command()
def op_example(
    show_query: bool = tp.show_query,
    minified_query_format: bool = tp.minified_query_format,
    print_pages: bool = tp.print_pages,
    output_file_path: Optional[str] = tp.output,
    formatting: TableFormatOptions = tp.data_format,
):
    """Example showing how to use the operations class for common use cases"""

    op = QueryDataOperation("SELECT NOW() UNION ALL SELECT NOW()")
    op.do_show_query(show_query, minified_query_format, die=True)
    op.do_save_output(Path(output_file_path) if output_file_path else None, die=True)
    op.do_print_pages(print_pages)

    print(op.data_formatted(formatting))
