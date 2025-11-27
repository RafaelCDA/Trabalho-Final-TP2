"""
Repositório de Usuários

Implementa as operações CRUD utilizadas pela aplicação para gerenciar
instâncias da entidade User. Atua como camada intermediária entre o
modelo ORM e a lógica de serviços.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.user import User


class UserRepository:
    """
    Repositório responsável pelas operações de persistência da entidade User.

    Parâmetros
    ----------
    db : Session
        Sessão ativa do SQLAlchemy utilizada para executar operações no banco.
    """

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def create_user(self, name: str, email: str, password: str) -> User:
        """
        Cria e persiste um novo usuário no banco de dados.

        Retorno
        -------
        User
            Instância persistida contendo identificador e dados informados.
        """
        user = User(name=name, email=email, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Retorna o usuário correspondente ao ID informado, caso exista.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retorna o usuário correspondente ao e-mail informado, caso exista.
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self) -> List[User]:
        """
        Retorna a lista completa de usuários cadastrados.
        """
        return self.db.query(User).all()

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """
        Atualiza campos específicos do usuário informado.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário.
        kwargs : dict
            Campos a serem atualizados.

        Retorno
        -------
        User ou None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        for campo, valor in kwargs.items():
            if hasattr(user, campo) and valor is not None:
                setattr(user, campo, valor)

        self.db.commit()
        self.db.refresh(user)
        return user

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete_user(self, user_id: str) -> None:
        """
        Remove o usuário associado ao ID informado.
        """
        user = self.get_by_id(user_id)
        if not user:
            return

        self.db.delete(user)
        self.db.commit()
