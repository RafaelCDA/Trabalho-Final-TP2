"""
## Modelo ORM: Banca

Representa as bancas cadastradas pelos fornecedores na feira.
Define atributos essenciais como nome, localização, descrição e horário de funcionamento.
Gerencia informações automáticas de criação e atualização.

Utiliza SQLAlchemy ORM para mapear a tabela `bancas` e permitir operações CRUD
via camadas de repositório e serviço.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Banca(Base):
    """
    Modelo ORM da entidade **Banca**.

    - Identifica uma banca pertencente a um fornecedor.
    - Associa a banca a um endereço registrado.
    - Mantém metadados de criação e atualização.
    """

    __tablename__ = "bancas"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )

    supplier_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    address_id: Mapped[str] = mapped_column(
        String, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False
    )

    nome: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    horario_funcionamento: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    # -----------------------------
    # Relacionamentos
    # -----------------------------

    address = relationship("Address", back_populates="bancas")
    supplier = relationship("User")

    produtos = relationship(
        "Produto",
        back_populates="banca",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        supplier_id: str,
        address_id: str,
        nome: str,
        descricao: Optional[str] = None,
        horario_funcionamento: Optional[str] = None,
    ):
        """
        Inicializa uma nova instância de Banca.

        Parâmetros:
        - `supplier_id`: ID do fornecedor responsável.
        - `address_id`: ID do endereço associado.
        - `nome`: Nome comercial da banca.
        - `descricao`: Informações adicionais.
        - `horario_funcionamento`: Horários de operação.

        Define automaticamente `created_at` e `updated_at`.
        """
        now = datetime.now(timezone.utc).isoformat()

        self.supplier_id = supplier_id
        self.address_id = address_id
        self.nome = nome
        self.descricao = descricao
        self.horario_funcionamento = horario_funcionamento
        self.created_at = now
        self.updated_at = now
