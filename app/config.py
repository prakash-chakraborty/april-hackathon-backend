from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pghost: str
    pgport: int
    pguser: str
    pgpassword: str
    pgdatabase: str
    jwt_secret: str
    debug: bool = False

    class Config:
        env_file = ".env"

    @property
    def database_url(self):
        return (
            f"postgresql://{self.pguser}:{self.pgpassword}"
            f"@{self.pghost}:{self.pgport}/{self.pgdatabase}"
            f"?sslmode=require"
        )


settings = Settings()
