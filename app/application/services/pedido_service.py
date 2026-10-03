
from sqlalchemy.orm import Session
from app.domain.models import Pedido


TRANSICOES_PERMITIDAS = {
    "PENDENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["EM_PREPARACAO", "CANCELADO"],
    "EM_PREPARACAO": ["PRONTO"],
    "PRONTO": ["ENTREGUE"],
    "ENTREGUE": [],
    "CANCELADO": []
}


def criar_pedido(
    db: Session,
    unidade_id: int,
    cliente_id: int,
    canal_pedido: str,
    total: float
):
    
    if unidade_id != 0:
        pass
    else:
        return "Unidade indisponível"
        #como validar a unidade?
        
    novo = Pedido(pedido_id= dados.id , unidade_id = dados.unidade_id , canalpedido=dados.canal_pedido)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"id": novo.id, "status": novo.status}
    
    #qual usar?
    novo_pedido = Pedido(
        unidade_id=unidade_id,
        cliente_id=cliente_id,
        canal_pedido=canal_pedido,
        status="PENDENTE",
        total=total
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido





