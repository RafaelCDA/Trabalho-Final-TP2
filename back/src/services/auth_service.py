"""
Serviço responsável pela autenticação simples de usuários.

Executa validações básicas utilizando DTOs como interface e
consulta o repositório para verificar credenciais.
"""

from src.dto.user_dto import LoginDTO, UserResponseDTO
from src.repositories.user_repository import UserRepository


class AuthService:
    """
    Fornece operações de autenticação simples utilizando e-mail e senha.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Parâmetros
        ----------
        user_repository : UserRepository
            Repositório utilizado para acesso aos dados de usuário.
        """
        self.user_repository = user_repository

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------
    def login_user(self, dto: LoginDTO) -> UserResponseDTO:
        """
        Realiza autenticação simples de usuário baseado em e-mail e senha.

        Parâmetros
        ----------
        dto : LoginDTO
            Estrutura contendo e-mail e senha enviados para login.

        Retorno
        -------
        UserResponseDTO
            Dados públicos do usuário autenticado.

        Exceções
        --------
        ValueError
            Quando o e-mail não existe ou a senha está incorreta.
        """
        user = self.user_repository.get_by_email(dto.email)
        if not user:
            raise ValueError("E-mail não encontrado.")

        # Pyright-safe: garantir que é str e não Column
        if str(user.password) != dto.password:
            raise ValueError("Senha incorreta.")

        return UserResponseDTO(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )
