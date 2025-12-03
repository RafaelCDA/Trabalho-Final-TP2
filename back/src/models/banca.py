"""
Modelo ORM da entidade Banca.

Representa as bancas cadastradas pelos fornecedores dentro da feira.
Este modelo define os atributos essenciais, como nome, localização,
descrição e horário de funcionamento, além de informações automáticas
de criação e atualização.

Utiliza SQLAlchemy ORM para mapear a estrutura da tabela e permitir
operações CRUD via repositórios e serviços.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Banca(Base):
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

    # ============================================================
    # RELACIONAMENTOS
    # ============================================================

    # Banca → Address
    address = relationship("Address", back_populates="bancas")

    # Banca → Supplier (usuário do tipo supplier)
    supplier = relationship("User")

    # Banca → Produtos
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
        Inicializa a entidade Banca.

        Parâmetros
        ----------
        supplier_id : str
            ID do fornecedor responsável.
        address_id : str
            ID do endereço associado à banca.
        nome : str
            Nome da banca.
        descricao : str | None
            Informações adicionais.
        horario_funcionamento : str | None
            Horários de abertura e fechamento.

        Retorno
        -------
        None
        """
        now = datetime.now(timezone.utc).isoformat()

        self.supplier_id = supplier_id
        self.address_id = address_id
        self.nome = nome
        self.descricao = descricao
        self.horario_funcionamento = horario_funcionamento
        self.created_at = now
        self.updated_at = now
