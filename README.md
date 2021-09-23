# DB Explorer

A bootstrapped command-line tool for exploring and working with a database from the command-line. 
Useful when interacting with a DB on a project without CLI tooling offered by its framework.

## Features
- **[SQLAlchemy:](https://www.sqlalchemy.org/)** Powered by providing a SQLAlchemy engine.
- **[Typer:](https://typer.tiangolo.com/)** Powered by the Typer library allowing for simple command definition.
  - **[Click:](https://click.palletsprojects.com/en/8.0.x/)** Typer is powered by the Click library which can be leveraged for additional CLI functionality.

_This project is not ready, but its public because I need it 😉_

## Getting Started
### Install
```bash
$ pip install -r requirements.txt
```
### Settings
There are multiple options for settings
1. Edit the `settings.py` file
2. Create a `.env` file (recommended). 
3. Create environment variables.

## Custom Commands
To define your own commands, create a file in the `commands/` dir. Each file must have `app = typer.Typer()` 
which will be picked up as a sub command. 
- Sub-command name: Taken from file name.
- Sub-command help text: Taken from the file's doc string.
- Sub-command available commands: Commands registered to the `app`.

## Use
- Your best bet is (after installing) to run `python main.py`
- See `commands/example.py` for an example of a custom command.