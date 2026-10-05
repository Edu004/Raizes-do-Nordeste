import bcrypt
import jwt 
from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, Header



def gerar_hash_senha(senha: str) -> str:
    #bcrypt para gerar senha
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_senha(senha: str, hashed: str) -> bool:
    #verificar senha fornecida
    return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))

def gerar_token(payload: dict, expira_em_minutos: int = 30) -> str:
    #Gera um token JWT com o payload fornecido e tempo de expiração.
#
    #rever como que isso será feito pois o id do cliente não é um dicionário!!!
    #
    payload_copy = payload.copy()
    payload_copy['exp'] = datetime.utcnow() + timedelta(minutes=expira_em_minutos)
    secret_key = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_aqui")
    token = jwt.encode(payload_copy, secret_key, algorithm="HS256")
    return token



def verificar_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    token = authorization.replace("Bearer ", "")
    try:
        secret_key = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_aqui")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def exigir_perfil(*perfis_permitidos):
    def verificador(payload: dict = Depends(verificar_token)):
        if payload.get("tipo_cliente") not in perfis_permitidos:
            raise HTTPException(status_code=403, detail="Perfil sem permissão para essa ação")
        return payload
    return verificador