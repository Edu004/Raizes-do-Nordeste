from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.domain.models import Cliente
#from app.schemas import ClienteBase, LoginRequest 

from app.infraestructure.security import (
    gerar_hash_senha,
    verificar_senha,
    gerar_token
)#importar funções de lgpd

#registrar e validar cliente por senha e seu tipo
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
        senha_hash=gerar_hash_senha(senha)
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def autenticar_cliente(
    db: Session,
    nome: str,
    senha: str
    #tipo_cliente: str não esta sendo utilizado então pode sair*
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.nome == nome)
        .first()
    )

    if not cliente:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not verificar_senha(senha, cliente.senha_hash):
        raise HTTPException(
                    status_code=401,
                    detail="Senha incorreta")

    token = gerar_token({
        "sub": str(cliente.id),
        "tipo_cliente": cliente.tipo_cliente
    })

    return token



