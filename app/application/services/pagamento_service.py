
from sqlalchemy.orm import Session

from domain.models import Pagamento, Pedido


def processar_pagamento(
    db: Session,
    pedido_id: int,
    valor: float
):
    pedido = (
        db.query(Pedido)
        .filter(Pedido.id == pedido_id)
        .first()
    )

    if not pedido:
        return None, "Pedido não encontrado"

    # MOCK DE PAGAMENTO
    pagamento_aprovado = valor == float(pedido.total)

    if pagamento_aprovado:
        status = "APROVADO"
    else:
        status = "RECUSADO"

    pagamento = Pagamento(
        pedido_id=pedido_id,
        status_pag=status,
        valor=valor
    )

    db.add(pagamento)

    if status == "APROVADO":
        pedido.status = "CONFIRMADO"

    db.commit()
    db.refresh(pagamento)

    return pagamento, None






