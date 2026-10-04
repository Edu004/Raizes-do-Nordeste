# schemas.py
# Modelos Pydantic para entrada/saída da API (validação e serialização)

from typing import Optional
from pydantic import BaseModel


class ClienteBase(BaseModel):
    nome:str
    senha:str
    tipo_cliente:str
    usuario_id: Optional[int]#como tratar disso no auth?




class ClienteUpdate(ClienteBase):
    """
    Base de dados para criar/atualizar clientes.
    """
    nome: Optional[str] = None
    usuario_id: Optional[int] = None
    
    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    nome: str
    #email:str usar email para validar?
    senha: str



class ProdutoBase(BaseModel):
    nome: str
    categoria: str

class ProdutoUpdate(ProdutoBase):
    """
    Base de dados para criar/atualizar produtos.
    """
    nome: Optional[str] = None
    categoria: Optional[str] = None


class ItemPedidoBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float

class ItemPedidoUpdate(ItemPedidoBase):
    """
    Base de dados para criar/atualizar itens de pedido.
    """
    quantidade: Optional[int] = None
    preco_unitario: Optional[float] = None

class PedidoBase(BaseModel):
    unidade_id: int
    cliente_id: Optional[int] = None
    cupom_id: Optional[int] = None
    canal_pedido: str
    status: str = "PENDENTE"
    total: float
    itens : list[ItemPedidoUpdate] = []

class PedidoUpdate(PedidoBase):
    """
    Base de dados para criar/atualizar pedidos.
    """
    status: Optional[str] = None
    total: Optional[float] = None

class PedidoOut(PedidoBase):
    """
    Resposta enviada ao cliente.
    """
    id: int
    unidade_id: int
    cupom_id: int
    canal_pedido: str
    status: str
    total: float
    produtos : list[ProdutoUpdate] = []

    class Config:
        orm_mode = True  # Permite compatibilidade com ORM (SQLAlchemy)


class UnidadeBase(BaseModel):
    nome: str
    cidade: str


class UnidadeUpdate(UnidadeBase):
    nome: Optional[str] = None
    cidade: Optional[str] = None


class ProdutoUnidadeBase(BaseModel):
    """
    Base de dados para criar/atualizar produto em unidade.
    """
    produto_id: int
    unidade_id: int
    preco: float
    disponivel_de: str  # ISO 8601 date string
    disponivel_ate: Optional[str] = None  # ISO 8601 date string

class ProdutoUnidadeUpdate(ProdutoUnidadeBase):
    """
    Base de dados para criar/atualizar produto em unidade.
    """
    preco: Optional[float] = None
    disponivel_de: Optional[str] = None  # ISO 8601 date string
    disponivel_ate: Optional[str] = None  # ISO 8601 date string



class EstoqueBase(BaseModel):
    """
    Base de dados para criar/atualizar estoque.
    """
    unidade_id: int
    produto_id: int
    quantidade: int

class EstoqueUpdate(EstoqueBase):
    """
    Base de dados para criar/atualizar estoque.
    """
    quantidade: Optional[int] = None


class PagamentoBase(BaseModel):
    pedido_id: int
    valor: float


class PagamentoUpdate(PagamentoBase ):
    """
    Base de dados para criar/atualizar pagamento.
    """
    status_pag: Optional[str] = None
    valor: Optional[float] = None



#aqui só vou chamar as variáveis,não vou aplicar algo nelas




