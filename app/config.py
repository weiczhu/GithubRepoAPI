from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost/githubapidb"
    tablename: str = "githubrepo"
    github_api_base_url: str = "https://api.github.com/repos"
    github_api_timeout: float = 2.0  # in seconds

    class Config:
        env_file = ".env"


settings = Settings()
