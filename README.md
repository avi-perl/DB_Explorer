# DB Explorer

A command-line tool for exploring a database from the command-line.

**This project is not ready, but its public because I need it 😉**

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

## Use
### SELECT command 
```
Usage: main.py select [OPTIONS] TABLE

Arguments:
  TABLE  [required]

Options:
  --columns TEXT
  --comma-columns TEXT
  --where TEXT
  --help                Show this message and exit.
```
#### Use Case
```bash
$ python main.py select some_table --columns "some_col" --columns "additional_col" --comma-columns "these,also,work" --where "some_col = 'value'"
```
### OPERATION command 
```
Usage: main.py operation [OPTIONS] NAME VAR

Arguments:
  NAME  [required]
  VAR   [required]

Options:
  --help  Show this message and exit.
```
#### Instructions
- Create a function inside of the`operations.py` file that accepts a single variable (VAR).
- This function may optionally return a string that will be printed. 
#### Use Case
```bash
$ python main.py operation table_with_column id
```