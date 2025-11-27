"""
Ponto de entrada principal da aplicação.

Este módulo inicializa a instância FastAPI, define informações gerais da API
e integra o conjunto de rotas disponibilizado no pacote `api`. A aplicação
resultante fornece suporte às funcionalidades essenciais do sistema,
incluindo busca de produtos, gerenciamento de fornecedores e interações com
usuários, conforme definido nos requisitos funcionais.
"""

from fastapi import FastAPI
from src.api.router import router as api_router
from api.services.produto_busca_service import ProdutoBuscaService 

# Instância principal da aplicação
app = FastAPI(
    title="Sistema de Compras em Feiras",
    description=(
        "API responsável por operações de consulta, cadastro e interação "
        "entre usuários, fornecedores e administradores."
    ),
    version="1.0.0",
)

# Registro das rotas da aplicação
app.include_router(router)

