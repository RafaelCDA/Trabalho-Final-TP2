"""
Ponto de entrada principal da aplicação.

Este módulo inicializa a instância FastAPI, define informações gerais da API
e integra o conjunto de rotas disponibilizado no pacote `api`. A aplicação
resultante fornece suporte às funcionalidades essenciais do sistema,
incluindo busca de produtos, gerenciamento de fornecedores e interações com
usuários, conforme definido nos requisitos funcionais.
"""
from src.models.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router as api_router
from src.core.database import Base, engine

# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# Instância principal
app = FastAPI(
    title="Sistema de Compras em Feiras",
    description=(
        "API responsável por operações de consulta, cadastro e interação "
        "entre usuários, fornecedores e administradores."
    ),
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas da aplicação
app.include_router(api_router)