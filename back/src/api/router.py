"""
Módulo responsável por centralizar e expor todos os endpoints da aplicação.
"""

from fastapi import APIRouter
from .services.produto_busca_service import ProdutoBuscaService
from ..models.produto_model import ProdutoModel
from .endpoints import health

# Router principal da API
router = APIRouter()

# Registro dos endpoints disponíveis
router.include_router(health.router, tags=["Health"])

busca_service = ProdutoBuscaService()
@router.post("/buscar", response_model=BuscaResponse)
async def buscar_produtos(busca: BuscaRequest):
    """
    HU-01 e HU-02: Busca e ordenação de produtos
    """
    resultados = busca_service.buscar_produtos(
        busca.termo, 
        busca.usuario_lat, 
        busca.usuario_long
    )
    
    resultados_ordenados = busca_service.ordenar_produtos(
        resultados, 
        busca.criterio_ordenacao,
        busca.usuario_lat,
        busca.usuario_long
    )
    
    return BuscaResponse(
        resultados=resultados_ordenados,
        total=len(resultados_ordenados)
    )

@router.get("/produtos")
async def listar_produtos():
    """Lista todos os produtos (para teste)"""
    return busca_service.buscar_produtos("", 0, 0)
