"""
Modelo ORM da entidade Produto.

Representa os produtos vendidos em uma banca. Cada produto pertence a uma banca,
mantendo vínculo via chave estrangeira. Armazena dados essenciais como nome,
preço e imagem, além dos registros automáticos de criação e atualização.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )

    banca_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("bancas.id", ondelete="CASCADE"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(String, nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    imagem: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    banca = relationship("Banca", back_populates="produtos")

    def __init__(
        self,
        banca_id: int,
        nome: str,
        preco: float,
        imagem: Optional[str] = None,
    ):
        now = datetime.now(timezone.utc).isoformat()

        self.banca_id = banca_id
        self.nome = nome
        self.preco = preco
        self.imagem = imagem
        self.created_at = now
        self.updated_at = now
