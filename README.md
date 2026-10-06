
# Raízes do Nordeste — API

API REST para gerenciamento de uma rede de restaurantes nordestinos,
desenvolvida como projeto da disciplina de Back-End (ADS).

## Tecnologias

- Python 3.13
- FastAPI 0.142.2
- SQLAlchemy 2.1.1
- Pydantic 2.13.5
- SQLite (banco local, arquivo `estoque.db`)
- PyJWT 2.15.1 (autenticação) + bcrypt (hash de senha)

## Dependências

Verifique em `requirements.txt`. Principais:
`fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `PyJWT`, `bcrypt`.

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (não é obrigatório — se não
criar, a API usa um valor padrão só pra ambiente de desenvolvimento):

JWT_SECRET_KEY=troque_por_uma_chave_secreta_sua


## Como instalar e rodar

1. Clone o repositório:

git clone https://github.com/Edu004/raizes-do-nordeste.git cd raizes-do-nordeste

2. Crie e ative um ambiente virtual:

python -m venv .venv .venv\Scripts\activate # Windows source .venv/bin/activate # Linux/Mac

3. Instale as dependências:

pip install -r requirements.txt

4. (Opcional) crie o arquivo `.env` com `JWT_SECRET_KEY` (veja seção
   acima).

## Banco de dados

O projeto usa SQLite com criação automática das tabelas: ao iniciar a
aplicação, `Base.metadata.create_all()` cria o arquivo `estoque.db` e
todas as tabelas necessárias, caso ainda não existam. Não é preciso
rodar nenhum comando de migração separado.

Se você alterar algum model (adicionar uma coluna, por exemplo) e a
tabela já existir no seu `estoque.db` local, é necessário apagar esse
arquivo manualmente para que ele seja recriado com a estrutura nova
(o SQLite/SQLAlchemy, nesse projeto, não altera tabelas já criadas).Este controle é útil para futuras correções no código.

## Como iniciar a API

uvicorn app.main:app --reload

A API sobe por padrão em `http://127.0.0.1:8000`.

## Como acessar o Swagger (documentação interativa)

Com a API rodando, acesse:

http://127.0.0.1:8000/docs

Lá é possível testar todos os endpoints diretamente pelo navegador.

## Ordem recomendada para testar o fluxo principal

1. `POST /unidades/` — criar uma unidade
2. `POST /produtos/` — criar um produto
3. `POST /produto-unidade/` — vincular o produto à unidade, com preço
4. `POST /estoque/` — cadastrar estoque desse produto nessa unidade
5. `POST /auth/register` — cadastrar um cliente
6. `POST /auth/login` — autenticar e obter o token
7. `POST /pedidos/` — criar um pedido com os itens desejados
8. `POST /pagamentos/status/{pedido_id}` — processar o pagamento
   (aprovado se o valor enviado for igual ao total do pedido)
9. `PATCH /pedidos/{pedido_id}/status` — avançar o status do pedido
   conforme a máquina de estados (PENDENTE → CONFIRMADO →
   EM_PREPARACAO → PRONTO → ENTREGUE, ou CANCELADO)


## Estrutura do projeto

app/ ├── api/routes/ # Rotas (camada de entrada da API) ├── application/services/# Regras de negócio ├── domain/ # Models (SQLAlchemy) e enums ├── infraestructure/ # Configuração de banco e segurança └── main.py # Ponto de entrada da aplicação





