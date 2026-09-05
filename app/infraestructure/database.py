


# database.py
# Configuração do banco de dados SQLite e sessão do SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



# String de conexão SQLite (arquivo local estoque.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./estoque.db"

# Engine com check_same_thread=False para uso com FastAPI/async (threading)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal será injetada nos endpoints para transações com o BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()

# Dependência de sessão para FastAPI (garante abertura e fechamento)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





#terminar tudo!


