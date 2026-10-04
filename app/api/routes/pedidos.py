from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.application.services import pedido_service
from app.domain.models import Pedido
from app.schemas import PedidoBase, PedidoUpdate , PedidoOut #pedidoupdate não foi usado?


router = APIRouter(prefix="/pedidos", tags=["pedidos"])



@router.post("/", status_code=201)
def criar_pedido(pedido:PedidoBase,db: Session = Depends(get_db) , ):
    return pedido_service.criar_pedido(db=db,unidade_id= pedido.unidade_id,cliente_id=pedido.cliente_id,canal_pedido=pedido.canal_pedido,itens=pedido.itens)
    


@router.get("/",
    response_model=List[PedidoOut],
    summary="Listar pedidos",
    tags=["pedidos"]
)
#criar função de listar e jogar ela para o service
def listar_pedidos(db: Session, canal_pedido: str = None):
    query = db.query(Pedido)
    if canal_pedido:
        query = query.filter(Pedido.canal_pedido == canal_pedido)
        #validando por canal_pedido
    pedidos = query.all()
    if canal_pedido and not pedidos:
        raise HTTPException(status_code=404, detail=f"Nenhum pedido encontrado para o canal {canal_pedido}")
    return pedidos


@router.patch("/{pedido_id}/status")
#passar para service
def atualizar_status(pedido_id: int, novo_status: str, db: Session = Depends(get_db)):
    return pedido_service.atualizar_status(db=db,id=pedido_id,novo_status= novo_status)




