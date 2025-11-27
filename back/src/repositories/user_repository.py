"""
Repositório de Usuários

Centraliza as operações de acesso e manipulação da entidade User na base
de dados. Este módulo serve como intermediário entre o modelo ORM e a
camada de serviços, garantindo um ponto único para operações de
persistência.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.user import User


class UserRepository:
    """
    Encapsula as operações CRUD relacionadas à entidade User.

    Parâmetros
    ----------
    db : Session
        Sessão ativa utilizada para executar comandos SQL e transações.
    """

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create_user(self, name: str, email: str, password: str) -> User:
        """
        Registra um novo usuário no banco de dados.

        Parâmetros
        ----------
        name : str
            Nome completo do usuário.
        email : str
            Endereço de e-mail, utilizado como identificador único.
        password : str
            Senha associada ao usuário.

        Retorno
        -------
        User
            Instância persistida contendo o identificador e os dados enviados.
        """
        user = User(name=name, email=email, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # READ
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Consulta um usuário pelo identificador único.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário (UUID v4).

        Retorno
        -------
        User ou None
            Instância correspondente ou None caso o registro não exista.
        """
        return self.db.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Consulta um usuário pelo endereço de e-mail.

        Parâmetros
        ----------
        email : str
            Endereço de e-mail cadastrado.

        Retorno
        -------
        User ou None
            Instância encontrada ou None se não houver correspondência.
        """
        return self.db.query(User).filter_by(email=email).first()

    def get_all(self) -> List[User]:
        """
        Retorna todos os usuários cadastrados.

        Retorno
        -------
        list[User]
            Lista contendo todas as instâncias persistidas.
        """
        return self.db.query(User).all()

    # UPDATE
    def update_user(self, user_id: str, **fields) -> Optional[User]:
        """
        Atualiza os campos enviados para o usuário especificado.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário a ser atualizado.
        fields : dict
            Conjunto chave-valor com os campos a serem modificados.

        Retorno
        -------
        User ou None
            Instância atualizada ou None caso o registro não exista.
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        for key, value in fields.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    # DELETE
    def delete_user(self, user_id: str) -> None:
        """
        Remove o usuário correspondente ao ID informado.

        Parâmetros
        ----------
        user_id : str
            Identificador do registro a ser removido.

        Retorno
        -------
        None
            Não há retorno. Caso o usuário não exista, nenhuma operação é executada.
        """
        user = self.get_by_id(user_id)
        if not user:
            return

        self.db.delete(user)
        self.db.commit()
