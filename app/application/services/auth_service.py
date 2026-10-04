from sqlalchemy.orm import Session

from app.domain.models import Cliente
from app.infraestructure.security import (
    gerar_senha,
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
        senha_hash=gerar_senha(senha)
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def autenticar_cliente(
    db: Session,
    nome: str,
    senha: str,
    tipo_cliente:str
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




