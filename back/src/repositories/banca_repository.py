"""
Repositório de Bancas

Centraliza as operações de acesso e manipulação da entidade Banca na base
de dados, servindo como intermediário entre o modelo ORM e a camada de
serviços.
"""

from typing import Optional, Sequence
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.banca import Banca


class BancaRepository:
    """
    Encapsula as operações CRUD relacionadas à entidade Banca.

    Parâmetros
    ----------
    db : Session
        Sessão ativa utilizada para operações de persistência.
    """

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create_banca(
        self,
        supplier_id: str,
        address_id: str,
        nome: str,
        descricao: Optional[str] = None,
        horario_funcionamento: Optional[str] = None,
    ) -> Banca:
        """
        Registra uma nova banca no banco de dados.

        Parâmetros
        ----------
        supplier_id : str
            Identificador do fornecedor proprietário da banca.
        address_id : str
            Identificador do endereço associado.
        nome : str
            Nome da banca.
        descricao : str | None
            Descrição adicional.
        horario_funcionamento : str | None
            Horário de funcionamento informado.

        Retorno
        -------
        Banca
            Instância persistida com identificador gerado.
        """
        banca = Banca(
            supplier_id=supplier_id,
            address_id=address_id,
            nome=nome,
            descricao=descricao,
            horario_funcionamento=horario_funcionamento,
        )

        self.db.add(banca)
        self.db.commit()
        self.db.refresh(banca)
        return banca

    # READ
    def get_by_id(self, banca_id: int) -> Optional[Banca]:
        """
        Consulta uma banca pelo identificador.

        Parâmetros
        ----------
        banca_id : int
            Identificador único da banca.

        Retorno
        -------
        Banca ou None
            Registro encontrado ou None.
        """
        return self.db.query(Banca).filter_by(id=banca_id).first()

    def get_all(self) -> Sequence[Banca]:
        """
        Retorna todas as bancas cadastradas.

        Retorno
        -------
        Sequence[Banca]
            Lista com todos os registros persistidos.
        """
        return self.db.query(Banca).all()

    def get_by_supplier(self, supplier_id: str) -> Sequence[Banca]:
        """
        Retorna todas as bancas associadas a um fornecedor.

        Parâmetros
        ----------
        supplier_id : str
            Identificador do fornecedor.

        Retorno
        -------
        Sequence[Banca]
            Lista de bancas pertencentes ao fornecedor.
        """
        return self.db.query(Banca).filter_by(supplier_id=supplier_id).all()

    # UPDATE
    def update_banca(self, banca_id: int, **fields) -> Optional[Banca]:
        """
        Atualiza os campos informados da banca especificada.

        Parâmetros
        ----------
        banca_id : int
            Identificador da banca.
        fields : dict
            Campos a serem atualizados.

        Retorno
        -------
        Banca ou None
            Instância atualizada ou None se o registro não existir.
        """
        banca = self.get_by_id(banca_id)
        if not banca:
            return None

        for key, value in fields.items():
            if hasattr(banca, key) and value is not None:
                setattr(banca, key, value)

        banca.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(banca)
        return banca

    # DELETE
    def delete_banca(self, banca_id: int) -> None:
        """
        Remove a banca correspondente ao identificador.

        Parâmetros
        ----------
        banca_id : int
            Identificador da banca.

        Retorno
        -------
        None
            Não há retorno.
        """
        banca = self.get_by_id(banca_id)
        if not banca:
            return

        self.db.delete(banca)
        self.db.commit()
