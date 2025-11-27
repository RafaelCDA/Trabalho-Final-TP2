"""
Endpoint responsável por fornecer informações de saúde da aplicação.

Este módulo contém rotas utilizadas em monitoramento, verificação de
disponibilidade e integração com serviços de observabilidade.
"""

from fastapi import APIRouter
from datetime import datetime, UTC

router = APIRouter()


@router.get(
    "/health",
    summary="Verifica o estado da aplicação",
    description=(
        "Retorna informações objetivas sobre o estado atual da aplicação, "
        "incluindo timestamp e versão disponibilizada."
    ),
)
def health_check():
    """
    Executa uma verificação simples do estado da aplicação.

    Este endpoint é utilizado para rotinas de monitoramento, validação de
    disponibilidade e confirmação de funcionamento do serviço.

    **Retorno**
    - `status`: indica se a aplicação está operante.
    - `timestamp`: data e hora da verificação.
    - `version`: versão atual disponibilizada.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
        "version": "1.0.0",
    }
