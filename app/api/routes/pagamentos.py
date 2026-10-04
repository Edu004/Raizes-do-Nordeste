from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.services import pagamento_service
from app.infraestructure.database import get_db
from app.schemas import PagamentoBase,PedidoBase
#from app.domain.models import Pagamento,Pedido
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])



class PagamentoResponse(BaseModel):
    valido: bool
    mensagem: str
    status: str



@router.post("/status/{pedido_id}", response_model=PagamentoResponse)
def processar_pagamento(pedido_id: int, dados: PagamentoBase, db: Session = Depends(get_db)):
    pagamento, erro = pagamento_service.processar_pagamento(db, pedido_id, dados.valor)
    if erro:
        raise HTTPException(status_code=404, detail=erro)

    return PagamentoResponse(
        valido=(pagamento.status_pag == "APROVADO"),
        mensagem="Pagamento processado com sucesso" if pagamento.status_pag == "APROVADO" else "Pagamento recusado",
        status=pagamento.status_pag
    )






