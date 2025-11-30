from typing import List, Optional
from datetime import datetime, timezone

from src.repositories.banca_repository import BancaRepository
from src.dto.banca_dto import (
    BancaCreateDTO,
    BancaResponseDTO,
    BancaUpdateDTO,
)


def _to_iso(value):
    """Converte datetime para ISO string, se necessário."""
    return value if isinstance(value, str) else value.isoformat()


class BancaService:
    """
    Serviço intermediário para operações de gerenciamento de bancas.
    Versão simplificada: sem autenticação, sem validações complexas.
    """

    def __init__(self, repository: BancaRepository):
        self.repository = repository

    # CREATE
    def create_banca(self, dto: BancaCreateDTO) -> BancaResponseDTO:
        banca = self.repository.create(
            nome=dto.nome,
            localizacao=dto.localizacao,
            descricao=dto.descricao,
            horario_funcionamento=dto.horario_funcionamento,
        )

        return BancaResponseDTO(
            id=banca.id,
            nome=banca.nome,
            localizacao=banca.localizacao,
            descricao=banca.descricao,
            horario_funcionamento=banca.horario_funcionamento,
        )

    # READ
    def get_banca(self, banca_id: int) -> Optional[BancaResponseDTO]:
        banca = self.repository.get_by_id(banca_id)
        if not banca:
            return None

        return BancaResponseDTO(
            id=banca.id,
            nome=banca.nome,
            localizacao=banca.localizacao,
            descricao=banca.descricao,
            horario_funcionamento=banca.horario_funcionamento,
        )

    # LIST
    def list_bancas(self) -> List[BancaResponseDTO]:
        bancas = self.repository.list_all()

        return [
            BancaResponseDTO(
                id=b.id,
                nome=b.nome,
                localizacao=b.localizacao,
                descricao=b.descricao,
                horario_funcionamento=b.horario_funcionamento,
            )
            for b in bancas
        ]

    # DELETE
    def delete_banca(self, banca_id: int) -> bool:
        banca = self.repository.get_by_id(banca_id)
        if not banca:
            return False

        self.repository.delete(banca)
        return True
