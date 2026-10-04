from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.application.services import pagamento_service
from app.infraestructure.database import get_db
from app.schemas import PagamentoBase
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])





class PagamentoResponse(BaseModel):
    valido: bool
    mensagem: str
    status: str

@router.post("/status/{pedido_id}")
def processar_pagamento():
    db: Session = Depends(get_db)
    dados = PagamentoBase
    return pagamento_service.processar_pagamento(db ,dados)









