from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.dto.user_dto import UserCreateDTO, UserResponseDTO


router = APIRouter(prefix="/users", tags=["Users"])


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
    Cria a instância do serviço de usuários com o repositório associado.
    """
    repository = UserRepository(db)
    return UserService(repository)


@router.post(
    "/",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário",
    description="Registra um novo usuário no sistema a partir de dados válidos."
)
def create_user(
    dto: UserCreateDTO,
    service: UserService = Depends(get_user_service),
):
    """
    Cadastra um novo usuário.

    Parâmetros
    ----------
    dto : UserCreateDTO
        Dados enviados no corpo da requisição contendo nome, e-mail e senha.

    Retorno
    -------
    UserResponseDTO
        Estrutura pública representando o usuário criado.

    Exceções
    --------
    HTTPException (400)
        Quando o e-mail informado já estiver cadastrado.
    """
    try:
        return service.create_user(dto)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
