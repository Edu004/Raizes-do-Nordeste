from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infraestructure.database import get_db
from app.domain.models import Cliente
from app.schemas import ClienteBase, LoginRequest # type: ignore
from app.infraestructure.security import gerar_hash_senha, verificar_senha, gerar_token


#/ do auth
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(cliente: ClienteBase, db: Session = Depends(get_db)):
    # Verifica se o cliente já está registrado
    cliente_existente = db.query(Cliente).filter(Cliente.nome == cliente.nome).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="Cliente já registrado")
    
    # Cria novo usuário com senha hash
    novo_cliente = Cliente(
        nome=cliente.nome,
        id=cliente.id,
        tipo_cliente=cliente.tipo_cliente,
        senha_hash=gerar_hash_senha(cliente.senha)
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    
    return {"id": novo_cliente.id, 
            "nome": novo_cliente.nome, 
            "tipo_cliente": novo_cliente.tipo_cliente
            }


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



