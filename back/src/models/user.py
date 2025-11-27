"""
# Modelo de Usuário

Representa a entidade de usuário armazenada no banco de dados.
O modelo utiliza UUID v4 como identificador e contém os atributos
necessários para identificação e autenticação simples.
"""

import uuid
from sqlalchemy import Column, String
from src.core.database import Base


class User(Base):
    """
    Modelo ORM responsável pelo mapeamento da tabela de usuários.

    ## Campos
    - **id** (*str*): Identificador único em formato UUID v4.
    - **name** (*str*): Nome do usuário.
    - **email** (*str*): Endereço de e-mail único no sistema.
    - **password** (*str*): Senha armazenada em texto simples.

    ## Comportamento
    - O `id` é gerado automaticamente no momento da criação da instância.
    - Este modelo é compatível com o SQLAlchemy em ambiente síncrono.
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, name: str, email: str, password: str):
        """
        Inicializa a entidade de usuário com os valores fornecidos.

        ## Parâmetros
        - **name** (*str*): Nome completo do usuário.
        - **email** (*str*): Endereço de e-mail.
        - **password** (*str*): Senha em texto simples.

        ## Nota
        O identificador é gerado automaticamente no formato UUID v4.
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
