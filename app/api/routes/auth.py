from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infraestructure.database import get_db
from domain.models import Cliente
from schemas import ClienteCreate , LoginRequest # type: ignore
from infraestructure.security import gerar_hash_senha, verificar_senha, gerar_token



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(cliente: ClienteCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está registrado
    cliente_existente = db.query(Cliente).filter(Cliente.id == cliente.id).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="Cliente já registrado")
    
    # Cria novo usuário com senha hash
    novo_cliente = Cliente(
        nome=cliente.nome,
        id=cliente.id,
        senha_hash=gerar_hash_senha(cliente.senha)
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    
    return {"id": novo_cliente.id, "nome": novo_cliente.nome, "email": novo_cliente.email}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    cliente = db.query(Cliente).filter(Cliente.id == request.id).first()
    if not cliente or not verificar_senha(request.senha, cliente.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Gera token JWT
    token = gerar_token(cliente.id)
    
    return {"access_token": token, "token_type": "bearer"}



