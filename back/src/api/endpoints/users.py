from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
)


router = APIRouter(prefix="/users", tags=["Users"])


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


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    Instancia o serviço de usuários utilizando o repositório associado.
    """
    return UserService(UserRepository(db))


# ============================================================
#  CREATE
# ============================================================


@router.post(
    "/",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
    description="Cria um novo usuário no sistema com nome, e-mail, senha e tipo.",
)
def create_user(
    dto: UserCreateDTO,
    service: UserService = Depends(get_user_service),
):
    """
    Endpoint responsável pela criação de usuários.
    """
    try:
        return service.create_user(dto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ============================================================
#  READ
# ============================================================


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Obter usuário",
    description="Retorna os dados de um usuário pelo seu identificador.",
)
def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    """
    Consulta um usuário pelo ID.
    """
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user


# ============================================================
#  LIST
# ============================================================


@router.get(
    "/",
    response_model=list[UserResponseDTO],
    summary="Listar usuários",
    description="Retorna todos os usuários cadastrados no sistema.",
)
def list_users(
    service: UserService = Depends(get_user_service),
):
    """
    Lista todos os usuários.
    """
    return service.list_users()


# ============================================================
#  UPDATE
# ============================================================


@router.patch(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Atualizar usuário",
    description=(
        "Atualiza parcialmente os dados de um usuário existente. "
        "Somente campos enviados serão modificados."
    ),
)
def update_user(
    user_id: str,
    dto: UserUpdateDTO,
    service: UserService = Depends(get_user_service),
):
    """
    Atualiza os dados de um usuário existente.
    """
    updated = service.update_user(user_id, dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return updated


# ============================================================
#  DELETE
# ============================================================


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover usuário",
    description="Remove um usuário do sistema pelo seu identificador.",
)
def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    """
    Remove um usuário do banco de dados.
    """
    # Verifica antes de deletar
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    service.delete_user(user_id)
    return None
