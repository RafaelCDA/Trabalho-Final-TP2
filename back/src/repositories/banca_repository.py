from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models.banca import Banca

class BancaRepository:
    """
    Responsável por operações de persistência da entidade Banca.
    Realiza criação, consulta, listagem e exclusão.
    """

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    def create(self, nome: str, localizacao: str, descricao: str = None, horario_funcionamento: str = None) -> Banca:
        banca = Banca(
            nome=nome,
            localizacao=localizacao,
            descricao=descricao,
            horario_funcionamento=horario_funcionamento,
        )

        self.db.add(banca)
        self.db.commit()
        self.db.refresh(banca)
        return banca

    # READ (por ID)
    def get_by_id(self, banca_id: int) -> Optional[Banca]:
        return self.db.query(Banca).filter_by(id=banca_id).first()

    # LIST (todas as bancas)
    def list_all(self) -> List[Banca]:
        return self.db.query(Banca).all()

    # DELETE
    def delete(self, banca: Banca) -> None:
        self.db.delete(banca)
        self.db.commit()
