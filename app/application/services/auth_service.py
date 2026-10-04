from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.domain.models import Cliente
from app.schemas import ClienteBase, LoginRequest 
from app.infraestructure.security import (
    gerar_hash_senha,
    verificar_senha,
    gerar_token
)


def registrar_cliente(
    db: Session,
    nome: str,
    senha: str,
    tipo_cliente:str
):
    cliente_existente = (
        db.query(Cliente)
        .filter(Cliente.nome == nome)
        .first()
    )

    if cliente_existente:
        return None

    novo_cliente = Cliente(
        tipo_cliente=tipo_cliente,
        nome=nome,
        senha=gerar_hash_senha(senha)
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def autenticar_cliente(
    db: Session,
    nome: str,
    senha: str,
    tipo_cliente: str
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.nome == nome)
        .first()
    )

    if not cliente:
        return None

    if not verificar_senha(senha, cliente.senha_hash):
        return None

    token = gerar_token({
        "sub": str(cliente.id)
    })

    return token

def login(db: Session,
    request:str,
    nome: str,
    senha: str,
    tipo_cliente: str):

    # Verifica se o usuário existe
    cliente = db.query(Cliente).filter(Cliente.nome == request.nome).first()#como tratar em casosde clientes anonimos?
    if not cliente or not verificar_senha(request.senha, cliente.senha):
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


