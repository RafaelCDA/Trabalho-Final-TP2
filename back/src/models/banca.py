from pydantic import BaseModel

class Banca(BaseModel):
    id: int
    fornecedor_id: int
    nome: str | None = None
