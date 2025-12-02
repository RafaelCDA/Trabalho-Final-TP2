"""
Serviço responsável pela aplicação das regras de negócio relacionadas à entidade Banca.

A camada de serviços atua como intermediária entre os repositórios (persistência)
e os endpoints, garantindo integridade dos dados e implementando regras de negócio.
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
    Serviço intermediário para gerenciamento de bancas.

    Regras principais:
    - Uma banca deve possuir um fornecedor (supplier_id).
    - Uma banca deve possuir um endereço próprio (gerado automaticamente a partir do DTO).
    """

    def __init__(self, banca_repo: BancaRepository, address_repo: AddressRepository):
        self.banca_repo = banca_repo
        self.address_repo = address_repo

    # CREATE
    def create_banca(self, dto: BancaCreate) -> BancaRead:
        """
        Cria uma banca e seu endereço associado.
        """

        # 1. Criar endereço
        address: Address = self.address_repo.create_address(**dto.address.dict())

        # 2. Criar banca
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

    # READ
    def get_banca(self, banca_id: int) -> Optional[BancaRead]:
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

    # LIST
    def list_bancas(self) -> List[BancaRead]:
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

    # UPDATE
    def update_banca(self, banca_id: int, dto: BancaUpdate) -> Optional[BancaRead]:
        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return None

        updated = self.banca_repo.update_banca(banca_id, **dto.dict(exclude_none=True))

        # 🔥 CORREÇÃO PARA O PYRIGHT
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

    # DELETE
    def delete_banca(self, banca_id: int) -> bool:
        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return False

        self.banca_repo.delete_banca(banca_id)
        return True
