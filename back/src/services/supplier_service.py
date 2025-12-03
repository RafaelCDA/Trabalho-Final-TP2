"""
Serviço de Suppliers (Fornecedores)

Implementa a lógica de negócio relacionada aos fornecedores,
incluindo validações e regras antes de persistir os dados.
"""

from typing import Optional, Sequence

from src.repositories.supplier_repository import SupplierRepository
from src.dto.supplier_dto import SupplierCreate, SupplierUpdate, SupplierRead
from src.models.supplier import Supplier


class SupplierService:
    """
    Camada de serviço para gerenciamento de fornecedores.

    Parâmetros
    ----------
    repository : SupplierRepository
        Instância do repositório de fornecedores.
    """

    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def create_supplier(self, dto: SupplierCreate) -> SupplierRead:
        """
        Cria um novo fornecedor após validações.

        Parâmetros
        ----------
        dto : SupplierCreate
            Dados para criação do fornecedor.

        Retorno
        -------
        SupplierRead
            Dados do fornecedor criado.

        Exceções
        --------
        ValueError
            Se email já estiver cadastrado.
        """
        # Verifica se email já existe
        existing = self.repository.get_by_email(dto.email)
        if existing:
            raise ValueError(f"Email '{dto.email}' já está cadastrado.")

        supplier = self.repository.create_supplier(
            nome=dto.nome,
            email=dto.email,
            cidade=dto.cidade,
            descricao=dto.descricao,
        )

        return SupplierRead.model_validate(supplier)

    def get_supplier(self, supplier_id: str) -> Optional[SupplierRead]:
        """
        Busca um fornecedor por ID.

        Parâmetros
        ----------
        supplier_id : str
            ID do fornecedor.

        Retorno
        -------
        SupplierRead ou None
            Dados do fornecedor ou None se não encontrado.
        """
        supplier = self.repository.get_by_id(supplier_id)
        if not supplier:
            return None
        return SupplierRead.model_validate(supplier)

    def list_suppliers(self) -> Sequence[SupplierRead]:
        """
        Lista todos os fornecedores.

        Retorno
        -------
        Sequence[SupplierRead]
            Lista de fornecedores.
        """
        suppliers = self.repository.get_all()
        return [SupplierRead.model_validate(s) for s in suppliers]

    def list_suppliers_by_cidade(self, cidade: str) -> Sequence[SupplierRead]:
        """
        Lista fornecedores de uma cidade específica.

        Parâmetros
        ----------
        cidade : str
            Nome da cidade.

        Retorno
        -------
        Sequence[SupplierRead]
            Lista de fornecedores da cidade.
        """
        suppliers = self.repository.get_by_cidade(cidade)
        return [SupplierRead.model_validate(s) for s in suppliers]

    def update_supplier(
        self, supplier_id: str, dto: SupplierUpdate
    ) -> Optional[SupplierRead]:
        """
        Atualiza dados de um fornecedor.

        Parâmetros
        ----------
        supplier_id : str
            ID do fornecedor.
        dto : SupplierUpdate
            Dados para atualização.

        Retorno
        -------
        SupplierRead ou None
            Dados atualizados ou None se não encontrado.

        Exceções
        --------
        ValueError
            Se email já estiver em uso por outro fornecedor.
        """
        # Se está tentando mudar email, verifica se já existe
        if dto.email:
            existing = self.repository.get_by_email(dto.email)
            if existing and existing.id != supplier_id:
                raise ValueError(f"Email '{dto.email}' já está em uso.")

        # Monta dict apenas com campos fornecidos
        update_data = dto.model_dump(exclude_unset=True)

        supplier = self.repository.update_supplier(supplier_id, **update_data)
        if not supplier:
            return None

        return SupplierRead.model_validate(supplier)

    def delete_supplier(self, supplier_id: str) -> None:
        """
        Remove um fornecedor.

        Parâmetros
        ----------
        supplier_id : str
            ID do fornecedor.

        Retorno
        -------
        None
        """
        self.repository.delete_supplier(supplier_id)