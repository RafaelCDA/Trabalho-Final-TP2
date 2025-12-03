"""
## Repositório: Pesquisa

Centraliza as operações de persistência relacionadas às pesquisas realizadas
pelos usuários.
Funciona como camada intermediária entre o modelo ORM `Pesquisa` e os serviços,
permitindo registrar pesquisas e consultar registros previamente feitos.
"""

from typing import Optional, Sequence, List
from sqlalchemy.orm import Session

from src.models.pesquisa import Pesquisa


class PesquisaRepository:
    """
    Encapsula as operações CRUD e consultas específicas da entidade Pesquisa.

    Parâmetros
    ----------
    db : Session
        Sessão ativa do SQLAlchemy utilizada para operações de banco de dados.
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

        Parâmetros
        ----------
        termo : str
            Termo digitado pelo usuário durante a busca.
        latitude : float | None
            Latitude no momento da pesquisa (opcional).
        longitude : float | None
            Longitude no momento da pesquisa (opcional).

        Retorno
        -------
        Pesquisa
            Instância persistida contendo ID e timestamp gerados.
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

        Retorno
        -------
        Sequence[Pesquisa]
            Lista completa de registros persistidos.
        """
        return self.db.query(Pesquisa).all()

    # ============================================================
    # GET BY ID
    # ============================================================
    def get_by_id(self, pesquisa_id: int) -> Optional[Pesquisa]:
        """
        Consulta uma pesquisa específica pelo ID.

        Parâmetros
        ----------
        pesquisa_id : int
            Identificador único da pesquisa.

        Retorno
        -------
        Pesquisa | None
            Instância encontrada ou None caso não exista.
        """
        return self.db.query(Pesquisa).filter_by(id=pesquisa_id).first()

    # ============================================================
    # ALIAS (DUPLICADO)
    # ============================================================
    def get_all(self) -> List[Pesquisa]:
        """
        Alias de listar_todas() mantido por compatibilidade.

        Retorno
        -------
        List[Pesquisa]
            Lista com todas as pesquisas registradas.
        """
        return self.db.query(Pesquisa).all()
