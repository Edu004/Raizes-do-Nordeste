# schemas.py
# Modelos Pydantic para entrada/saída da API (validação e serialização)

from typing import Optional
from pydantic import BaseModel



class LoginRequest(BaseModel):
    nome: str
    senha: str

class ClienteCreate(BaseModel):
    
    nome:str
    usuario_id: Optional[int]

class ClienteUpdate(BaseModel):
    """
    Base de dados para criar/atualizar clientes.
    """
    nome: Optional[str] = None
    usuario_id: Optional[int] = None



class ProdutoCreate(BaseModel):
    nome: str
    categoria: str

class ProdutoUpdate(BaseModel):
    """
    Base de dados para criar/atualizar produtos.
    """
    nome: Optional[str] = None
    categoria: Optional[str] = None

class PedidoCreate(BaseModel):
    unidade_id: int
    cliente_id: Optional[int] = None
    cupom_id: Optional[int] = None
    canal_pedido: str
    status: str = "PENDENTE"
    total: float

class PedidoUpdate(BaseModel):
    """
    Base de dados para criar/atualizar pedidos.
    """
    status: Optional[str] = None
    total: Optional[float] = None

class PedidoOut(BaseModel):
    """
    Resposta enviada ao cliente.
    """
    id: int
    unidade_id: int
    cupom_id: int
    canal_pedido: str
    status: str
    total: float

    class Config:
        orm_mode = True  # Permite compatibilidade com ORM (SQLAlchemy)


class UnidadeCreate(BaseModel):
    nome: str
    cidade: str


class UnidadeUpdate(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None


class ProdutoUnidadeCreate(BaseModel):
    """
    Base de dados para criar/atualizar produto em unidade.
    """
    produto_id: int
    unidade_id: int
    preco: float
    disponivel_de: str  # ISO 8601 date string
    disponivel_ate: Optional[str] = None  # ISO 8601 date string

class ProdutoUnidadeUpdate(BaseModel):
    """
    Base de dados para criar/atualizar produto em unidade.
    """
    preco: Optional[float] = None
    disponivel_de: Optional[str] = None  # ISO 8601 date string
    disponivel_ate: Optional[str] = None  # ISO 8601 date string



class EstoqueCreate(BaseModel):
    """
    Base de dados para criar/atualizar estoque.
    """
    unidade_id: int
    produto_id: int
    quantidade: int

class EstoqueUpdate(BaseModel):
    """
    Base de dados para criar/atualizar estoque.
    """
    quantidade: Optional[int] = None

class PagamentoCreate(BaseModel):
    pedido_id: int
    valor: float



class PagamentoUpdate(BaseModel):
    """
    Base de dados para criar/atualizar pagamento.
    """
    status_pag: Optional[str] = None
    valor: Optional[float] = None



#aqui só vou chamar as variáveis,não vou aplicar algo nelas
#terminar tudo



