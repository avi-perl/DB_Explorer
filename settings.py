from pydantic import BaseSettings


class Settings(BaseSettings):
    db_type: str = None
    db_user: str = None
    db_password: str = None
    db_host: str = "localhost"
    default_db: str = None

    tabulate_headers: str = "keys"
    tabulate_tablefmt: str = "github"

    user_defined_commands_dir_name: str = "commands"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
