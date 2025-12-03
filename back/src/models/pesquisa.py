"""
Modelo ORM da entidade Pesquisa.

Registra as pesquisas realizadas pelos usuários, incluindo o termo buscado,
o horário da pesquisa e, opcionalmente, a localização (latitude/longitude)
do usuário no momento da busca.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Pesquisa(Base):
    __tablename__ = "pesquisas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # termo pesquisado, ex.: "tomate"
    termo: Mapped[str] = mapped_column(String, nullable=False)

    # localização aproximada do usuário (opcional)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # momento da pesquisa em ISO 8601 (UTC)
    created_at: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(
        self,
        termo: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ):
        """
        Inicializa uma nova pesquisa.

        Parâmetros
        ----------
        termo : str
            Texto pesquisado pelo usuário (ex.: "tomate").
        latitude : float | None
            Latitude do usuário no momento da pesquisa.
        longitude : float | None
            Longitude do usuário no momento da pesquisa.
        """
        now = datetime.now(timezone.utc).isoformat()

        self.termo = termo
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = now
