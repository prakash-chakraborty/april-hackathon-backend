from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    pghost: str
    pgport: int
    pguser: str
    pgpassword: str
    pgdatabase: str
    jwt_secret: str

    @property
    def database_url(self):
        return (
            f"postgresql://{self.pguser}:{self.pgpassword}"
            f"@{self.pghost}:{self.pgport}/{self.pgdatabase}"
            f"?sslmode=require"
        )


settings = Settings()
