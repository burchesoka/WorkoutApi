from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int

    db_user: str
    db_name: str
    db_host: str
    db_pass: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
