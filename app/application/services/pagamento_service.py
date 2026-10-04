
from sqlalchemy.orm import Session
from app.domain.models import Pagamento, Pedido



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
    #procurar pedido
    if not pedido:
        return None, "Pedido não encontrado"

    #só validar se for igual ao valor total
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
        #logica de decrementar produtos do pedido no estoque
        
        for item in pedido.itens:
            produto_unidade = (
                db.query(Pagamento)
                .filter(
                    Pagamento.produto_id == item.produto_id,
                    Pagamento.unidade_id == pedido.unidade_id
                )
                .first()
            )
            if produto_unidade:
                produto_unidade.quantidade -= item.quantidade
                db.commit()

    
    db.refresh(pagamento)

    return pagamento, None






