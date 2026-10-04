



from app.infraestructure.database import Base, engine
from app.infraestructure.database import get_db
from fastapi import FastAPI, Depends, HTTPException, Query
from app.api.routes import auth, unidades, produtos, estoque, pedidos, pagamentos 



app = FastAPI(title="Raízes do Nordeste - API",
            description="API REST para gerenciamento de uma rede de restaurantes do Nordeste",
            version="1.0.0"
)

#import de todos os router junto de seus services posteriormente
app.include_router(auth.router)
app.include_router(unidades.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)



#import dos modelos
from app.domain.models import (
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

# incializar tabelas no banco e só criando elas se não existir
Base.metadata.create_all(bind=engine)


#testar se a api está funcionando
@app.get("/health", summary="Verifica saúde da API")
def healthcheck():
    
    return {"status": "ok"}





