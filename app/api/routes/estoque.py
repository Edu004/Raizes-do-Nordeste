

from contextlib import closing



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infraestructure.database import get_db
from app.domain.models import Estoque
from app.schemas import EstoqueBase




router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post("/", status_code=201)
def criar_Estoque(
    dados: EstoqueBase,
    db: Session = Depends(get_db)
):
    nova = Estoque(**dados.model_dump())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return {
        "id": nova.id,
        "unidade_id": nova.unidade_id,
        "produto_id": nova.produto_id,
        "quantidade": nova.quantidade
    }


@router.get("/")
def listar_estoque(
	db: Session = Depends(get_db)
):
	estoque = db.query(Estoque).all()
	return estoque


@router.get("/unidades/{unidade_id}/cardapio", response_model=list[Estoque])
def consultar_estoque_id(unidade_id: int,db: Session = Depends(get_db)):
	estoque = db.query(Estoque).filter(Estoque.unidade_id == unidade_id).all()
	return estoque


#terminar tudo!


