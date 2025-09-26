from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

Base=declarative_base()

class Settings(BaseSettings):
    DB_HOST:str=''
    DB_PORT:str=''
    DB_PASSWORD:str=''
    DB_USER:str=''
    DATABASE:str=''
    DEBUG:bool=False

    ALLOWED_ORIGINS:str=''
    
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls,v:str) -> List[str]:
        return v.split(',') if v else []
    
    class Config:
        env_file=".env"
        env_file_encoding="utf-8"
        case_sensitive=True
        
settings=Settings()

# engine=create_engine(f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD.replace('@','%40')}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DATABASE}")
db_url=f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD.replace('@','%40')}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DATABASE}"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally :
        db.close()
        
def get_raw_db():
    db=engine.raw_connection()
    try:
        yield db
    finally:
        db.close()
        
def create_table():
    Base.metadata.create_all(bind=engine)