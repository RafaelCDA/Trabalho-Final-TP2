"""
Endpoints responsáveis pelo gerenciamento de bancas via API.

Esta camada expõe rotas REST para criação, listagem, consulta e exclusão
de bancas, seguindo os requisitos da HU-10. O endpoint utiliza o serviço
de bancas (BancaService) como intermediário, garantindo separação clara
entre regras de negócio e lógica de requisição/resposta.
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.repositories.banca_repository import BancaRepository
from src.services.banca_service import BancaService
from src.dto.banca_dto import (
    BancaCreateDTO,
    BancaResponseDTO,
)


router = APIRouter(prefix="/bancas", tags=["Bancas"])


# -----------------------------------------
# Dependências
# -----------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_banca_service(db: Session = Depends(get_db)) -> BancaService:
    return BancaService(BancaRepository(db))


# -----------------------------------------
# CREATE
# -----------------------------------------
@router.post(
    "/",
    response_model=BancaResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar banca",
    description="Cadastra uma nova banca no sistema.",
)
def criar_banca(
    dto: BancaCreateDTO,
    service: BancaService = Depends(get_banca_service),
):
    return service.create_banca(dto)


# -----------------------------------------
# READ (por ID)
# -----------------------------------------
@router.get(
    "/{banca_id}",
    response_model=BancaResponseDTO,
    summary="Obter banca",
    description="Retorna os dados de uma banca pelo ID.",
)
def obter_banca(
    banca_id: int,
    service: BancaService = Depends(get_banca_service),
):
    banca = service.get_banca(banca_id)
    if not banca:
        raise HTTPException(status_code=404, detail="Banca não encontrada.")
    return banca


# -----------------------------------------
# LIST
# -----------------------------------------
@router.get(
    "/",
    response_model=list[BancaResponseDTO],
    summary="Listar bancas",
    description="Retorna todas as bancas cadastradas.",
)
def listar_bancas(
    service: BancaService = Depends(get_banca_service),
):
    return service.list_bancas()


# -----------------------------------------
# DELETE
# -----------------------------------------
@router.delete(
    "/{banca_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir banca",
    description="Remove uma banca pelo seu identificador.",
)
def deletar_banca(
    banca_id: int,
    service: BancaService = Depends(get_banca_service),
):
    deleted = service.delete_banca(banca_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Banca não encontrada.")
    return None
