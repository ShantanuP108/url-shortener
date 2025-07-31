from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "Shantanu@6"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "url_shortener_db"

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
