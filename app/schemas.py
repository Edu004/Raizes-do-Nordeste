
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ClienteBase(BaseModel):
    nome:str
    senha:str
    tipo_cliente:str
    #usuario_id: Optional[int]#como tratar disso no auth tirar por enquanto




class ClienteUpdate(ClienteBase):
    #atualizar clientes
    nome: Optional[str] = None
    usuario_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    nome: str
    #email:str usar email para validar?
    senha: str



class ProdutoBase(BaseModel):
    nome: str
    categoria: str

class ProdutoUpdate(ProdutoBase):
    #atualizar produtos
    nome: Optional[str] = None
    categoria: Optional[str] = None


class ItemPedidoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    produto_id: int
    quantidade: int
    

class ItemPedidoUpdate(ItemPedidoBase):
    #criar ou atualizar itens de pedidos
    quantidade: Optional[int] = None
    preco_unitario: Optional[float] = None

class PedidoBase(BaseModel):
    unidade_id: int
    cliente_id: Optional[int] = None
    cupom_id: Optional[int] = None
    canal_pedido: str
    itens : list[ItemPedidoBase] = []#listar conforme a base de um item do pedido

class PedidoUpdate(PedidoBase):
    #criar/atualizar pedidos
    status: Optional[str] = None
    total: Optional[float] = None

class PedidoOut(PedidoBase):
    #o que irá vir para o cliente
    id: int
    unidade_id: int
    canal_pedido: str
    status: str
    total: float
    #produtos : list[ProdutoUpdate] = []

    model_config = ConfigDict(from_attributes=True)  # Permite compatibilidade com ORM (SQLAlchemy)


class UnidadeBase(BaseModel):
    nome: str
    cidade: str


class UnidadeUpdate(UnidadeBase):
    nome: Optional[str] = None
    cidade: Optional[str] = None


class ProdutoUnidadeBase(BaseModel):
    #atualizar produto proprio de cada unidade
    produto_id: int
    unidade_id: int
    preco: float
    disponivel_de: datetime  # ISO 8601 date string
    disponivel_ate: Optional[datetime] = None  # ISO 8601 date string

class ProdutoUnidadeUpdate(ProdutoUnidadeBase):
    #criar/atualizar produto da unidade
    preco: Optional[float] = None
    disponivel_de: Optional[datetime] = None  # ISO 8601 date string
    disponivel_ate: Optional[datetime] = None  # ISO 8601 date string



class EstoqueBase(BaseModel):
    #criar estoque
    unidade_id: int
    produto_id: int
    quantidade: int

class EstoqueUpdate(EstoqueBase):
    #atualizar estoque
    quantidade: Optional[int] = None


class PagamentoBase(BaseModel):
    pedido_id: int
    valor: float


class PagamentoUpdate(PagamentoBase ):
    #atualizar status de pagamento
    status_pag: Optional[str] = None
    valor: Optional[float] = None



#aqui só vou chamar as variáveis,não vou aplicar algo nelas




