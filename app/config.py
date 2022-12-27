from pydantic import BaseSettings

# pega as environment variables

class Settings(BaseSettings):
    database_hostname: str 
    database_password: str 
    database_name: str  
    database_username: str 
    database_port: str
    secret_key: str 
    algorithm: str   
    access_token_expire_days: int

    class Config:
        env_file = '.env'

settings = Settings()
