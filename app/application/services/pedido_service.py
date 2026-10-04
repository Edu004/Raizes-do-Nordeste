


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.models import Pedido,ProdutoUnidade,ItemPedido,Unidade,Estoque
from app.domain import enums
#from app.schemas import ProdutoUnidadeBase nao estao sendo usados
#from app.schemas import ItemPedidoBase,ItemPedidoUpdate


# mapa de transições permitidas em conformidade com enums
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
    #total: float, testar rodar sem ele
    itens:list
):
    #verificar unidade
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
        # existe na unidade?
    
    elif canal_pedido not in [c.value for c in enums.CanalPedido]:
        raise HTTPException(status_code=422, detail="Canal de pedido inválido")
    #passando pela validação de canal e depois ir pelos itens
    total = 0
    #criar pedido
    novo_pedido = Pedido(
    unidade_id=unidade_id,
    cliente_id=cliente_id,
    canal_pedido=canal_pedido,
    status="PENDENTE",
    total=total
    )   
    db.add(novo_pedido)
    db.flush()

    for item in itens:
        #para cada item:
        #verificar produto
        #verificar disponibilidade
        produto_unidade = db.query(ProdutoUnidade).filter(
            ProdutoUnidade.produto_id == item.produto_id,
            ProdutoUnidade.unidade_id == unidade_id
        ).first()
        #se não estiver disponivel na unidade selecionada
        if not produto_unidade:
            raise HTTPException(
            status_code=404,
            detail=f"Produto {item.produto_id} não disponível nessa unidade"
        )
        #verificar estoque
        estoque = db.query(Estoque).filter(
        Estoque.produto_id == item.produto_id,
        Estoque.unidade_id == unidade_id
        ).first()
        if not estoque or estoque.quantidade < item.quantidade:
            raise HTTPException(
            status_code=409,
            detail=f"Estoque insuficiente para o produto {item.produto_id}"
        )#existindo produto e estoque necessário,criar novo item
        
        novo_item = ItemPedido(
                    pedido_id=novo_pedido.id,
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                    valor_unitario=produto_unidade.preco  # o preço do banco, de novo
                    )
        
        db.add(novo_item)
        total += produto_unidade.preco * item.quantidade
        
        #validar preço do pedido antes de criar ele
        #calcular total
        #diminuir do estoque e mostrar o que foi pago,ir para o pagamento_service nessa parte*
    
      # gera o id do pedido, mas não fecha a transação ainda para que ela termine de ser validada no commit depois
    db.refresh(novo_pedido)
    db.commit()
    return novo_pedido
#
    #se aprovado e gerado: aí daqui em diante é no pagamento_service
    #    atualizar estoque
    #salvar alterações

    #solicitar pagamento
    #analisar resultado
    #atualizar status
    
    


def listar_pedidos(
    db: Session
):
    pedidos = db.query(Pedido).all()
    return pedidos

def atualizar_status(db: Session,
    id: int,
    novo_status: str):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    permitidos = TRANSICOES_PERMITIDAS.get(pedido.status, [])#dicionario validado conforme as transações que um pedido tem
    if novo_status not in permitidos:
        raise HTTPException(
            status_code=409,
            detail=f"Transição de {pedido.status} para {novo_status} não permitida",
        )

    pedido.status = novo_status
    db.commit()
    return {"id": pedido.id, "status": pedido.status}




