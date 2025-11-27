"""
# Modelo de Usuário

Estrutura base do modelo de usuário. Este arquivo será
implementado nas próximas etapas do TDD. No momento,
não contém atributos ou mapeamento ORM, permitindo que
os testes falhem conforme a fase RED.
"""

# Base importada para futura herança dos modelos ORM
from src.core.database import Base


class User(Base):
    """
    Representa a entidade de usuário da aplicação.

    A implementação será adicionada na próxima fase
    para atender aos requisitos definidos pelos testes.
    """

    __tablename__ = "users"
    # Nenhuma coluna definida — propositalmente vazio (fase RED)
