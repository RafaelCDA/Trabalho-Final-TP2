"""
Repositório de Suppliers (Fornecedores)

Centraliza as operações de acesso e manipulação da entidade Supplier na base
de dados, servindo como intermediário entre o modelo ORM e a camada de
serviços.
"""

from typing import Optional, Sequence
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.supplier import Supplier


class SupplierRepository:
    """
    Encapsula as operações CRUD relacionadas à entidade Supplier.

    Parâmetros
    ----------
    db : Session
        Sessão ativa utilizada para operações de persistência.
    """

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create_supplier(
        self,
        nome: str,
        email: str,
        cidade: str,
        descricao: Optional[str] = None,
    ) -> Supplier:
        """
        Registra um novo fornecedor no banco de dados.

        Parâmetros
        ----------
        nome : str
            Nome do fornecedor.
        email : str
            Email do fornecedor (deve ser único).
        cidade : str
            Cidade do fornecedor.
        descricao : str | None
            Descrição adicional.

        Retorno
        -------
        Supplier
            Instância persistida com identificador gerado.
        """
        supplier = Supplier(
            nome=nome,
            email=email,
            cidade=cidade,
            descricao=descricao,
        )

        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    # READ
    def get_by_id(self, supplier_id: str) -> Optional[Supplier]:
        """
        Consulta um fornecedor pelo identificador.

        Parâmetros
        ----------
        supplier_id : str
            Identificador único do fornecedor.

        Retorno
        -------
        Supplier ou None
            Registro encontrado ou None.
        """
        return self.db.query(Supplier).filter_by(id=supplier_id).first()

    def get_by_email(self, email: str) -> Optional[Supplier]:
        """
        Consulta um fornecedor pelo email.

        Parâmetros
        ----------
        email : str
            Email do fornecedor.

        Retorno
        -------
        Supplier ou None
            Registro encontrado ou None.
        """
        return self.db.query(Supplier).filter_by(email=email).first()

    def get_all(self) -> Sequence[Supplier]:
        """
        Retorna todos os fornecedores cadastrados.

        Retorno
        -------
        Sequence[Supplier]
            Lista com todos os registros persistidos.
        """
        return self.db.query(Supplier).all()

    def get_by_cidade(self, cidade: str) -> Sequence[Supplier]:
        """
        Retorna todos os fornecedores de uma cidade.

        Parâmetros
        ----------
        cidade : str
            Nome da cidade.

        Retorno
        -------
        Sequence[Supplier]
            Lista de fornecedores da cidade.
        """
        return self.db.query(Supplier).filter_by(cidade=cidade).all()

    # UPDATE
    def update_supplier(self, supplier_id: str, **fields) -> Optional[Supplier]:
        """
        Atualiza os campos informados do fornecedor especificado.

        Parâmetros
        ----------
        supplier_id : str
            Identificador do fornecedor.
        fields : dict
            Campos a serem atualizados.

        Retorno
        -------
        Supplier ou None
            Instância atualizada ou None se o registro não existir.
        """
        supplier = self.get_by_id(supplier_id)
        if not supplier:
            return None

        for key, value in fields.items():
            if hasattr(supplier, key) and value is not None:
                setattr(supplier, key, value)

        supplier.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    # DELETE
    def delete_supplier(self, supplier_id: str) -> None:
        """
        Remove o fornecedor correspondente ao identificador.

        Parâmetros
        ----------
        supplier_id : str
            Identificador do fornecedor.

        Retorno
        -------
        None
            Não há retorno.
        """
        supplier = self.get_by_id(supplier_id)
        if not supplier:
            return

        self.db.delete(supplier)
        self.db.commit()