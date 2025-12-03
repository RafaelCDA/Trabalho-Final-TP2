"""
Repositório de Pesquisas

Responsável por registrar e consultar pesquisas realizadas pelos usuários.
Serve como ponte entre o modelo Pesquisa e a camada de serviços.
"""

from typing import Optional, Sequence, List
from sqlalchemy.orm import Session

from src.models.pesquisa import Pesquisa


class PesquisaRepository:
    """
    Encapsula as operações relacionadas à entidade Pesquisa.
    """

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================
    def registrar(
        self,
        termo: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> Pesquisa:
        """
        Registra uma nova pesquisa no banco de dados.
        """
        pesquisa = Pesquisa(
            termo=termo,
            latitude=latitude,
            longitude=longitude,
        )

        self.db.add(pesquisa)
        self.db.commit()
        self.db.refresh(pesquisa)
        return pesquisa

    # ============================================================
    # LIST
    # ============================================================
    def listar_todas(self) -> Sequence[Pesquisa]:
        """
        Retorna todas as pesquisas registradas.
        """
        return self.db.query(Pesquisa).all()

    # ============================================================
    # GET BY ID
    # ============================================================
    def get_by_id(self, pesquisa_id: int) -> Optional[Pesquisa]:
        """
        Retorna uma pesquisa específica pelo ID.
        """
        return self.db.query(Pesquisa).filter_by(id=pesquisa_id).first()

    def get_all(self) -> List[Pesquisa]:
        return self.db.query(Pesquisa).all()