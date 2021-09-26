from sqlalchemy import create_engine
from sqlalchemy.future import Engine

from settings import settings as config

type = config.db_type
user = config.db_user
password = config.db_password
host = config.db_host
default_db = config.default_db


def get_engine() -> Engine:
    return create_engine(f"{type}://{user}:{password}@{host}/{default_db}")


if __name__ == "__main__":
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute("SELECT NOW()")
        for row in result:
            print(row)
