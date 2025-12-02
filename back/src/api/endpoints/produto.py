from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from src.api.services.produto_service import ProdutoService
from src.models.produto_model import Produto

router = APIRouter()
service = ProdutoService()

# ===============================
#  POST - Criar Produto
# ===============================
@router.post("/produtos", response_model=Produto, status_code=201)
def criar_produto(payload: Dict[str, Any]):
    try:
        produto = service.criar(payload)
        return produto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===============================
#  GET - Listar Todos
# ===============================
@router.get("/produtos", response_model=List[Produto])
def listar_produtos():
    return service.listar()


# ===============================
#  GET - Busca textual (LIKE)
#  Rota está antes de /{produto_id}
# ===============================
@router.get("/produtos/search", response_model=List[Produto])
def buscar_produtos_por_texto(text: str):
    try:
        return service.buscar_por_texto(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
#  GET - Buscar por ID
# ===============================
@router.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = service.listar()
    for p in produtos:
        if p.id == produto_id:
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


# ===============================
#  PUT - Atualizar Produto
# ===============================
@router.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, payload: Dict[str, Any]):
    produto = service.atualizar(produto_id, payload)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


# ===============================
#  PATCH - Alterar somente o preço
# ===============================
@router.patch("/produtos/{produto_id}/preco", response_model=Produto)
def alterar_preco(produto_id: int, payload: Dict[str, Any]):
    novo_preco = payload.get("preco")

    if novo_preco is None or type(novo_preco) not in (int, float) or novo_preco < 0:
        raise HTTPException(status_code=400, detail="Preço inválido.")

    produto = service.atualizar(produto_id, {"preco": novo_preco})

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


# ===============================
#  DELETE - Excluir Produto
# ===============================
@router.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):
    ok = service.excluir(produto_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return {"status": "excluído"}

