from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configurações gerais
    SUMMARY: str = "Microservice to maintain withdrawal and deposit operations from current accounts."
    APP_NAME: str = "DIO bank API"
    APP_VERSION: str = "1.2.0"
    DEBUG: bool = True
    ISS: str = "desafio-bank.com.br"
    AUD: str = "desafio-bank"

    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./bank.db"
    ENVIRONMENT: str | None = None

    # Configurações de segurança
    SECRET_KEY: str = "default-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SCHEME: str = "Bearer"

    # model_config = SettingsConfigDict(
    #     env_file=".env", extra="ignore", env_file_encoding="utf-8"
    # )
    class Config:
        env_file = ".env"  # Carregar variáveis de ambiente de um arquivo .env


# Instância global das configurações
settings = Settings()
