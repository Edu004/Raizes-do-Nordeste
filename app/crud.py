


# crud.py
# Funções de acesso ao banco para o recurso Corrida

from sqlalchemy.orm import Session
from app.domain.models import Estoque, Produto, Unidade , Pedido, Cliente, Pagamento
from schemas import  PedidoBase, PedidoUpdate 
from schemas import ClienteBase, ClienteUpdate
from schemas import EstoqueBase, EstoqueUpdate#um estoque precisa ser criado para cada produto e unidade, então o crud precisa de funções para criar e atualizar estoque
from app.infraestructure import security

import logging
from typing import Optional, Dict
from enum import Enum

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração de Retry
class ConfigRetry:
    """Configuração para retry em processamento de pagamentos"""
    MAX_TENTATIVAS = 3
    DELAY_ENTRE_TENTATIVAS = 2  # segundos
    DELAY_PROGRESSIVO = True  # aumentar delay a cada tentativa


class StatusPagamento(Enum):
    """Status possíveis de um pagamento"""
    PENDENTE = "Pendente"
    PROCESSANDO = "Processando"
    PAGO = "Pago"
    RECUSADO = "Recusado"
    FALHA_TEMPORARIA = "Falha Temporária"


def criar_cliente(db: Session, payload: ClienteBase):
    """
    Cria novo cliente a partir do payload validado.
    """
    cliente = Cliente(**payload.dict())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def autenticar_cliente(db: Session, cliente_id: int, senha: str):
    """
    Autentica cliente com base no ID e senha fornecidos.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente or not security.verificar_senha(senha, cliente.senha_hash):
        return None
    return cliente

def listar_produtos_unidade(db: Session, unidade_id: int):
    """
    Lista produtos disponíveis em uma unidade específica.
    """
    return db.query(Produto).join(Estoque).filter(Estoque.unidade_id == unidade_id).all()

def verificar_estoque(db: Session, produto_id: int, unidade_id: int):
    """
    Verifica se há estoque disponível para um produto em uma unidade específica.
    """
    estoque = db.query(Estoque).filter(
        Estoque.produto_id == produto_id,
        Estoque.unidade_id == unidade_id
    ).first()
    return estoque and estoque.quantidade > 0


def criar_pedido(db: Session, payload: PedidoBase):
    """
    Cria nova pedido a partir do payload validado.
    usar payload?rever como criar o pedido melhor e qual classe do schemas usar*

    """
    pedido = Pedido(**payload.dict())
    estoque_disponivel = verificar_estoque()
    if estoque_disponivel == True:
        
        db.add(pedido)#adicionar
        db.commit()#salvar no db
        db.refresh(pedido)#atualizar banco de dados
        return pedido#retornar atualizado
    else:
        return "Estoque não disponível!"


def consultar_pedido_por_id(db: Session, pedido:Pedido):
    #buscar por id
    pedido_id = pedido.id
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def listar_pedidos(db,Session):
    return db.query(Pedido).all()
    #ver se funciona*



def atualizar_pedido(db: Session, pedido: Pedido, payload: PedidoUpdate):
    """
    Atualiza campos fornecidos no payload (atualização parcial/total).
    
    atualizar status do pedido *
    
    """
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(pedido, field, value)
    db.commit()
    db.refresh(pedido)
    return pedido

def delete_pedido(db: Session, pedido: Pedido):
    """
    Remove pedido do banco.

    deletar produtos de dentro do estoque depois de validado o pagamento!

    """
    db.delete(pedido)
    db.commit()




#adptar tudo para o restaurante

#terminar tudo!

