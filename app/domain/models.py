


# models.py

from decimal import Decimal

from sqlalchemy import Boolean, Column, Integer, String, DateTime , Numeric , ForeignKey
from app.infraestructure.database import Base



class Cliente(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True , index=True)#autoincrement para ir atualizando o id com o tempo e conforme for sendo criado novos clientes
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
    preco = Column(Numeric(10,2), nullable=False)#colocar seu valor no produto
    disponivel_de = Column(DateTime(timezone=True), nullable=False)#periodo de tempo de promoções
    disponivel_ate = Column(DateTime(timezone=True), nullable=True)

class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), index=True)
    quantidade = Column(Integer, nullable=False)
    
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), index=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=True)#opcional,deixar possível a criação de clientes anonimos
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




