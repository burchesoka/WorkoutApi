from pydantic import BaseSettings
import logging
import logging.handlers


class Settings(BaseSettings):
    server_host: str
    server_port: int

    db_user: str
    db_name: str
    db_host: str
    db_pass: str

    jwt_secret: str = 'asd'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)


def logger_init(name):
    logger = logging.getLogger(name)
    format_ = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(format_))
    sh.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(
        filename='logs/workout_api.log',
        maxBytes=1024000,
        backupCount=10,
    )
    fh.setFormatter(logging.Formatter(format_))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('Logger was initialized')
