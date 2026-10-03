from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infraestructure.database import get_db
from app.domain.models import Produto
from app.schemas import ProdutoBase

#rota dos produtos
router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)


@router.post("/", status_code=201)
def criar_produto(
    dados: ProdutoBase,
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




@router.get("/",status_code=201)
def listar_produtos(
    db: Session = Depends(get_db)
):
    produtos = db.query(Produto).all()
    return produtos

@router.get("/{produto_id}",status_code=201)
def consultar_produto_id(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto 


@router.put("/{produto_id}", status_code=200)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoBase,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for key, value in dados.model_dump().items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)

    return {
        "id": produto.id,
        "nome": produto.nome,
        "categoria": produto.categoria
    }

@router.delete("/{produto_id}", status_code=204)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()

    return {"detail": "Produto deletado com sucesso"}


