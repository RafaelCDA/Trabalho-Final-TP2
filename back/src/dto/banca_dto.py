from typing import Optional
from pydantic import BaseModel

class BancaCreateDTO(BaseModel):
    nome: str
    localizacao: str
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None

class BancaResponseDTO(BaseModel):
    id: int
    nome: str
    localizacao: str
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None

class BancaUpdateDTO(BaseModel):
    nome: Optional[str] = None
    localizacao: Optional[str] = None
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None
