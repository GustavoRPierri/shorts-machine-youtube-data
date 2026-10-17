from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///local.db"
# DATABASE_URL = "mysql+pymysql://user:senha@host:3306/meubanco"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)