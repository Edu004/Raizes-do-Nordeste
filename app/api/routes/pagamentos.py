from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

# ---------------------------------------------------------------------------
# EXEMPLO SIMPLES DE "BANCO" EM MEMÓRIA
# ---------------------------------------------------------------------------
# Isso é só para entender a ideia. No projeto real, a lógica de deletar ficaria
# no crud.py e a conexão com o banco no database.py.
#
# A ideia aqui é: quando o pagamento for validado, o pedido deixa de existir no
# "banco" de pedidos pendentes.
# ---------------------------------------------------------------------------
pedidos_mock = {
    1: {"id": 1, "status": "pendente"},
    2: {"id": 2, "status": "pendente"},
    3: {"id": 3, "status": "pendente"},
}


def deletar_pedido_mock(pedido_id: int) -> None:
    """Simula a função de deletar um pedido no CRUD.

    Em um projeto real, isso seria algo como:
        crud.deletar_pedido(pedido_id)
    ou:
        database.delete_pedido(pedido_id)
    """
    if pedido_id not in pedidos_mock:
        raise HTTPException(status_code=404, detail="Pedido não encontrado para deletar.")

    del pedidos_mock[pedido_id]


class PagamentoRequest(BaseModel):
    pedido_id: int = Field(..., gt=0)
    numero_cartao: str = Field(..., min_length=13, max_length=19)
    nome_titular: str = Field(..., min_length=2)
    validade: str = Field(..., pattern=r"^(0[1-9]|1[0-2])\/\d{2}$")
    cvv: str = Field(..., min_length=3, max_length=4, pattern=r"^\d{3,4}$")
    valor: float = Field(..., gt=0)


class PagamentoResponse(BaseModel):
    valido: bool
    mensagem: str
    status: str


def somente_digitos(valor: str) -> str:
    return "".join(d for d in valor if d.isdigit())


def validar_luhn(numero: str) -> bool:
    """Validação simples do cartão (algoritmo de Luhn).

    Não é uma IA fazendo magia. É só uma regra matemática bem básica:
    - percorre os dígitos de trás para frente
    - dobra certos números
    - soma tudo
    - se o resto da divisão por 10 for 0, é válido
    """
    numero = somente_digitos(numero)
    if len(numero) < 13:
        return False

    soma = 0
    dobrar = False

    for digito in reversed(numero):
        valor = int(digito)
        if dobrar:
            valor *= 2
            if valor > 9:
                valor -= 9
        soma += valor
        dobrar = not dobrar

    return soma % 10 == 0


@router.post("/validar", response_model=PagamentoResponse)
async def validar_pagamento_mock(pagamento: PagamentoRequest):
    """Valida um pagamento mock e remove o pedido do banco mock.

    Esse é um exemplo didático, sem complicação.
    Se a validação passar, o pedido é apagado da lista de pendentes.
    """
    numero = somente_digitos(pagamento.numero_cartao)
    nome = pagamento.nome_titular.strip()

    if not nome:
        raise HTTPException(status_code=400, detail="Nome do titular não pode estar vazio.")

    if len(numero) < 13 or len(numero) > 19:
        raise HTTPException(status_code=400, detail="Número do cartão inválido.")

    if not validar_luhn(numero):
        raise HTTPException(status_code=400, detail="Número do cartão não passou na validação mock.")

    if pagamento.valor > 10000:
        raise HTTPException(status_code=400, detail="Valor acima do limite mock permitido.")

    # -------------------------------------------------------------------
    # Aqui o pedido é deletado depois da validação.
    # Em um projeto real, isso seria substituído por algo como:
    #   crud.deletar_pedido(pagamento.pedido_id)
    # ou
    #   database.delete_pedido(pagamento.pedido_id)
    # -------------------------------------------------------------------
    deletar_pedido_mock(pagamento.pedido_id)

    return {
        "valido": True,
        "mensagem": (
            "Pagamento mock validado com sucesso. "
            "Nenhuma transação real foi realizada e o pedido foi removido da lista mock."
        ),
        "status": "mock-validado",
    }


# ---------------------------------------------------------------------------
# Como seria no projeto real (apenas a lógica, sem ser "IA esperta"):
#
# no crud.py:
# def deletar_pedido(pedido_id: int):
#     with SessionLocal() as db:
#         pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
#         if pedido:
#             db.delete(pedido)
#             db.commit()
#
# no database.py:
# def get_db():
#     ...
#
# na rota:
# if pagamento_valido:
#     crud.deletar_pedido(pagamento.pedido_id)
#
# Ou seja: a rota valida o pagamento e, se tudo deu certo, chama o CRUD para
# apagar o pedido.
# ---------------------------------------------------------------------------



