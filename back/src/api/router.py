"""
Módulo responsável por centralizar e expor todos os endpoints da aplicação.
"""
from fastapi import APIRouter
from .endpoints import health, auth, users, banca
from .services.produto_busca_service import ProdutoBuscaService
from ..models.produto_model import BuscaRequest, BuscaResponse

# HU-11 — cadastro, edição, listagem e exclusão de produtos
from .endpoints import produto

# ======================================================
# Router principal da API
# ======================================================

router = APIRouter()

# Registrar health
router.include_router(health.router, tags=["Health"])
router.include_router(auth.router, tags=["Auth"])
router.include_router(users.router, tags=["Users"])
router.include_router(banca.router, tags=["Bancas"])

# Registrar produtos (HU-11)
router.include_router(produto.router, tags=["Produtos"])

# ======================================================
# Router específico para busca de produtos (HU-01 e HU-02)
# ======================================================

busca_router = APIRouter()
busca_service = ProdutoBuscaService()


@busca_router.post("/buscar", response_model=BuscaResponse)
async def buscar_produtos(busca: BuscaRequest):
    """
    HU-01 e HU-02: Busca e ordenação de produtos.
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
        total=len(resultados_ordenados),
        termo_buscado=busca.termo
    )


# Registrar o router de busca
router.include_router(busca_router, tags=["Busca"])

