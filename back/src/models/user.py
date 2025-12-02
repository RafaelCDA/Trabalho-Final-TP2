"""
Modelo ORM responsável pelo mapeamento da tabela de usuários.

Contém os atributos essenciais para identificação e autenticação, incluindo
nome, e-mail, senha, tipo de usuário e registros de criação e atualização.
O identificador é gerado automaticamente no formato UUID v4.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
from src.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    type: Mapped[str] = mapped_column(
        Enum("user", "admin", "supplier", name="user_type"),
        nullable=False,
        default="user",
    )

    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, name: str, email: str, password: str, type: str = "user"):
        """
        Inicializa a entidade de usuário.

        ### Parâmetros
        - **name** (`str`): Nome do usuário.
        - **email** (`str`): E-mail do usuário.
        - **password** (`str`): Senha do usuário.
        - **type** (`str`): Tipo do usuário (`user`, `admin`, `supplier`).

        ### Retorno
        - Nenhum. A instância é criada com UUID e timestamps automáticos.
        """
        if type not in ("user", "admin", "supplier"):
            raise ValueError("Invalid user type.")

        now = datetime.now(timezone.utc).isoformat()

        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
        self.type = type
        self.created_at = now
        self.updated_at = now
