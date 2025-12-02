from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService
from src.dto.user_dto import LoginDTO, UserResponseDTO


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)


@router.post("/login", response_model=UserResponseDTO)
def login(dto: LoginDTO, service: AuthService = Depends(get_auth_service)):
    """
    Realiza autenticação simples baseada em e-mail e senha.

    Parâmetros
    ----------
    dto : LoginDTO
        Dados enviados para autenticação.

    Retorno
    -------
    UserResponseDTO
        Informações públicas do usuário autenticado.

    Exceções
    --------
    HTTPException (401)
        Quando as credenciais não correspondem.
    """
    try:
        user = service.login_user(dto)
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
