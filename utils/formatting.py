from tabulate import tabulate
from pandas import DataFrame

from settings import settings as conf


def format_table(df: DataFrame) -> str:
    return tabulate(df, headers=conf.tabulate_headers, tablefmt=conf.tabulate_tablefmt)


if __name__ == '__main__':
    import pandas as pd
    
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    
    print(format_table(df))
