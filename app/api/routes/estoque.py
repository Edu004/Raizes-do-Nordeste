"""Exemplo de estoque de restaurante com SQLite e FastAPI.

Produtos entram no estoque por meio de /recebimentos. A quantidade só é
retirada quando a venda é concluída em /vendas/{venda_id}/concluir.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(prefix="/estoque", tags=["Estoque"])
DB_PATH = Path(__file__).resolve().parents[4] / "estoque.db"


class ProdutoEntrada(BaseModel):
	nome: str = Field(min_length=1)
	unidade: str = Field(default="un")
	quantidade: float = Field(gt=0)
	custo_unitario: float = Field(ge=0)


class ItemVenda(BaseModel):
	produto_id: int
	quantidade: float = Field(gt=0)


class VendaEntrada(BaseModel):
	itens: list[ItemVenda] = Field(min_length=1)


def conectar() -> sqlite3.Connection:
	conexao = sqlite3.connect(DB_PATH)
	conexao.row_factory = sqlite3.Row
	conexao.execute("PRAGMA foreign_keys = ON")
	return conexao


def criar_tabelas() -> None:
	with closing(conectar()) as db:
		db.executescript(
			"""
			CREATE TABLE IF NOT EXISTS produtos (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nome TEXT NOT NULL,
				unidade TEXT NOT NULL DEFAULT 'un',
				estoque REAL NOT NULL DEFAULT 0 CHECK (estoque >= 0)
			);
			CREATE TABLE IF NOT EXISTS vendas (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				status TEXT NOT NULL DEFAULT 'PENDENTE'
			);
			CREATE TABLE IF NOT EXISTS venda_itens (
				venda_id INTEGER NOT NULL REFERENCES vendas(id),
				produto_id INTEGER NOT NULL REFERENCES produtos(id),
				quantidade REAL NOT NULL CHECK (quantidade > 0),
				PRIMARY KEY (venda_id, produto_id)
			);
			"""
		)
		db.commit()


criar_tabelas()


@router.post("/recebimentos", status_code=201)
def receber_produto(entrada: ProdutoEntrada):
	"""Cadastra o produto (se necessário) e soma a quantidade recebida."""
	with closing(conectar()) as db:
		produto = db.execute(
			"SELECT id FROM produtos WHERE nome = ?", (entrada.nome,)
		).fetchone()
		if produto:
			produto_id = produto["id"]
			db.execute(
				"UPDATE produtos SET estoque = estoque + ? WHERE id = ?",
				(entrada.quantidade, produto_id),
			)
		else:
			cursor = db.execute(
				"INSERT INTO produtos (nome, unidade, estoque) VALUES (?, ?, ?)",
				(entrada.nome, entrada.unidade, entrada.quantidade),
			)
			produto_id = cursor.lastrowid
		db.commit()
		return {"produto_id": produto_id, "mensagem": "Produto recebido"}


@router.get("")
def consultar_estoque():
	with closing(conectar()) as db:
		return [dict(row) for row in db.execute("SELECT * FROM produtos ORDER BY nome")]


@router.post("/vendas", status_code=201)
def criar_venda(venda: VendaEntrada):
	with closing(conectar()) as db:
		try:
			cursor = db.execute("INSERT INTO vendas DEFAULT VALUES")
			venda_id = cursor.lastrowid
			for item in venda.itens:
				if not db.execute("SELECT id FROM produtos WHERE id = ?", (item.produto_id,)).fetchone():
					raise HTTPException(404, f"Produto {item.produto_id} não encontrado")
				db.execute(
					"INSERT INTO venda_itens VALUES (?, ?, ?)",
					(venda_id, item.produto_id, item.quantidade),
				)
			db.commit()
			return {"venda_id": venda_id, "status": "PENDENTE"}
		except HTTPException:
			db.rollback()
			raise


@router.post("/vendas/{venda_id}/concluir")
def concluir_venda(venda_id: int):
	"""Conclui a venda e baixa todos os itens em uma única transação."""
	with closing(conectar()) as db:
		venda = db.execute("SELECT status FROM vendas WHERE id = ?", (venda_id,)).fetchone()
		if not venda:
			raise HTTPException(404, "Venda não encontrada")
		if venda["status"] == "CONCLUIDA":
			raise HTTPException(409, "Venda já concluída")
		itens = db.execute("SELECT * FROM venda_itens WHERE venda_id = ?", (venda_id,)).fetchall()
		for item in itens:
			atual = db.execute("SELECT estoque FROM produtos WHERE id = ?", (item["produto_id"],)).fetchone()
			if atual["estoque"] < item["quantidade"]:
				raise HTTPException(409, f"Estoque insuficiente para o produto {item['produto_id']}")
		for item in itens:
			db.execute(
				"UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
				(item["quantidade"], item["produto_id"]),
			)
		db.execute("UPDATE vendas SET status = 'CONCLUIDA' WHERE id = ?", (venda_id,))
		db.commit()
		return {"venda_id": venda_id, "status": "CONCLUIDA", "mensagem": "Estoque atualizado"}


#refazer de forma menos copia e cola de ia
#entender o funcionamento e refazer!

#terminar tudo!


