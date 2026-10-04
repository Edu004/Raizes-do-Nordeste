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
    return pedido_service.criar_pedido(db=db,unidade_id= pedido.unidade_id,cliente_id=pedido.cliente_id,canal_pedido=pedido.canal_pedido ,total=pedido.total)
    


@router.get("/pedidos",
    response_model=List[PedidoOut],
    summary="Listar pedidos",
    tags=["pedidos"]
)
#criar função de listar e jogar ela para o service
def listar_pedidos(pedido:PedidoBase,db:Session = Depends(get_db)):
    return pedido_service.listar_pedidos(pedido=pedido,db=db)


@router.patch("/{pedido_id}/status")
#passar para service
def atualizar_status(id: int, novo_status: str, db: Session = Depends(get_db)):
    return pedido_service.atualizar_status(db=db,id=id,novo_status= novo_status)



