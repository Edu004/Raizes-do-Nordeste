
from sqlalchemy.orm import Session
from app.domain.models import Pagamento, Pedido, ItemPedido ,Estoque



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
        itens_do_pedido = db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido_id).all()
        for item in itens_do_pedido:
            estoque = db.query(Estoque).filter(
            Estoque.produto_id == item.produto_id,
            Estoque.unidade_id == pedido.unidade_id
        ).first()
        if estoque:
            estoque.quantidade -= item.quantidade

    db.commit()
    db.refresh(pagamento)
    return pagamento, None

            #buscar itens de cada pedido no estoque





