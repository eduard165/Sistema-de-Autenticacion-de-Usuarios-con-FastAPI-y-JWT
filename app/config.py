import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    
    PROJECT_NAME: str = "FastAPI MongoDB Users"
    PROJECT_VERSION: str = "1.0.0"
    
    # Configuraciones de MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/user_database/users")
    
    # Configuraciones de JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Instancia de configuración
settings = Settings()
