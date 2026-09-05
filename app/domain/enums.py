#CanalPedido
#
#
##
#
#
##
#app/domain/enums.py — comece por AQUI. É o arquivo mais rápido de escrever e destrava o resto. Traduz seus 4 enums já decididos: CanalPedido (APP/TOTEM/BALCAO/PICKUP/WEB), StatusPedido (com todos os estados da sua máquina de estados), StatusPagamento (pendente/aprovado/recusado), Role/perfil (Cliente/Atendente/ Gerente/Cozinha)


from enum import Enum


class CanalPedido(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPedido(str, Enum): 
    
    PENDENTE = "PENDENTE"
    CONFIRMADO = "CONFIRMADO"
    EM_PREPARACAO = "EM_PREPARACAO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class StatusPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"


class Role(str, Enum):
    CLIENTE = "CLIENTE"
    ATENDENTE = "ATENDENTE"
    GERENTE = "GERENTE"
    COZINHA = "COZINHA"

#todas as classes até então são esboços!


#terminar tudo!

