


# crud.py
# Funções de acesso ao banco para o recurso Corrida

from sqlalchemy.orm import Session
from domain.models import Estoque, Produto, Unidade, Pedido, Cliente, Pagamento
from schemas import  PedidoCreate, PedidoUpdate 
from schemas import ClienteCreate, ClienteUpdate
from schemas import EstoqueCreate, EstoqueUpdate
from infraestructure import security
import time
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


def criar_cliente(db: Session, payload: ClienteCreate):
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


def criar_pedido(db: Session, payload: PedidoCreate):
    """
    Cria nova pedido a partir do payload validado.
    """
    pedido = pedido(**payload.dict())
    db.add(pedido)#adicionar
    db.commit()#salvar no bd
    db.refresh(pedido)#atualizar banco de dados
    return pedido#retornar atualizado


def processar_pagamento(db: Session, pedido_id: int, valor_pago: float):
    """
    Processa pagamento de um pedido com lógica de retry em caso de recusa.
    
    Retorna:
        dict: {
            'sucesso': bool,
            'mensagem': str,
            'pagamento': Pagamento object or None,
            'tentativas': int
        }
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        logger.warning(f"Pedido {pedido_id} não encontrado")
        return {
            'sucesso': False,
            'mensagem': 'Pedido não encontrado',
            'pagamento': None,
            'tentativas': 0
        }
    
    # Verificar se pedido já foi pago
    if pedido.status == StatusPagamento.PAGO.value:
        logger.info(f"Pedido {pedido_id} já foi pago")
        return {
            'sucesso': True,
            'mensagem': 'Pedido já foi pago',
            'pagamento': None,
            'tentativas': 0
        }
    
    # Tentar processar pagamento com retry
    resultado = _processar_pagamento_com_retry(db, pedido, valor_pago)
    return resultado


def _processar_pagamento_com_retry(
    db: Session, 
    pedido: Pedido, 
    valor_pago: float,
    tentativa_atual: int = 1
) -> Dict:
    """
    Processa pagamento com retry automático em caso de recusa.
    
    Args:
        db: Sessão do banco de dados
        pedido: Objeto Pedido
        valor_pago: Valor a ser pago
        tentativa_atual: Número da tentativa atual
    
    Returns:
        dict com resultado do processamento
    """
    logger.info(f"Tentativa {tentativa_atual}/{ConfigRetry.MAX_TENTATIVAS} - Processando pagamento para pedido {pedido.id}")
    
    # Simular processamento de pagamento (aqui você integraria com gateway)
    resultado_pagamento = _simular_processamento_gateway(valor_pago)
    
    if resultado_pagamento['sucesso']:
        # Pagamento aprovado
        logger.info(f"Pagamento aprovado para pedido {pedido.id}")
        
        # Criar registro de pagamento
        pagamento = Pagamento(
            pedido_id=pedido.id,
            status_pag=StatusPagamento.PAGO.value,
            valor=valor_pago
        )
        db.add(pagamento)
        
        # Atualizar status do pedido
        pedido.status = StatusPagamento.PAGO.value
        db.commit()
        db.refresh(pedido)
        
        return {
            'sucesso': True,
            'mensagem': f'Pagamento processado com sucesso na tentativa {tentativa_atual}',
            'pagamento': pagamento,
            'tentativas': tentativa_atual
        }
    
    elif resultado_pagamento['motivo'] == 'recusado':
        # Pagamento recusado - tentar novamente
        logger.warning(f"Pagamento recusado para pedido {pedido.id} - Motivo: {resultado_pagamento.get('detalhes', 'Desconhecido')}")
        
        if tentativa_atual < ConfigRetry.MAX_TENTATIVAS:
            # Calcular delay com backoff progressivo
            delay = ConfigRetry.DELAY_ENTRE_TENTATIVAS
            if ConfigRetry.DELAY_PROGRESSIVO:
                delay = delay * tentativa_atual  # Aumenta a cada tentativa: 2s, 4s, 6s
            
            logger.info(f"Aguardando {delay}s antes da próxima tentativa...")
            time.sleep(delay)
            
            # Tentar novamente recursivamente
            return _processar_pagamento_com_retry(
                db, 
                pedido, 
                valor_pago, 
                tentativa_atual + 1
            )
        else:
            # Máximo de tentativas atingido
            logger.error(f"Máximo de tentativas atingido para pedido {pedido.id}")
            
            # Registrar pagamento como recusado
            pagamento = Pagamento(
                pedido_id=pedido.id,
                status_pag=StatusPagamento.RECUSADO.value,
                valor=valor_pago
            )
            db.add(pagamento)
            
            # Atualizar status do pedido para recusado
            pedido.status = StatusPagamento.RECUSADO.value
            db.commit()
            db.refresh(pedido)
            
            return {
                'sucesso': False,
                'mensagem': f'Pagamento recusado após {tentativa_atual} tentativas. Motivo: {resultado_pagamento.get("detalhes", "Desconhecido")}',
                'pagamento': pagamento,
                'tentativas': tentativa_atual,
                'motivo': 'recusado'
            }
    
    else:
        # Erro temporário (timeout, conexão, etc)
        logger.warning(f"Erro temporário ao processar pagamento - Motivo: {resultado_pagamento.get('detalhes', 'Desconhecido')}")
        
        if tentativa_atual < ConfigRetry.MAX_TENTATIVAS:
            delay = ConfigRetry.DELAY_ENTRE_TENTATIVAS
            if ConfigRetry.DELAY_PROGRESSIVO:
                delay = delay * tentativa_atual
            
            logger.info(f"Aguardando {delay}s antes de retentativa...")
            time.sleep(delay)
            
            return _processar_pagamento_com_retry(
                db, 
                pedido, 
                valor_pago, 
                tentativa_atual + 1
            )
        else:
            logger.error(f"Erro ao processar pagamento após {tentativa_atual} tentativas")
            
            pagamento = Pagamento(
                pedido_id=pedido.id,
                status_pag=StatusPagamento.FALHA_TEMPORARIA.value,
                valor=valor_pago
            )
            db.add(pagamento)
            pedido.status = StatusPagamento.FALHA_TEMPORARIA.value
            db.commit()
            db.refresh(pedido)
            
            return {
                'sucesso': False,
                'mensagem': f'Erro ao processar pagamento após {tentativa_atual} tentativas. {resultado_pagamento.get("detalhes", "")}',
                'pagamento': pagamento,
                'tentativas': tentativa_atual,
                'motivo': 'erro_temporario'
            }


def _simular_processamento_gateway(valor: float) -> Dict:
    """
    Simula integração com gateway de pagamento.
    Você deve substituir isso com a integração real (Stripe, PayPal, etc).
    
    Returns:
        dict: {'sucesso': bool, 'motivo': str, 'detalhes': str}
    """
    import random
    
    # Simulação: 70% de chance de sucesso, 20% recusado, 10% erro temporário
    resultado_aleatorio = random.random()
    
    if resultado_aleatorio < 0.7:
        return {
            'sucesso': True,
            'motivo': 'aprovado',
            'detalhes': 'Transação aprovada'
        }
    elif resultado_aleatorio < 0.9:
        return {
            'sucesso': False,
            'motivo': 'recusado',
            'detalhes': 'Saldo insuficiente ou limite excedido'
        }
    else:
        return {
            'sucesso': False,
            'motivo': 'erro_temporario',
            'detalhes': 'Timeout na comunicação com gateway de pagamento'
        }


def retentar_pagamento_recusado(db: Session, pedido_id: int, valor_pago: float):
    """
    Retenta pagamento de um pedido que foi recusado anteriormente.
    Útil para permitir que o cliente tente novamente após corrigir os dados.
    
    Returns:
        dict: resultado do processamento de pagamento
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        logger.error(f"Pedido {pedido_id} não encontrado")
        return {
            'sucesso': False,
            'mensagem': 'Pedido não encontrado',
            'tentativas': 0
        }
    
    if pedido.status == StatusPagamento.PAGO.value:
        logger.info(f"Pedido {pedido_id} já foi pago")
        return {
            'sucesso': True,
            'mensagem': 'Pedido já foi pago',
            'tentativas': 0
        }
    
    if pedido.status not in [StatusPagamento.RECUSADO.value, StatusPagamento.FALHA_TEMPORARIA.value]:
        logger.warning(f"Pedido {pedido_id} não está em estado recusado ou com falha")
        return {
            'sucesso': False,
            'mensagem': f'Pedido está com status {pedido.status}. Apenas pedidos recusados podem ser retentados.',
            'tentativas': 0
        }
    
    logger.info(f"Retentando pagamento para pedido {pedido_id}")
    
    # Resetar status para processando antes de tentar
    pedido.status = StatusPagamento.PROCESSANDO.value
    db.commit()
    
    # Tentar processar novamente
    resultado = _processar_pagamento_com_retry(db, pedido, valor_pago, tentativa_atual=1)
    
    logger.info(f"Resultado da retentativa para pedido {pedido_id}: {resultado['mensagem']}")
    return resultado


