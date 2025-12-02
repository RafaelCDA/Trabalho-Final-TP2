"""
Repositório de Endereços

Centraliza as operações de acesso e manipulação da entidade Address na base
de dados, servindo como intermediário entre o modelo ORM e a camada de
serviços.
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
        Sessão ativa utilizada para operações de persistência.
    """

    def __init__(self, db: Session):
        self.db = db

    # CREATE
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
            Cidade.
        state : str
            Unidade federativa.
        zip_code : str
            CEP.
        number : str | None
            Número do imóvel.
        complement : str | None
            Complemento adicional.
        district : str | None
            Bairro.
        latitude : float | None
            Latitude geográfica.
        longitude : float | None
            Longitude geográfica.

        Retorno
        -------
        Address
            Instância persistida com identificador gerado.
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

    # READ
    def get_by_id(self, address_id: str) -> Optional[Address]:
        """
        Consulta um endereço pelo identificador.

        Parâmetros
        ----------
        address_id : str
            Identificador único.

        Retorno
        -------
        Address ou None
            Registro encontrado ou None.
        """
        return self.db.query(Address).filter_by(id=address_id).first()

    def get_all(self) -> Sequence[Address]:
        """
        Retorna todos os endereços cadastrados.

        Retorno
        -------
        Sequence[Address]
            Lista com todos os registros persistidos.
        """
        return self.db.query(Address).all()

    # UPDATE
    def update_address(self, address_id: str, **fields) -> Optional[Address]:
        """
        Atualiza os campos informados do endereço especificado.

        Parâmetros
        ----------
        address_id : str
            Identificador do endereço.
        fields : dict
            Campos a serem atualizados.

        Retorno
        -------
        Address ou None
            Instância atualizada ou None se o registro não existir.
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

    # DELETE
    def delete_address(self, address_id: str) -> None:
        """
        Remove o endereço correspondente ao identificador.

        Parâmetros
        ----------
        address_id : str
            Identificador do endereço.

        Retorno
        -------
        None
            Não há retorno.
        """
        address = self.get_by_id(address_id)
        if not address:
            return

        self.db.delete(address)
        self.db.commit()
