"""
Modelo ORM responsável pelo mapeamento da tabela de endereços.
"""

import uuid
from datetime import datetime, timezone

from typing import Optional
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)

    street: Mapped[str] = mapped_column(String, nullable=False)
    number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    complement: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[str] = mapped_column(String, nullable=False)

    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    bancas = relationship("Banca", back_populates="address")

    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        number: Optional[str] = None,
        complement: Optional[str] = None,
        district: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ):
        now = datetime.now(timezone.utc).isoformat()

        self.id = str(uuid.uuid4())
        self.street = street
        self.number = number
        self.complement = complement
        self.district = district
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = now
        self.updated_at = now
