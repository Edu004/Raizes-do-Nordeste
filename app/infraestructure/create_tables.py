from app.infraestructure.database import Base,engine
from app.domain.models import Usuario , Unidade , Produto, ProdutoUnidade, Estoque, Pedido, ItemPedido, Pagamento,Cupom


def criar_tabelas():
    """
    Cria todas as tabelas no banco de dados.
    """
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()



#app/domain/models.py — espelha a Seção 2 do exemplo da biblioteca. Suas entidades: Usuario, Unidade, Produto, ProdutoUnidade, Estoque, Pedido, ItemPedido, Pagamento,Cupom