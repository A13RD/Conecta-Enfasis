from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://neondb_owner:npg_E5O6dRcxFyBh@ep-polished-rain-ad0whm21-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    PGHOST: str = 'ep-polished-rain-ad0whm21-pooler.c-2.us-east-1.aws.neon.tech'
    PGDATABASE: str = 'neondb'
    PGUSER: str = 'neondb_owner'
    PGPASSWORD: str = 'npg_E5O6dRcxFyBh'
    PGSSLMODE: str = 'require'
    

    SECRET_KEY: str = "jb851EjcJ6a1WoGtmh6HcxLWkKWDrpRTMXoBu27-Ojk="
    ALGORITHM: str = "HS256"

    class Config:
        """Configuración para leer variables de entorno (opcional)"""
        env_file = ".env" 

settings = Settings()