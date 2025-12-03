"""
Módulo responsável por centralizar e expor todos os endpoints da aplicação.
"""

from fastapi import APIRouter
from .services.produto_busca_service import ProdutoBuscaService
from ..models.produto_model import BuscaRequest, BuscaResponse
from .endpoints import health
from back.src.api.endpoints import messages
from .endpoints import health, auth, users, banca, produto, pesquisa

# Router principal da API
router = APIRouter()

# Registro dos endpoints disponíveis
router.include_router(health.router, tags=["Health"])
router.include_router(auth.router, tags=["Auth"])
router.include_router(users.router, tags=["Users"])
router.include_router(banca.router, tags=["bancas"])
router.include_router(produto.router, tags=["produtos"])
router.include_router(pesquisa.router, tags=["Pesquisa"])
router.include_router(messages.router, tags=["Chat"])