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
def registrar_cliente(cliente: ClienteBase , db: Session = Depends(get_db)):
    return auth_service.registrar_cliente(db=db, nome=cliente.nome, senha=cliente.senha,tipo_cliente=cliente.tipo_cliente)


#este def já usa nome e senha para fazer o login do cliente
#def divergente do service dá problema?
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.autenticar_cliente(db, request.nome, request.senha)



