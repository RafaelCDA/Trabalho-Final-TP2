from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from src.api.services.produto_service import ProdutoService
from src.models.produto_model import Produto

router = APIRouter()
service = ProdutoService()

# Nota: autenticação/cheque de fornecedor não está implementado neste projeto.
# Quando houver um sistema de auth, troque os endpoints para usar Depends(get_current_user)
# e valide que a banca escolhida pertence ao fornecedor logado.

@router.post("/produtos", response_model=Produto, status_code=201)
def criar_produto(payload: Dict[str, Any]):
    """
    Cria um produto. Validações mínimas da HU-11 estão no serviço.
    Corpo esperado (exemplo):
    {
      "nome": "Tomate",
      "preco": 7.5,
      "banca": "Banca 01",
      "lat": -15.88,
      "long": -47.98,
      "categoria": "hortaliça",
      "avaliacao": 0.0
    }
    """
    try:
        produto = service.criar(payload)
        return produto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/produtos", response_model=List[Produto])
def listar_produtos():
    """Lista todos os produtos (visíveis)"""
    return service.listar()

@router.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = service.listar()
    for p in produtos:
        if p.id == produto_id:
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

@router.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, payload: Dict[str, Any]):
    produto = service.atualizar(produto_id, payload)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto

@router.patch("/produtos/{produto_id}/preco", response_model=Produto)
def alterar_preco(produto_id: int, payload: Dict[str, Any]):
    # espera {"preco": 6.0}
    novo_preco = payload.get("preco")
    if novo_preco is None or type(novo_preco) not in (int, float) or novo_preco < 0:
        raise HTTPException(status_code=400, detail="Preço inválido.")
    produto = service.atualizar(produto_id, {"preco": novo_preco})
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto

@router.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):
    ok = service.excluir(produto_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return {"status": "excluído"}

