"""
MODELO MÍNIMO para testes passarem
"""
from pydantic import BaseModel

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    banca: str
    lat: float
    long: float
