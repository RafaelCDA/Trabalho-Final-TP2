from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.services.banca_service import BancaService
from src.repositories.banca_repository import BancaRepository
from src.repositories.address_repository import AddressRepository

from src.dto.banca_dto import (
    BancaCreate,
    BancaUpdate,
    BancaRead,
)


router = APIRouter(prefix="/bancas", tags=["Bancas"])


# ============================================================
#  DEPENDÊNCIAS
# ============================================================


def get_db():
    """
    Gera uma sessão de banco de dados por requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_banca_service(db: Session = Depends(get_db)) -> BancaService:
    banca_repo = BancaRepository(db)
    address_repo = AddressRepository(db)
    return BancaService(banca_repo, address_repo)


# ============================================================
#  CREATE
# ============================================================


@router.post(
    "/",
    response_model=BancaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar banca",
    description=(
        "Cria uma nova banca no sistema. "
        "O endereço é criado automaticamente com base nos dados enviados."
    ),
)
def create_banca(
    dto: BancaCreate,
    service: BancaService = Depends(get_banca_service),
):
    """
    Endpoint responsável pela criação de uma banca e seu endereço associado.
    """
    try:
        return service.create_banca(dto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ============================================================
#  READ
# ============================================================


@router.get(
    "/{banca_id}",
    response_model=BancaRead,
    summary="Obter banca",
    description="Retorna os dados de uma banca pelo seu identificador.",
)
def get_banca(
    banca_id: int,
    service: BancaService = Depends(get_banca_service),
):
    """
    Consulta uma banca pelo ID.
    """
    banca = service.get_banca(banca_id)
    if not banca:
        raise HTTPException(status_code=404, detail="Banca não encontrada.")
    return banca


# ============================================================
#  LIST
# ============================================================


@router.get(
    "/",
    response_model=list[BancaRead],
    summary="Listar bancas",
    description="Retorna todas as bancas cadastradas no sistema.",
)
def list_bancas(
    service: BancaService = Depends(get_banca_service),
):
    """
    Lista todas as bancas registradas.
    """
    return service.list_bancas()


# ============================================================
#  UPDATE
# ============================================================


@router.patch(
    "/{banca_id}",
    response_model=BancaRead,
    summary="Atualizar banca",
    description=(
        "Atualiza parcialmente os dados de uma banca existente. "
        "Somente campos enviados serão modificados."
    ),
)
def update_banca(
    banca_id: int,
    dto: BancaUpdate,
    service: BancaService = Depends(get_banca_service),
):
    """
    Atualiza os dados de uma banca existente.
    """
    updated = service.update_banca(banca_id, dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Banca não encontrada.")
    return updated


# ============================================================
#  DELETE
# ============================================================


@router.delete(
    "/{banca_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover banca",
    description="Remove uma banca do sistema pelo seu identificador.",
)
def delete_banca(
    banca_id: int,
    service: BancaService = Depends(get_banca_service),
):
    """
    Remove a banca correspondente ao ID informado.
    """
    banca = service.get_banca(banca_id)
    if not banca:
        raise HTTPException(status_code=404, detail="Banca não encontrada.")

    service.delete_banca(banca_id)
    return None
