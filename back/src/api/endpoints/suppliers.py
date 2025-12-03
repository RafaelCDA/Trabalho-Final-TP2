"""
Endpoints da API para gerenciamento de Suppliers (Fornecedores).

Define as rotas HTTP para operações CRUD de fornecedores.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.core.database import SessionLocal
from src.repositories.supplier_repository import SupplierRepository
from src.services.supplier_service import SupplierService
from src.dto.supplier_dto import (
    SupplierCreate,
    SupplierUpdate,
    SupplierRead,
)


router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


# ============================================================
#  DEPENDÊNCIAS
# ============================================================


def get_db():
    """
    Fornece uma sessão de banco por requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_supplier_service(db: Session = Depends(get_db)) -> SupplierService:
    """
    Instancia o serviço de fornecedores utilizando o repositório associado.
    """
    return SupplierService(SupplierRepository(db))


# ============================================================
#  CREATE
# ============================================================


@router.post(
    "/",
    response_model=SupplierRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar fornecedor",
    description="Cria um novo fornecedor no sistema com nome, email, cidade e descrição.",
)
def create_supplier(
    dto: SupplierCreate,
    service: SupplierService = Depends(get_supplier_service),
):
    """
    Endpoint responsável pela criação de fornecedores.
    """
    try:
        return service.create_supplier(dto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ============================================================
#  READ
# ============================================================


@router.get(
    "/{supplier_id}",
    response_model=SupplierRead,
    summary="Obter fornecedor",
    description="Retorna os dados de um fornecedor pelo seu identificador.",
)
def get_supplier(
    supplier_id: str,
    service: SupplierService = Depends(get_supplier_service),
):
    """
    Consulta um fornecedor pelo ID.
    """
    supplier = service.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    return supplier


# ============================================================
#  LIST
# ============================================================


@router.get(
    "/",
    response_model=list[SupplierRead],
    summary="Listar fornecedores",
    description="Retorna todos os fornecedores cadastrados no sistema. Pode filtrar por cidade.",
)
def list_suppliers(
    cidade: Optional[str] = Query(None, description="Filtrar por cidade"),
    service: SupplierService = Depends(get_supplier_service),
):
    """
    Lista todos os fornecedores ou filtra por cidade.
    """
    if cidade:
        return service.list_suppliers_by_cidade(cidade)
    return service.list_suppliers()


# ============================================================
#  UPDATE
# ============================================================


@router.patch(
    "/{supplier_id}",
    response_model=SupplierRead,
    summary="Atualizar fornecedor",
    description=(
        "Atualiza parcialmente os dados de um fornecedor existente. "
        "Somente campos enviados serão modificados."
    ),
)
def update_supplier(
    supplier_id: str,
    dto: SupplierUpdate,
    service: SupplierService = Depends(get_supplier_service),
):
    """
    Atualiza os dados de um fornecedor existente.
    """
    try:
        updated = service.update_supplier(supplier_id, dto)
        if not updated:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
        return updated
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ============================================================
#  DELETE
# ============================================================


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover fornecedor",
    description="Remove um fornecedor do sistema pelo seu identificador.",
)
def delete_supplier(
    supplier_id: str,
    service: SupplierService = Depends(get_supplier_service),
):
    """
    Remove um fornecedor do banco de dados.
    """
    # Verifica antes de deletar
    supplier = service.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")

    service.delete_supplier(supplier_id)
    return None