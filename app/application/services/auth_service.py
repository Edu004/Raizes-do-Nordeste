from sqlalchemy.orm import Session

from domain.models import Cliente
from infraestructure.security import (
    gerar_senha,
    verificar_senha,
    gerar_token
)


def registrar_cliente(
    db: Session,
    nome: str,
    cliente_id: int,
    senha: str
):
    cliente_existente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if cliente_existente:
        return None

    novo_cliente = Cliente(
        id=cliente_id,
        nome=nome,
        senha_hash=gerar_senha(senha)
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def autenticar_cliente(
    db: Session,
    cliente_id: int,
    senha: str
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
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




