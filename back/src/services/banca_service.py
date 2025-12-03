"""
## Serviço: BancaService

Responsável pela aplicação das regras de negócio relacionadas à entidade **Banca**.
Atua como intermediário entre repositórios e endpoints, garantindo integridade
dos dados, consistência das operações e isolamento das regras de negócio.

Principais responsabilidades:
- Validar os dados de criação e atualização de bancas.
- Criar automaticamente o endereço associado a uma banca.
- Encapsular lógica de leitura, listagem e exclusão.
"""

from typing import List, Optional

from src.repositories.banca_repository import BancaRepository
from src.repositories.address_repository import AddressRepository

from src.dto.banca_dto import (
    BancaCreate,
    BancaRead,
    BancaUpdate,
)

from src.models.banca import Banca
from src.models.address import Address


class BancaService:
    """
    Serviço de gerenciamento de bancas.

    Regras principais
    -----------------
    - Toda banca deve possuir um fornecedor válido (`supplier_id`).
    - Toda banca deve possuir um endereço próprio, criado a partir do DTO recebido.
    """

    def __init__(self, banca_repo: BancaRepository, address_repo: AddressRepository):
        """
        Inicializa o serviço com os repositórios necessários.

        Parâmetros
        ----------
        banca_repo : BancaRepository
            Repositório responsável pelas operações relacionadas à entidade Banca.
        address_repo : AddressRepository
            Repositório utilizado para criação e manipulação de endereços.
        """
        self.banca_repo = banca_repo
        self.address_repo = address_repo

    # ============================================================
    # CREATE
    # ============================================================
    def create_banca(self, dto: BancaCreate) -> BancaRead:
        """
        Cria uma nova banca e o endereço associado.

        Parâmetros
        ----------
        dto : BancaCreate
            Dados necessários para criar a banca e seu endereço.

        Retorno
        -------
        BancaRead
            DTO contendo os dados completos da banca criada.
        """

        # 1. Criar endereço associado
        address: Address = self.address_repo.create_address(**dto.address.dict())

        # 2. Criar a banca
        banca: Banca = self.banca_repo.create_banca(
            supplier_id=dto.supplier_id,
            address_id=address.id,
            nome=dto.nome,
            descricao=dto.descricao,
            horario_funcionamento=dto.horario_funcionamento,
        )

        return BancaRead(
            id=banca.id,
            nome=banca.nome,
            descricao=banca.descricao,
            horario_funcionamento=banca.horario_funcionamento,
            supplier_id=banca.supplier_id,
            address_id=banca.address_id,
            created_at=banca.created_at,
            updated_at=banca.updated_at,
        )

    # ============================================================
    # READ
    # ============================================================
    def get_banca(self, banca_id: int) -> Optional[BancaRead]:
        """
        Retorna uma banca específica pelo ID.

        Parâmetros
        ----------
        banca_id : int
            Identificador da banca.

        Retorno
        -------
        BancaRead | None
            DTO da banca encontrada ou None caso não exista.
        """
        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return None

        return BancaRead(
            id=banca.id,
            nome=banca.nome,
            descricao=banca.descricao,
            horario_funcionamento=banca.horario_funcionamento,
            supplier_id=banca.supplier_id,
            address_id=banca.address_id,
            created_at=banca.created_at,
            updated_at=banca.updated_at,
        )

    # ============================================================
    # LIST
    # ============================================================
    def list_bancas(self) -> List[BancaRead]:
        """
        Retorna todas as bancas cadastradas.

        Retorno
        -------
        List[BancaRead]
            Lista de DTOs contendo as bancas registradas.
        """
        bancas = self.banca_repo.get_all()

        return [
            BancaRead(
                id=b.id,
                nome=b.nome,
                descricao=b.descricao,
                horario_funcionamento=b.horario_funcionamento,
                supplier_id=b.supplier_id,
                address_id=b.address_id,
                created_at=b.created_at,
                updated_at=b.updated_at,
            )
            for b in bancas
        ]

    # ============================================================
    # UPDATE
    # ============================================================
    def update_banca(self, banca_id: int, dto: BancaUpdate) -> Optional[BancaRead]:
        """
        Atualiza parcialmente uma banca existente.

        Parâmetros
        ----------
        banca_id : int
            Identificador da banca.
        dto : BancaUpdate
            Campos que devem ser atualizados.

        Retorno
        -------
        BancaRead | None
            DTO atualizado ou None caso a banca não exista.
        """

        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return None

        updated = self.banca_repo.update_banca(banca_id, **dto.dict(exclude_none=True))

        if updated is None:
            return None

        return BancaRead(
            id=updated.id,
            nome=updated.nome,
            descricao=updated.descricao,
            horario_funcionamento=updated.horario_funcionamento,
            supplier_id=updated.supplier_id,
            address_id=updated.address_id,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )

    # ============================================================
    # DELETE
    # ============================================================
    def delete_banca(self, banca_id: int) -> bool:
        """
        Remove uma banca do sistema.

        Parâmetros
        ----------
        banca_id : int
            Identificador da banca a ser removida.

        Retorno
        -------
        bool
            True se a banca foi removida, False caso não exista.
        """

        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return False

        self.banca_repo.delete_banca(banca_id)
        return True
