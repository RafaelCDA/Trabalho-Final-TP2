"""
# Modelo de Usuário

Representa a entidade de usuário persistida no banco de dados. Este modelo
define os atributos essenciais para identificação e autenticação simples.

## Parâmetros
- **name** (*str*): Nome do usuário.
- **email** (*str*): Endereço de e-mail.
- **password** (*str*): Senha em texto simples.

## Retorno
Uma instância da classe `User`, com os dados informados e o identificador
gerado automaticamente.

## Observações
- O identificador utiliza o formato UUID v4 e é armazenado como string.
"""

import uuid
from sqlalchemy import Column, String
from src.core.database import Base


class User(Base):
    """
    Modelo ORM da entidade de usuário.

    ## Campos
    - **id**: Identificador único (UUID v4).
    - **name**: Nome do usuário.
    - **email**: E-mail único.
    - **password**: Senha armazenada em texto simples.
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, name: str, email: str, password: str):
        """
        ## Parâmetros
        - **name** (*str*): Nome completo do usuário.
        - **email** (*str*): Endereço de e-mail do usuário.
        - **password** (*str*): Senha utilizada no processo de autenticação.

        ## Retorno
        Instância da classe `User` com o identificador gerado automaticamente.
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
