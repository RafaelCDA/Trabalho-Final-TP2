"""
Módulo responsável por centralizar e expor todos os endpoints da aplicação.
"""

from fastapi import APIRouter
from .endpoints import health

# Router principal da API
router = APIRouter()

# Registro dos endpoints disponíveis
router.include_router(health.router, tags=["Health"])
