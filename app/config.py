from pydantic.settings import BaseSettings, SettingsConfigDict

class PostgresSettings(BaseSettings):
    model_config = SettingConfigDict(env_prefix="PSQL_DB_")

    database: str
    username: str
    password: str
    host: str
    port: str

postgres_settings = PostgresSettings()

DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
    postgres_settings.username,
    postgres_settings.password,
    postgres_settings.host,
    postgres_settings.port,
    postgres_settings.database,
)

models = ["app.authentication.models","app.files.models","aerich.models"]


class MinioSettings(BaseSettings):
    model_config = SettingConfigDict(env_prefix="MINIO_")

    root_user: str
    root_password: str
    host: str
    port: str
    backet_name: str

minio_settings = MinioSettings()