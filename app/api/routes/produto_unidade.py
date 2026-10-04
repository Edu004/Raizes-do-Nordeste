#integração de produtos para suas devidas unidades

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.domain.models import ProdutoUnidade
from app.schemas import ProdutoUnidadeBase

router = APIRouter(prefix="/produto-unidade", tags=["ProdutoUnidade"])

#resolvendo erro de produto não disponivel para unidade
@router.post("/", status_code=201)
def vincular_produto_unidade(dados: ProdutoUnidadeBase, db: Session = Depends(get_db)):
    novo = ProdutoUnidade(**dados.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo






