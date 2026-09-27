from decouple import config
from sqlmodel import create_engine

postgres_url = config("DATABASE_URL")
engine = create_engine(postgres_url, echo=True)
