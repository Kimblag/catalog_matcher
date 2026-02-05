from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    VECTOR_DIMENSION: int
    VECTOR_FILE_PATH: str
    REPOSITORY_FILE_PATH: str
    MAX_DISTANCE: float
    TEMPLATE_CATALOG: str
    TEMPLATE_REQUIREMENT: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
        )

settings = Settings()