from typing import List
import typer
from utils.db_explore import DBSelect, DBOperation

app = typer.Typer()


@app.command()
def select(
        table: str,
        columns: List[str] = typer.Option([]),
        comma_columns: str = None,
        where: str = "",
):
    col = comma_columns.split(",") if comma_columns else []
    col = col + list(columns)

    db_explore = DBSelect(
        table_name=table,
        columns=set(col),
        where=where,
    )
    output = db_explore.get_output()

    typer.echo(output)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def operation(name: str, var: str):
    db_operation = DBOperation(name, var)
    typer.echo(db_operation.get_output())


if __name__ == "__main__":
    app()
