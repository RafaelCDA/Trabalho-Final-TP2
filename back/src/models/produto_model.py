"""
## Modelo ORM: Produto

Representa os produtos cadastrados em uma banca.
Cada item mantém vínculo direto com a entidade **Banca** e registra
informações essenciais como nome, preço e imagem, além dos dados
automáticos de criação e atualização.

Utiliza SQLAlchemy ORM para mapear a tabela `produtos`, permitindo
operações de consulta e persistência pelas camadas de repositório e serviço.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Produto(Base):
    """
    Modelo ORM da entidade **Produto**.

    - Associa cada produto a uma banca específica.
    - Armazena dados comerciais como nome, preço e imagem.
    - Mantém controle automático de criação e atualização.
    """

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
        """
        Inicializa uma nova instância de Produto.

        Parâmetros:
        - `banca_id`: Identificador da banca proprietária do produto.
        - `nome`: Nome comercial do item.
        - `preco`: Valor do produto.
        - `imagem`: Caminho ou URL da imagem ilustrativa (opcional).

        Define automaticamente `created_at` e `updated_at` no padrão ISO 8601 (UTC).
        """
        now = datetime.now(timezone.utc).isoformat()

        self.banca_id = banca_id
        self.nome = nome
        self.preco = preco
        self.imagem = imagem
        self.created_at = now
        self.updated_at = now
