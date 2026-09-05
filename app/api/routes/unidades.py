from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infraestructure.database import get_db
from domain.models import Unidade
from schemas import UnidadeCreate, UnidadeUpdate


router = APIRouter(
    prefix="/unidades",
    tags=["unidades"]
)


@router.post("/", status_code=201)
def criar_unidade(
    dados: UnidadeCreate,
    db: Session = Depends(get_db)
):
    nova = Unidade(**dados.model_dump())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return {
        "id": nova.id,
        "nome": nova.nome,
        "cidade": nova.cidade
    }

