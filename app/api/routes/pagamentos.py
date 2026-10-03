from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


pedidos_mock = {
    1: {"id": 1, "status": "pendente"},
    2: {"id": 2, "status": "pendente"},
    3: {"id": 3, "status": "pendente"},
}


def deletar_pedido_mock(pedido_id: int) -> None:
    """Simula a função de deletar um pedido no CRUD.

    """
    if pedido_id not in pedidos_mock:
        raise HTTPException(status_code=404, detail="Pedido não encontrado para deletar.")

    del pedidos_mock[pedido_id]


class PagamentoRequest(BaseModel):
    pedido_id: int = Field(..., gt=0)
    valor: float = Field(..., gt=0)


class PagamentoResponse(BaseModel):
    valido: bool
    mensagem: str
    status: str



