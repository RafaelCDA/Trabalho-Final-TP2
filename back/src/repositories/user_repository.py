"""
Repositório de Usuários

Centraliza as operações de acesso e manipulação da entidade User na base
de dados, servindo como intermediário entre o modelo ORM e a camada de
serviços.
"""

from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models.user import User


class UserRepository:
    """
    Encapsula as operações CRUD relacionadas à entidade User.

    Parâmetros
    ----------
    db : Session
        Sessão ativa utilizada para operações de persistência.
    """

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create_user(
        self, name: str, email: str, password: str, type: str = "user"
    ) -> User:
        """
        Registra um novo usuário no banco de dados.

        Parâmetros
        ----------
        name : str
            Nome completo do usuário.
        email : str
            Endereço de e-mail.
        password : str
            Senha associada.
        type : str
            Tipo do usuário (`user`, `admin`, `supplier`).

        Retorno
        -------
        User
            Instância persistida com identificador gerado.
        """
        user = User(name=name, email=email, password=password, type=type)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # READ
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Consulta um usuário pelo identificador.

        Parâmetros
        ----------
        user_id : str
            Identificador único.

        Retorno
        -------
        User ou None
            Registro encontrado ou None.
        """
        return self.db.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Consulta um usuário pelo e-mail.

        Parâmetros
        ----------
        email : str
            Endereço de e-mail cadastrado.

        Retorno
        -------
        User ou None
            Registro correspondente ou None.
        """
        return self.db.query(User).filter_by(email=email).first()

    def get_all(self) -> List[User]:
        """
        Retorna todos os usuários cadastrados.

        Retorno
        -------
        list[User]
            Lista com todos os registros persistidos.
        """
        return self.db.query(User).all()

    # UPDATE
    def update_user(self, user_id: str, **fields) -> Optional[User]:
        """
        Atualiza os campos informados do usuário especificado.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário.
        fields : dict
            Campos a serem atualizados.

        Retorno
        -------
        User ou None
            Instância atualizada ou None se o registro não existir.
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        for key, value in fields.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        user.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(user)
        return user

    # DELETE
    def delete_user(self, user_id: str) -> None:
        """
        Remove o usuário correspondente ao identificador.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário.

        Retorno
        -------
        None
            Não há retorno.
        """
        user = self.get_by_id(user_id)
        if not user:
            return

        self.db.delete(user)
        self.db.commit()
