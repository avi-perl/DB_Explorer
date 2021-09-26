from enum import Enum, auto

from tabulate import tabulate
from pandas import DataFrame

from settings import settings as conf


class TableFormatOptions(str, Enum):
    plain = "plain"
    simple = "simple"
    github = "github"
    grid = "grid"
    fancy_grid = "fancy_grid"
    pipe = "pipe"
    orgtbl = "orgtbl"
    jira = "jira"
    presto = "presto"
    pretty = "pretty"
    psql = "psql"
    rst = "rst"
    mediawiki = "mediawiki"
    moinmoin = "moinmoin"
    youtrack = "youtrack"
    html = "html"
    unsafehtml = "unsafehtml"
    latex = "latex"
    latex_raw = "latex_raw"
    latex_booktabs = "latex_booktabs"
    latex_longtable = "latex_longtable"
    textile = "textile"
    tsv = "tsv"


def format_table(
    df: DataFrame, style: TableFormatOptions = conf.tabulate_tablefmt
) -> str:
    return tabulate(df, headers=conf.tabulate_headers, tablefmt=style)


if __name__ == "__main__":
    import pandas as pd

    d = {"col1": [1, 2], "col2": [3, 4]}
    df = pd.DataFrame(data=d)

    print(format_table(df))
