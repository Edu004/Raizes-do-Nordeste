from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.application.services import pedido_service
from app.domain.models import Pedido
from app.schemas import PedidoBase, PedidoUpdate , PedidoOut #pedidoupdate não foi usado?


router = APIRouter(prefix="/pedidos", tags=["pedidos"])

# mapa de transições permitidas em conformidade com enums
TRANSICOES_PERMITIDAS = {

    "PENDENTE","CONFIRMADO","EM_PREPARACAO","PRONTO","ENTREGUE","CANCELADO"
}

@router.post("/", status_code=201)
def criar_pedido(pedido:PedidoBase,db: Session = Depends(get_db) , ):
    return pedido_service.criar_pedido(db: Session,unidade_id= pedido.unidade_id,cliente_id=pedido.cliente_id,canal_pedido=pedido.canal_pedido ,total=pedido.total)
    


@router.get("/pedidos",
    response_model=List[PedidoOut],
    summary="Listar pedidos",
    tags=["pedidos"]
)
#criar função de listar e jogar ela para o service
def listar_pedidos():
    return pedido_service.listar_pedidos()


@router.patch("/{pedido_id}/status")
#passar para service
def atualizar_status(pedido_id: int, novo_status: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    permitidos = TRANSICOES_PERMITIDAS.get(pedido.status, [])#mudar a lógica e nao usar .get
    if novo_status not in permitidos:
        raise HTTPException(
            status_code=409,
            detail=f"Transição de {pedido.status} para {novo_status} não permitida",
        )

    pedido.status = novo_status
    db.commit()
    return {"id": pedido.id, "status": pedido.status}



