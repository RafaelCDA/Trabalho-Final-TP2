"""
Serviço responsável pela aplicação das regras de negócio relacionadas à entidade Produto.

A camada de serviços atua como intermediária entre o repositório e a API,
validando operações, garantindo integridade dos dados e aplicando regras
exigidas pela HU-XX, incluindo validação da banca à qual o produto pertence.
"""

from typing import List, Optional

from src.repositories.produto_repository import ProdutoRepository
from src.repositories.banca_repository import BancaRepository

from src.dto.produto_dto import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoRead,
)


class ProdutoService:
    """
    Serviço intermediário para operações de gerenciamento de produtos.
    """

    def __init__(self, produto_repo: ProdutoRepository, banca_repo: BancaRepository):
        self.produto_repo = produto_repo
        self.banca_repo = banca_repo

    # ============================================================
    # CREATE
    # ============================================================
    def create_produto(self, dto: ProdutoCreate) -> ProdutoRead:
        """
        Cria um produto vinculado a uma banca existente.
        """
        # 1. Verificar se a banca existe
        banca = self.banca_repo.get_by_id(dto.banca_id)
        if not banca:
            raise ValueError("A banca informada não existe.")

        # 2. Criar o produto
        produto = self.produto_repo.create_produto(
            banca_id=dto.banca_id,
            nome=dto.nome,
            preco=dto.preco,
            imagem=dto.imagem,
        )

        return ProdutoRead(
            id=produto.id,
            nome=produto.nome,
            preco=produto.preco,
            imagem=produto.imagem,
            banca_id=produto.banca_id,
            created_at=produto.created_at,
            updated_at=produto.updated_at,
        )

    # ============================================================
    # READ
    # ============================================================
    def get_produto(self, produto_id: int) -> Optional[ProdutoRead]:
        produto = self.produto_repo.get_by_id(produto_id)

        if not produto:
            return None

        return ProdutoRead(
            id=produto.id,
            nome=produto.nome,
            preco=produto.preco,
            imagem=produto.imagem,
            banca_id=produto.banca_id,
            created_at=produto.created_at,
            updated_at=produto.updated_at,
        )

    # ============================================================
    # LIST
    # ============================================================
    def list_produtos(self) -> List[ProdutoRead]:
        produtos = self.produto_repo.get_all()

        return [
            ProdutoRead(
                id=p.id,
                nome=p.nome,
                preco=p.preco,
                imagem=p.imagem,
                banca_id=p.banca_id,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in produtos
        ]

    def list_by_banca(self, banca_id: int) -> List[ProdutoRead]:
        produtos = self.produto_repo.get_by_banca(banca_id)

        return [
            ProdutoRead(
                id=p.id,
                nome=p.nome,
                preco=p.preco,
                imagem=p.imagem,
                banca_id=p.banca_id,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in produtos
        ]

    # ============================================================
    # UPDATE
    # ============================================================
    def update_produto(
        self, produto_id: int, dto: ProdutoUpdate
    ) -> Optional[ProdutoRead]:
        # Se for atualizar banca_id, validar se nova banca existe
        if dto.banca_id is not None:
            if not self.banca_repo.get_by_id(dto.banca_id):
                raise ValueError("A banca informada não existe.")

        updated = self.produto_repo.update_produto(
            produto_id, **dto.dict(exclude_none=True)
        )

        if not updated:
            return None

        return ProdutoRead(
            id=updated.id,
            nome=updated.nome,
            preco=updated.preco,
            imagem=updated.imagem,
            banca_id=updated.banca_id,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )

    # ============================================================
    # DELETE
    # ============================================================
    def delete_produto(self, produto_id: int) -> bool:
        return self.produto_repo.delete_produto(produto_id)