def obter_historico_tentativas_pagamento(db: Session, pedido_id: int):
    """
    Obtém o histórico de tentativas de pagamento de um pedido.
    
    Returns:
        list: lista de pagamentos associados ao pedido
    """
    pagamentos = db.query(Pagamento).filter(Pagamento.pedido_id == pedido_id).all()
    return pagamentos


def obter_status_pedido(db: Session, pedido_id: int) -> Dict:
    """
    Obtém o status atual do pedido com informações de pagamento.
    
    Returns:
        dict: informações do pedido e pagamento
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        return {'erro': 'Pedido não encontrado'}
    
    pagamentos = db.query(Pagamento).filter(Pagamento.pedido_id == pedido_id).all()
    
    return {
        'pedido_id': pedido.id,
        'status': pedido.status,
        'total': pedido.total,
        'quantidade_tentativas': len(pagamentos),
        'ultimo_status_pagamento': pagamentos[-1].status_pag if pagamentos else 'Nenhuma tentativa',
        'pagamentos': [
            {
                'id': p.id,
                'status': p.status_pag,
                'valor': p.valor
            } for p in pagamentos
        ]
    }



def consultar_pedido_por_id(db: Session, pedido:Pedido, pedido_id: int):
    """
    Busca pedido por ID.
    """
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()


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

