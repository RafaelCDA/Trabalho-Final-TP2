"""
Repositório de Usuários

Define a interface de acesso aos dados da entidade User. Este módulo
centraliza as operações de criação, consulta, atualização e remoção
de usuários.
"""

from src.models.user import User


class UserRepository:
    """
    Repositório responsável pelas operações CRUD da entidade User.

    Os métodos definidos aqui representam a interface de comunicação
    com o banco de dados utilizada pelas camadas superiores.
    """

    def __init__(self, db):
        """
        Inicializa o repositório com a sessão de banco fornecida.

        Parâmetros
        ----------
        db : Session
            Sessão ativa do SQLAlchemy utilizada para operações de persistência.
        """
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> User:
        """
        Cria um novo usuário no banco de dados.
        """
        raise NotImplementedError

    def get_by_id(self, user_id: str) -> User:
        """
        Retorna um usuário correspondente ao ID informado.
        """
        raise NotImplementedError

    def get_by_email(self, email: str) -> User:
        """
        Retorna um usuário correspondente ao e-mail informado.
        """
        raise NotImplementedError

    def get_all(self) -> list[User]:
        """
        Retorna a lista completa de usuários cadastrados.
        """
        raise NotImplementedError

    def update_user(self, user_id: str, **kwargs) -> User:
        """
        Atualiza os campos fornecidos para o usuário especificado.
        """
        raise NotImplementedError

    def delete_user(self, user_id: str) -> None:
        """
        Remove o usuário associado ao ID informado.
        """
        raise NotImplementedError
