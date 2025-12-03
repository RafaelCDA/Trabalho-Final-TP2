"""
## Repositório: Address

Centraliza as operações de acesso e manipulação da entidade Address
na base de dados, funcionando como a camada responsável por interagir
diretamente com o ORM.
Implementa métodos padronizados de criação, consulta, atualização
e remoção.
"""

from typing import Optional, Sequence
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.address import Address


class AddressRepository:
    """
    Encapsula as operações CRUD relacionadas à entidade Address.

    Parâmetros
    ----------
    db : Session
        Sessão ativa do SQLAlchemy utilizada para persistência de dados.
    """

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------
    def create_address(
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
    ) -> Address:
        """
        Registra um novo endereço no banco de dados.

        Parâmetros
        ----------
        street : str
            Logradouro.
        city : str
            Cidade do endereço.
        state : str
            Unidade federativa.
        zip_code : str
            Código postal (CEP).
        number : str | None
            Número do imóvel.
        complement : str | None
            Complemento adicional.
        district : str | None
            Bairro.
        latitude : float | None
            Coordenada de latitude.
        longitude : float | None
            Coordenada de longitude.

        Retorno
        -------
        Address
            Instância persistida com ID e metadados preenchidos.
        """

        address = Address(
            street=street,
            number=number,
            complement=complement,
            district=district,
            city=city,
            state=state,
            zip_code=zip_code,
            latitude=latitude,
            longitude=longitude,
        )

        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    # ------------------------------------------------------------
    # READ
    # ------------------------------------------------------------
    def get_by_id(self, address_id: str) -> Optional[Address]:
        """
        Consulta um endereço pelo identificador.

        Parâmetros
        ----------
        address_id : str
            Identificador único do endereço (UUID).

        Retorno
        -------
        Address | None
            O registro encontrado ou None caso não exista.
        """
        return self.db.query(Address).filter_by(id=address_id).first()

    def get_all(self) -> Sequence[Address]:
        """
        Retorna todos os endereços cadastrados.

        Retorno
        -------
        Sequence[Address]
            Lista contendo todas as instâncias persistidas.
        """
        return self.db.query(Address).all()

    # ------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------
    def update_address(self, address_id: str, **fields) -> Optional[Address]:
        """
        Atualiza parcialmente um endereço já cadastrado.

        Parâmetros
        ----------
        address_id : str
            Identificador do endereço a ser atualizado.
        fields : dict
            Campos que devem ser modificados. Somente valores não nulos
            serão aplicados.

        Retorno
        -------
        Address | None
            Instância atualizada ou None caso o endereço não seja encontrado.
        """
        address = self.get_by_id(address_id)
        if not address:
            return None

        for key, value in fields.items():
            if hasattr(address, key) and value is not None:
                setattr(address, key, value)

        address.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(address)
        return address

    # ------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------
    def delete_address(self, address_id: str) -> None:
        """
        Remove permanentemente um endereço pelo seu ID.

        Parâmetros
        ----------
        address_id : str
            Identificador do endereço a ser removido.

        Retorno
        -------
        None
            Não há retorno. Se o endereço não existir, nenhuma ação é tomada.
        """
        address = self.get_by_id(address_id)
        if not address:
            return

        self.db.delete(address)
        self.db.commit()
