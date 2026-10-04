

from http.client import HTTPException

from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.domain.models import Pedido,ProdutoUnidade,ItemPedido
from app.domain import enums
from app.schemas import ProdutoUnidadeBase
from app.schemas import ItemPedidoBase,ItemPedidoUpdate


# mapa de transições permitidas em conformidade com enums
TRANSICOES_PERMITIDAS = {
    "PENDENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["EM_PREPARACAO", "CANCELADO"],
    "EM_PREPARACAO": ["PRONTO", "CANCELADO"],
    "PRONTO": ["ENTREGUE", "CANCELADO"],
    "ENTREGUE": ["CONCLUIDO", "CANCELADO"],
    "CANCELADO": []

}


def criar_pedido(
    db: Session,
    unidade_id: int,
    cliente_id: int,
    canal_pedido: str,
    total: float,
    itens:list
):
    #verificar unidade
#
    if unidade_id != 0:
        pass
    else:
        return "Unidade indisponível"
        #como validar a unidade?

    #para cada item:
    #    verificar produto
    #    verificar disponibilidade
    #    verificar estoque

    #validar preço do pedido antes de criar ele
    if canal_pedido not in [c.value for c in enums.CanalPedido]:
        return "Canal de pedido inválido"
    #passando pela validação de canal começar o valor
    total = 0
    for item in itens:
        #diminuir do estoque e mostrar o que foi pago
        produto_unidade = db.query(ProdutoUnidade).filter(
            ProdutoUnidade.produto_id == item.produto_id,
            ProdutoUnidade.unidade_id == unidade_id
        ).first()
        total += produto_unidade.preco * item.quantidade
        #calcular total
    
    #criar pedido
    
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

    #criar itens, como fazer?
    #solicitar pagamento

    #analisar resultado
    #atualizar status
#
    #se aprovado: aí daqui em diante é no pagamento_service
    #    atualizar estoque
    #salvar alterações
    #retornar pedido    
    
    return novo_pedido


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

    permitidos = TRANSICOES_PERMITIDAS.get(pedido.status, [])#mudar a lógica e nao usar .get
    if novo_status not in permitidos:
        raise HTTPException(
            status_code=409,
            detail=f"Transição de {pedido.status} para {novo_status} não permitida",
        )

    pedido.status = novo_status
    db.commit()
    return {"id": pedido.id, "status": pedido.status}




