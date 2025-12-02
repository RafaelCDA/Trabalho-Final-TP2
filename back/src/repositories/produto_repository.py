"""
Repositório de Produtos

Centraliza as operações de acesso e manipulação da entidade Produto na base
de dados, servindo como intermediário entre o modelo ORM e a camada de
serviços.
"""

from typing import Optional, Sequence
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.produto_model import Produto


class ProdutoRepository:
    """
    Encapsula as operações CRUD relacionadas à entidade Produto.

    Parâmetros
    ----------
    db : Session
        Sessão ativa utilizada para operações de persistência.
    """

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================
    def create_produto(
        self,
        banca_id: int,
        nome: str,
        preco: float,
        imagem: Optional[str] = None,
    ) -> Produto:
        """
        Registra um novo produto no banco de dados.
        """
        produto = Produto(
            banca_id=banca_id,
            nome=nome,
            preco=preco,
            imagem=imagem,
        )

        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    # ============================================================
    # READ
    # ============================================================
    def get_by_id(self, produto_id: int) -> Optional[Produto]:
        """
        Consulta um produto pelo identificador.
        """
        return self.db.query(Produto).filter_by(id=produto_id).first()

    def get_all(self) -> Sequence[Produto]:
        """
        Retorna todos os produtos cadastrados.
        """
        return self.db.query(Produto).all()

    def get_by_banca(self, banca_id: int) -> Sequence[Produto]:
        """
        Retorna todos os produtos pertencentes a uma banca específica.
        """
        return self.db.query(Produto).filter_by(banca_id=banca_id).all()

    # ============================================================
    # UPDATE
    # ============================================================
    def update_produto(self, produto_id: int, **fields) -> Optional[Produto]:
        """
        Atualiza os campos informados do produto especificado.
        """
        produto = self.get_by_id(produto_id)
        if not produto:
            return None

        for key, value in fields.items():
            if hasattr(produto, key) and value is not None:
                setattr(produto, key, value)

        produto.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(produto)
        return produto

    # ============================================================
    # DELETE
    # ============================================================
    def delete_produto(self, produto_id: int) -> bool:
        """
        Remove um produto pelo seu identificador.
        """
        produto = self.get_by_id(produto_id)
        if not produto:
            return False

        self.db.delete(produto)
        self.db.commit()
        return True
