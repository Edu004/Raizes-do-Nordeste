
# main.py
# Para obter as saídas digite no terminal: uvicorn main:app --reload or uvicorn Corrida.main:app --reload
# Ponto de entrada da API: rotas REST para o recurso "corridas"
## Estrutura das pastas:
# - main.py — ponto de entrada da API. -> pip install fastapi uvicorn sqlalchemy
# or pip install fastapi uvicorn sqlalchemy pydantic python-multipart
# - models.py — modelos ORM (SQLAlchemy).
# - schemas.py — modelos Pydantic (validação/IO).
# - database.py — sessão e engine do banco.
# - crud.py — operações CRUD desacopladas.
# - requirements.txt — dependências.  -> instalar: pip install -r /requirements.txt



#rever  todos os imports***
from infraestructure.database import Base, engine
from domain.models import (
    Cliente,
    Unidade,
    Produto,
    ProdutoUnidade,
    Estoque,
    Pedido,
    ItemPedido,
    Pagamento,
    Cupom
)

from fastapi import FastAPI, Depends, HTTPException, Query
#from sqlalchemy.orm import Session
#from typing import List


#from models import Pedido
#from schemas import PedidoCreate, PedidoUpdate, PedidoOut
#import crud
from api.routes import auth, unidades, produtos, estoque, pedidos, pagamentos 

app = FastAPI(title="Raízes do Nordeste - API",
            description="API REST para gerenciamento de uma rede de restaurantes do Nordeste",
            version="1.0.0"
)

app.include_router(auth.router)
app.include_router(unidades.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)


# Inicializa tabelas no banco (create_all só cria se não existir)
Base.metadata.create_all(bind=engine)




@app.get("/health", summary="Verifica saúde da API")
def healthcheck():
    """
    Healthcheck simples para ver se a API está de pé.
    """
    return {"status": "ok"}


#@app.get("/pedidos",
#    response_model=List[PedidoOut],
#    summary="Listar pedidos",
#    tags=["pedidos"]
#)
#def listar_pedidos(
#    skip: int = Query(0, ge=0, description="Número de registros a pular"),
#    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a retornar"),
#    db: Session = Depends(get_db)
#):
#    """
#    Lista pedidos com paginação. Use `skip` e `limit` para controlar a página.
#    """
#    pedidos = crud.get_pedidos(db, skip=skip, limit=limit)
#    return pedidos
#    
#


