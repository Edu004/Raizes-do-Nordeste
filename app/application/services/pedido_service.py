
from sqlalchemy.orm import Session
from app.domain.models import Pedido
from app.domain import enums

TRANSICOES_PERMITIDAS = {

    "PENDENTE","CONFIRMADO","EM_PREPARACAO","PRONTO","ENTREGUE","CANCELADO"
}

def criar_pedido(
    db: Session,
    unidade_id: int,
    cliente_id: int,
    canal_pedido: str,
    total: float
):
    #validar preço do pedido antes de criar ele
    if canal_pedido not in enums.CanalPedido.__members__:
        return "Canal de pedido inválido"
    #passando pela validação de canal começar o valor
    total = 0
    #diminuir do estoque e mostrar o que foi pago


    if unidade_id != 0:
        pass
    else:
        return "Unidade indisponível"
        #como validar a unidade?
    

    #verificar unidade
#
    #para cada item:
    #    verificar produto
    #    verificar disponibilidade
    #    verificar estoque
#
    #calcular total
#
    #criar pedido
#
    #criar itens
#
    #solicitar pagamento
#
    #analisar resultado
#
    #atualizar status
#
    #se aprovado:
    #    atualizar estoque
    #salvar alterações
    #retornar pedido    
    
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


def listar_pedidos(
    db: Session
):
    pedidos = db.query(Pedido).all()
    return pedidos






