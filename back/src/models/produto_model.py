from pydantic import BaseModel
from typing import List, Optional

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    banca: str
    lat: float
    long: float
    categoria: Optional[str] = None
    avaliacao: Optional[float] = 0.0

class BuscaRequest(BaseModel):
    termo: str
    usuario_lat: float
    usuario_long: float
    criterio_ordenacao: Optional[str] = "preco"
    distancia_maxima: Optional[float] = None

class BuscaResponse(BaseModel):
    resultados: List[Produto]
    total: int
    termo_buscado: str
