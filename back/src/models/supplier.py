"""
Modelo ORM da entidade Supplier (Fornecedor).

Representa os fornecedores cadastrados no sistema.
Este modelo define os atributos essenciais, como nome, email, cidade
e descrição, além de informações automáticas de criação e atualização.

Utiliza SQLAlchemy ORM para mapear a estrutura da tabela e permitir
operações CRUD via repositórios e serviços.
"""

from datetime import datetime, timezone
from typing import Optional
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )

    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    cidade: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    # ============================================================
    # RELACIONAMENTOS
    # ============================================================

    # Supplier → Bancas (um fornecedor pode ter várias bancas)
    # bancas = relationship("Banca", back_populates="supplier", cascade="all, delete-orphan")

    def __init__(
        self,
        nome: str,
        email: str,
        cidade: str,
        descricao: Optional[str] = None,
    ):
        """
        Inicializa a entidade Supplier.

        Parâmetros
        ----------
        nome : str
            Nome do fornecedor.
        email : str
            Email do fornecedor (único).
        cidade : str
            Cidade onde o fornecedor está localizado.
        descricao : str | None
            Informações adicionais sobre o fornecedor.

        Retorno
        -------
        None
        """
        now = datetime.now(timezone.utc).isoformat()

        self.id = str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.cidade = cidade
        self.descricao = descricao
        self.created_at = now
        self.updated_at = now