#  <- as classes que representam suas entidades (Unidade,

#                        Produto, ProdutoUnidade, Estoque, Usuario, Pedido,
#                        ItemPedido, Pagamento, Cupom)


# models.py
# Modelos de dados do domínio "pedido,estoque,todas as entidades" usando SQLAlchemy ORM

from decimal import Decimal

from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime , Numeric , ForeignKey
from sqlalchemy.sql import func
from infraestructure.database import Base



#app/domain/models.py — espelha a Seção 2 do exemplo da biblioteca. Suas entidades: Usuario, Unidade, Produto, ProdutoUnidade, Estoque, Pedido, ItemPedido, Pagamento. Traz do seu DER: usuario_id opcional em Pedido, Pedido↔Pagamento 1:1, campo cons_lgpd em Usuario


class Cliente(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=True, index=True)
    tipo_cliente = Column(String(100), nullable=False, index=True)
    senha_hash = Column(String(255), nullable=True)
    conslgpd = Column(Boolean, default = True)

class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index=True)
    cidade = Column(String(100), nullable=False, index=True)
    
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index=True)
    categoria = Column(String(100), nullable=False, index=True)
    

class ProdutoUnidade(Base):
    __tablename__ = "produtos_unidade"

    id = Column(Integer, primary_key=True, index=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), index=True)
    preco = Column(Numeric(10,2), nullable=False)
    disponivel_de = Column(DateTime(timezone=True), nullable=False)
    disponivel_ate = Column(DateTime(timezone=True), nullable=True)

class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), index=True)
    quantidade = Column(Integer, nullable=False)
    #atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), index=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=True)#opcional
    cupom_id = Column(Integer, ForeignKey("cupons.id"), index=True, nullable=False)
    canal_pedido = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    total = Column(Numeric(10,2), nullable=False)
    
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), index=True, nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), index=True, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(10,2), nullable=False)

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), index=True, nullable=False)
    status_pag = Column(String(50), nullable=False, index=True)
    valor = Column(Numeric(10,2), nullable=False)

class Cupom(Base):
    __tablename__ = "cupons"

    id = Column(Integer, primary_key=True, index=True)
    codigo_cupom = Column(String(50), nullable=False, index=True)
    tipo_desconto = Column(String(50), nullable=False)
    valor = Column(Numeric(10,2), nullable=False)


#terminar tudo!


