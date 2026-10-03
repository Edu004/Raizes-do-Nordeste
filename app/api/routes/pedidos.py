from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.domain.models import Pedido
from app.schemas import PedidoBase, PedidoUpdate , PedidoOut #pedidoupdate não foi usado?


router = APIRouter(prefix="/pedidos", tags=["pedidos"])

# mapa de transições permitidas em conformidade com enums
TRANSICOES_PERMITIDAS = {

    PENDENTE = "PENDENTE",
    CONFIRMADO = "CONFIRMADO",
    EM_PREPARACAO = "EM_PREPARACAO",
    PRONTO = "PRONTO",
    ENTREGUE = "ENTREGUE",
    CANCELADO = "CANCELADO"
}

@router.post("/", status_code=201)
def criar_pedido(dados: PedidoBase, db: Session = Depends(get_db)):
    return pedido_service(criar_pedido(dados=PedidoBase, db:Session = Depends(get_db)))
    novo = Pedido(pedido_id= dados.id , unidade_id = dados.unidade_id , canalpedido=dados.canal_pedido)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"id": novo.id, "status": novo.status}


@router.get("/pedidos",
    response_model=List[PedidoOut],
    summary="Listar pedidos",
    tags=["pedidos"]
)
#criar função de listar e jogar ela para o service



@router.patch("/{pedido_id}/status")
def atualizar_status(pedido_id: int, novo_status: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    permitidos = TRANSICOES_PERMITIDAS.get(pedido.status, [])
    if novo_status not in permitidos:
        raise HTTPException(
            status_code=409,
            detail=f"Transição de {pedido.status} para {novo_status} não permitida",
        )

    pedido.status = novo_status
    db.commit()
    return {"id": pedido.id, "status": pedido.status}



