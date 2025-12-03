"""
## Modelo ORM: Pesquisa

Registra pesquisas realizadas pelos usuários, incluindo o termo buscado,
a data/hora da ação e, opcionalmente, a localização (latitude/longitude)
no momento da consulta.

Utiliza SQLAlchemy ORM para mapear a tabela `pesquisas` e permitir
operações de registro e consulta pela camada de serviço.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Pesquisa(Base):
    """
    Modelo ORM da entidade **Pesquisa**.

    - Armazena o termo pesquisado pelo usuário.
    - Registra metadados da busca, incluindo horário (UTC) e localização opcional.
    """

    __tablename__ = "pesquisas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    termo: Mapped[str] = mapped_column(String, nullable=False)

    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(
        self,
        termo: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ):
        """
        Inicializa uma nova instância de Pesquisa.

        Parâmetros:
        - `termo`: Texto pesquisado pelo usuário.
        - `latitude`: Localização latitude no momento da pesquisa (opcional).
        - `longitude`: Localização longitude no momento da pesquisa (opcional).

        Define automaticamente o campo `created_at` no padrão ISO 8601 (UTC).
        """
        now = datetime.now(timezone.utc).isoformat()

        self.termo = termo
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = now
