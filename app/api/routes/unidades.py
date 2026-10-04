from fastapi import APIRouter, Depends , HTTPException
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


@router.get("/{unidade_id}")
def consultar_unidade_id(unidade_id: int, db: Session = Depends(get_db)):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    return unidade

@router.put("/{unidade_id}")
def atualizar_unidade(unidade_id: int, dados: UnidadeBase, db: Session = Depends(get_db)):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    for key, value in dados.model_dump().items():
        setattr(unidade, key, value)
    db.commit()
    db.refresh(unidade)
    return unidade





