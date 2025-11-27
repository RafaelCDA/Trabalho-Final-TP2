"""
Módulo responsável por centralizar e expor todos os endpoints da aplicação.
"""

from fastapi import APIRouter
from .endpoints import health, auth, users

# Router principal da API
router = APIRouter()

# Registro dos endpoints disponíveis
router.include_router(health.router, tags=["Health"])
router.include_router(auth.router, tags=["Auth"])
router.include_router(users.router, tags=["Users"])
