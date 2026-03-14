from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Mini ERP Inteligente API"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/mini_erp"
    frontend_url: str = "http://localhost:5173"
    google_client_id: str = ""
    secret_key: str = "change-me"
    gcp_project_id: str = ""
    gcp_secret_name: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
