

from contextlib import closing
from pathlib import Path


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

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


Base = declarative_base()

# Dependência de sessão para FastAPI (garante abertura e fechamento)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/estoque", tags=["Estoque"])



class ProdutoEstoque(BaseModel):
	nome: str = Field(min_length=1)
	unidade: str = Field(default="un")
	quantidade: float = Field(gt=0)
	id: int = Field(ge=0)


class ItemVenda(BaseModel):
	produto_id: int
	quantidade: float = Field(gt=0)


class VendaEntrada(BaseModel):
	itens: list[ItemVenda] = Field(min_length=1)
	produtos: list[ProdutoEstoque] = Field(min_length=1)
	quantidade: float = Field(gt=0)



@router.get("/unidades/{unidade_id}/cardapio", response_model=list[ProdutoEstoque])
def consultar_estoque(unidade_id: int):
      
	"""
	Consulta o estoque de uma unidade específica.
	"""
	with closing(SessionLocal()) as db:
		# Consulta os produtos no estoque da unidade
		produtos_estoque = db.query(ProdutoEstoque).filter(ProdutoEstoque.unidade_id == unidade_id).all()
		if not produtos_estoque:
			raise HTTPException(status_code=404, detail="Estoque não encontrado para a unidade especificada")
		return produtos_estoque


#terminar tudo!


