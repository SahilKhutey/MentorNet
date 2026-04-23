from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MentorNet AI"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./mentornet.db"

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: str) -> str:
        if isinstance(v, str) and v:
            return v
        return "sqlite:///./mentornet.db"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"

    # Vector DB
    FAISS_INDEX_PATH: str = "./data/faiss_index.bin"

    # Security Configuration
    SECRET_KEY: str = "DEV_SECRET_KEY_REPLACE_IN_PROD" # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
