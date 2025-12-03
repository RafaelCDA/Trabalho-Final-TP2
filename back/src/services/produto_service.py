"""
## Serviço: ProdutoService

Responsável pela aplicação das regras de negócio relacionadas à entidade **Produto**.

A camada de serviços atua como intermediária entre o repositório e a API,
validando operações, garantindo a integridade dos dados e aplicando regras
exigidas pelas histórias de usuário (HU), incluindo verificações sobre a banca
à qual o produto pertence.

Principais responsabilidades:
- Validar a existência da banca antes de criar ou mover um produto.
- Processar operações de CRUD.
- Retornar dados estruturados via DTOs.
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
        """
        Inicializa o serviço com os repositórios necessários.

        Parâmetros
        ----------
        produto_repo : ProdutoRepository
            Repositório responsável por operações persistentes de produto.
        banca_repo : BancaRepository
            Repositório utilizado para validar e consultar bancas.
        """
        self.produto_repo = produto_repo
        self.banca_repo = banca_repo

    # ============================================================
    # CREATE
    # ============================================================
    def create_produto(self, dto: ProdutoCreate) -> ProdutoRead:
        """
        Cria um produto vinculado a uma banca existente.

        Parâmetros
        ----------
        dto : ProdutoCreate
            Dados necessários para criação do produto.

        Regras de Negócio
        -----------------
        - A banca informada deve existir.

        Exceções
        --------
        ValueError
            Quando a banca informada não existe.

        Retorno
        -------
        ProdutoRead
            DTO contendo o produto criado.
        """

        banca = self.banca_repo.get_by_id(dto.banca_id)
        if not banca:
            raise ValueError("A banca informada não existe.")

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
        """
        Retorna um produto específico pelo ID.

        Parâmetros
        ----------
        produto_id : int
            Identificador do produto.

        Retorno
        -------
        ProdutoRead | None
            DTO do produto encontrado ou None caso não exista.
        """

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
        """
        Lista todos os produtos cadastrados.

        Retorno
        -------
        List[ProdutoRead]
            Lista completa dos produtos.
        """

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
        """
        Lista todos os produtos pertencentes a uma banca específica.

        Parâmetros
        ----------
        banca_id : int
            Identificador da banca.

        Retorno
        -------
        List[ProdutoRead]
            Produtos vinculados à banca selecionada.
        """

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
        """
        Atualiza parcialmente os dados de um produto.

        Parâmetros
        ----------
        produto_id : int
            Identificador do produto.
        dto : ProdutoUpdate
            Campos que devem ser atualizados.

        Regras de Negócio
        -----------------
        - Caso `banca_id` seja alterado, a nova banca deve existir.

        Exceções
        --------
        ValueError
            Quando a nova banca informada não existe.

        Retorno
        -------
        ProdutoRead | None
            DTO atualizado ou None caso o produto não exista.
        """

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
        """
        Remove um produto do sistema.

        Parâmetros
        ----------
        produto_id : int
            Identificador do produto.

        Retorno
        -------
        bool
            True se o produto foi removido, False caso não exista.
        """
        return self.produto_repo.delete_produto(produto_id)
