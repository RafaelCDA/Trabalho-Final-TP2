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
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from src.core.database import Base

class Banca(Base):
    __tablename__ = "bancas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    localizacao: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=True)
    horario_funcionamento: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, nome: str, localizacao: str, descricao: str = None, horario_funcionamento: str = None):
        now = datetime.now(timezone.utc).isoformat()

        self.nome = nome
        self.localizacao = localizacao
        self.descricao = descricao
        self.horario_funcionamento = horario_funcionamento
        self.created_at = now
        self.updated_at = now
