from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Callable

import pandas as pd
import typer
from sql_formatter.core import format_sql
from rich import print
from rich.console import Console
from rich.syntax import Syntax

from .engine import get_engine
from .formatting import format_table, TableFormatOptions
from settings import settings as conf

console = Console()


class QueryDataOperation:
    query: str
    __data: pd.DataFrame = pd.DataFrame()
    __result_count: int = None

    supported_export_types = [".csv", ".tsv", ".xlsx", ".json", ".html", ".xml"]

    def __init__(self, query: str):
        self.query = query

    @property
    def query_pretty(self) -> Syntax:
        """The query, formatted"""
        syntax = Syntax(format_sql(self.query), "sql", theme="monokai")
        return syntax

    @property
    def query_minified(self) -> str:
        """The query, in one line"""
        return " ".join(self.query.replace("\n", " ").split())

    @property
    def data(self) -> pd.DataFrame:
        """The data selected as a dataframe"""
        if self.__data.empty:
            self.__data = pd.read_sql(self.query, get_engine())

        return self.__data

    def data_formatted(self, style: TableFormatOptions = conf.tabulate_tablefmt) -> str:
        """The data formatted as a table"""
        return format_table(self.data, style=style)

    @property
    def result_count(self) -> int:
        """The number of rows returned from the database"""
        if not self.__result_count:
            self.__result_count = len(self.data.index)

        return self.__result_count

    def do_print_pages(self, do: bool):
        """Helper function to print one row at a time"""
        if do:
            for index, row in self.data.iterrows():
                current_row = index + 1
                console.print(row)
                if current_row != self.result_count:
                    response = input(
                        f"\nRow {current_row}/{self.result_count} :: Enter for the next row "
                    )
                    console.print()

            raise typer.Exit()

    def do_show_query(self, show: bool, minify: bool, die: bool = False):
        """Helper function to display the query"""
        if show:
            if minify:
                console.print(self.query_minified)
            else:
                console.print(self.query_pretty)

            if die:
                raise typer.Exit()

    def do_save_output(self, output_file_path: Optional[Path], die: bool = False):
        """Helper function to save data"""
        if output_file_path:
            file_type = output_file_path.suffix.lower()

            if file_type in self.supported_export_types:
                if file_type == ".csv":
                    self.data.to_csv(str(output_file_path), index=False)
                elif file_type == ".tsv":
                    self.data.to_csv(str(output_file_path), sep="\t", index=False)
                elif file_type == ".xlsx":
                    self.data.to_excel(str(output_file_path), index=False)
                elif file_type == ".json":
                    self.data.to_json(str(output_file_path))
                elif file_type == ".html":
                    self.data.to_html(str(output_file_path), index=False)
                elif file_type == ".xml":
                    self.data.to_xml(str(output_file_path), index=False)

                if die:
                    raise typer.Exit()

            else:
                raise ValueError(
                    f"The file type '{file_type}' is not supported. Supported types are: {self.supported_export_types}"
                )


@dataclass
class TyperParams:
    show_query: typer.Option = typer.Option(
        False, "--show-query", "-q", help="Display query instead of showing the results"
    )
    minified_query_format: typer.Option = typer.Option(
        False, "--minified-query", "-m", help="Minify the query when -q is passed"
    )
    print_pages: typer.Option = typer.Option(
        False, "--print-pages", "-p", help="Print one record at a time"
    )
    output: typer.Option = typer.Option(
        None,
        "--output",
        "-o",
        help=f"Path to export to. Supported types: {QueryDataOperation.supported_export_types}",
    )
    data_format: typer.Option = typer.Option(
        conf.tabulate_tablefmt,
        "--format",
        "-f",
        help=f"Formatting to use for data output",
        show_choices=True,
    )


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
