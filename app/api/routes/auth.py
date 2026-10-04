from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.domain.models import Cliente
from app.schemas import ClienteBase, LoginRequest 
#from app.infraestructure.security import gerar_hash_senha, verificar_senha, gerar_token
from app.application.services import auth_service

#/ do auth
router = APIRouter(prefix="/auth", tags=["auth"])


#lgpd na criação do cliente
@router.post("/register")
def registrar_cliente(cliente: ClienteBase, db: Session = Depends(get_db)):
    resultado = auth_service.registrar_cliente(db=db, nome=cliente.nome, senha=cliente.senha, tipo_cliente=cliente.tipo_cliente)
    if resultado is None:
        raise HTTPException(status_code=400, detail="Já existe um cliente cadastrado com esse nome")
    return resultado


#este def já usa nome e senha para fazer o login do cliente
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.autenticar_cliente(db, request.nome, request.senha)



