from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.repositories.produto_repository import ProdutoRepository
from src.repositories.banca_repository import BancaRepository
from src.services.produto_service import ProdutoService

from src.dto.produto_dto import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoRead,
)


router = APIRouter(prefix="/produtos", tags=["Produtos"])


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


def get_produto_service(db: Session = Depends(get_db)) -> ProdutoService:
    """
    Instancia o serviço de produtos utilizando os repositórios associados.
    """
    produto_repo = ProdutoRepository(db)
    banca_repo = BancaRepository(db)
    return ProdutoService(produto_repo, banca_repo)


# ============================================================
#  CREATE
# ============================================================


@router.post(
    "/",
    response_model=ProdutoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar produto",
    description="Cria um produto vinculado a uma banca existente.",
)
def create_produto(
    dto: ProdutoCreate,
    service: ProdutoService = Depends(get_produto_service),
):
    """
    Endpoint responsável pela criação de produtos.
    """
    try:
        return service.create_produto(dto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ============================================================
#  READ
# ============================================================


@router.get(
    "/{produto_id}",
    response_model=ProdutoRead,
    summary="Obter produto",
    description="Retorna os dados de um produto pelo seu identificador.",
)
def get_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
):
    """
    Consulta um produto pelo ID.
    """
    produto = service.get_produto(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


# ============================================================
#  LIST
# ============================================================


@router.get(
    "/",
    response_model=list[ProdutoRead],
    summary="Listar produtos",
    description="Retorna todos os produtos cadastrados no sistema.",
)
def list_produtos(
    service: ProdutoService = Depends(get_produto_service),
):
    """
    Lista todos os produtos.
    """
    return service.list_produtos()


@router.get(
    "/banca/{banca_id}",
    response_model=list[ProdutoRead],
    summary="Listar produtos por banca",
    description="Retorna todos os produtos vinculados a uma banca.",
)
def list_produtos_por_banca(
    banca_id: int,
    service: ProdutoService = Depends(get_produto_service),
):
    """
    Lista produtos pertencentes à banca informada.
    """
    return service.list_by_banca(banca_id)


# ============================================================
#  UPDATE
# ============================================================


@router.patch(
    "/{produto_id}",
    response_model=ProdutoRead,
    summary="Atualizar produto",
    description=(
        "Atualiza parcialmente os dados de um produto existente. "
        "Somente campos enviados serão modificados."
    ),
)
def update_produto(
    produto_id: int,
    dto: ProdutoUpdate,
    service: ProdutoService = Depends(get_produto_service),
):
    """
    Atualiza os dados de um produto existente.
    """
    try:
        updated = service.update_produto(produto_id, dto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not updated:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return updated


# ============================================================
#  DELETE
# ============================================================


@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover produto",
    description="Remove um produto do sistema pelo seu identificador.",
)
def delete_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
):
    """
    Remove o produto correspondente ao ID informado.
    """
    ok = service.delete_produto(produto_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return None
