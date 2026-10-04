from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.domain.models import Cliente
from app.schemas import ClienteBase, LoginRequest # type: ignore
from app.infraestructure.security import gerar_senha, verificar_senha, gerar_token
from app.application.services import auth_service

#/ do auth
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def registrar_cliente():
    cliente: ClienteBase
    db: Session = Depends(get_db)
    return auth_service.registrar_cliente(db=db, nome=cliente.nome, senha=cliente.senha,tipo_cliente=cliente.tipo_cliente)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    cliente = db.query(Cliente).filter(Cliente.nome == request.nome).first()#como tratar em casos de clientes anonimos?
    if not cliente or not verificar_senha(request.senha, cliente.senha_hash):
        raise HTTPException(status_code=401, detail="Senha inválida")
    
    # Gera token JWT
    token = gerar_token(
        id=str(cliente.id),
        nome=cliente.nome,
        tipo_cliente=cliente.tipo_cliente
    )#mudando de .id para um dicionário juntando as variaveis
    
    return {"access_token": token, 
            "token_type": "bearer"
            }



