from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infraestructure.database import get_db
from app.domain.models import Unidade
from app.schemas import UnidadeBase, UnidadeUpdate


router = APIRouter(
    prefix="/unidades",
    tags=["unidades"]
)


@router.post("/", status_code=201)
def criar_unidade(
    dados: UnidadeBase,
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

@router.get("/")
def listar_unidades(
    db: Session = Depends(get_db)
):
    unidades = db.query(Unidade).all()
    return unidades







