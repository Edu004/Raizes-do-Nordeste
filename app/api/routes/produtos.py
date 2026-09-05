from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infraestructure.database import get_db
from domain.models import Produto
from schemas import ProdutoCreate


router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)


@router.post("/", status_code=201)
def criar_produto(
    dados: ProdutoCreate,
    db: Session = Depends(get_db)
):
    novo = Produto(**dados.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "id": novo.id,
        "nome": novo.nome,
        "categoria": novo.categoria
    }