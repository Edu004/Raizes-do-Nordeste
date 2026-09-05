import bcrypt
import jwt # type: ignore
from datetime import datetime, timedelta
import os

def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash seguro para a senha fornecida usando bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_senha(senha: str, hashed: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))

def gerar_token(payload: dict, expira_em_minutos: int = 30) -> str:
    """
    Gera um token JWT com o payload fornecido e tempo de expiração.
    """
    payload_copy = payload.copy()
    payload_copy['exp'] = datetime.utcnow() + timedelta(minutes=expira_em_minutos)
    secret_key = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_aqui")
    token = jwt.encode(payload_copy, secret_key, algorithm="HS256")
    return token



