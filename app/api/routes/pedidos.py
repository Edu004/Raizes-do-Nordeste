
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infraestructure.database import get_db
from domain.models import Pedido
from schemas import PedidoCreate, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

# mapa de transições permitidas — o "pulo do gato" da máquina de estados
TRANSICOES_PERMITIDAS = {
    "SOLICITADO": ["APROVADO", "RECUSADO"],
    "APROVADO": ["CONCLUIDO"],
    "RECUSADO": ["DELETADO"]
}

@router.post("/", status_code=201)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    novo = Pedido(pedido_id= dados.id , unidade_id = dados.unidade_id , canalpedido=dados.canalpedido)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"id": novo.id, "status": novo.status}




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




