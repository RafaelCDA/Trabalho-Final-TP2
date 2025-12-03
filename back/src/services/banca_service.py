from typing import List, Optional

from src.repositories.banca_repository import BancaRepository
from src.repositories.address_repository import AddressRepository

from src.dto.banca_dto import (
    BancaCreate,
    BancaRead,
    BancaUpdate,
)
from src.dto.address_dto import AddressRead # Importante para conversão

from src.models.banca import Banca
from src.models.address import Address


class BancaService:
    def __init__(self, banca_repo: BancaRepository, address_repo: AddressRepository):
        self.banca_repo = banca_repo
        self.address_repo = address_repo

    # CREATE
    def create_banca(self, dto: BancaCreate) -> BancaRead:
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

        # Retorna com o endereço recém-criado
        return BancaRead(
            id=banca.id,
            nome=banca.nome,
            descricao=banca.descricao,
            horario_funcionamento=banca.horario_funcionamento,
            supplier_id=banca.supplier_id,
            address_id=banca.address_id,
            address=AddressRead.model_validate(address), # Preenche o objeto AddressRead
            created_at=banca.created_at,
            updated_at=banca.updated_at,
        )

    # READ
    def get_banca(self, banca_id: int) -> Optional[BancaRead]:
        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return None

        # O SQLAlchemy carrega banca.address automaticamente
        return BancaRead.model_validate(banca)

    # LIST
    def list_bancas(self) -> List[BancaRead]:
        bancas = self.banca_repo.get_all()
        # Converte a lista de models para lista de DTOs (incluindo endereços)
        return [BancaRead.model_validate(b) for b in bancas]

    # UPDATE
    def update_banca(self, banca_id: int, dto: BancaUpdate) -> Optional[BancaRead]:
        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return None

        updated = self.banca_repo.update_banca(banca_id, **dto.dict(exclude_none=True))

        if updated is None:
            return None

        return BancaRead.model_validate(updated)

    # DELETE
    def delete_banca(self, banca_id: int) -> bool:
        banca = self.banca_repo.get_by_id(banca_id)
        if not banca:
            return False

        self.banca_repo.delete_banca(banca_id)
        return True