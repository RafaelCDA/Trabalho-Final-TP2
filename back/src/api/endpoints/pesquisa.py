from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.services.pesquisa_service import PesquisaService
from src.dto.pesquisa_dto import SearchResponse


router = APIRouter(prefix="/pesquisa", tags=["Pesquisa"])


# ============================================================
#  DEPENDÊNCIAS
# ============================================================


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_pesquisa_service(db: Session = Depends(get_db)) -> PesquisaService:
    return PesquisaService(db)


# ============================================================
#  ENDPOINT DE BUSCA
# ============================================================


@router.get(
    "/",
    response_model=SearchResponse,
    summary="Realizar busca avançada",
    description=(
        "Executa uma busca por produtos e/ou bancas com filtros opcionais "
        "de preço, distância, localização e ordenação."
        "\n\n"
        "**Filtros disponíveis:**\n"
        "- `tipo`: produto | banca | all\n"
        "- `preco_max`: filtra produtos com preço ≤ valor informado\n"
        "- `distancia_max_metros`: filtra itens próximos à localização informada\n"
        "- `lat_user`, `lon_user`: localização do usuário para registrar a pesquisa\n"
        "- `lat_ref`, `lon_ref`: localização alternativa para cálculo de distância\n"
        "- `order_by`: preco | distancia\n"
    ),
)
def pesquisar(
    termo: str = Query(..., description="Termo a ser pesquisado (ex: tomate)"),
    tipo: str = Query(
        ...,
        regex="^(produto|banca|all)$",
        description="Tipo da busca: produto, banca ou all",
    ),
    preco_max: float | None = Query(
        None, description="Preço máximo permitido (para produtos)"
    ),
    distancia_max_metros: float | None = Query(
        None,
        description="Distância máxima em metros (para proximidade)",
    ),
    order_by: str | None = Query(
        None,
        regex="^(preco|distancia)$",
        description="Critério de ordenação: preco ou distancia",
    ),
    lat_user: float | None = Query(
        None, description="Latitude do usuário (para registrar a pesquisa)"
    ),
    lon_user: float | None = Query(
        None, description="Longitude do usuário (para registrar a pesquisa)"
    ),
    lat_ref: float | None = Query(
        None, description="Latitude alternativa para cálculo de distância"
    ),
    lon_ref: float | None = Query(
        None, description="Longitude alternativa para cálculo de distância"
    ),
    service: PesquisaService = Depends(get_pesquisa_service),
):
    """
    Endpoint principal de busca.
    """

    try:
        return service.buscar(
            termo=termo,
            tipo=tipo,
            lat_user=lat_user,
            lon_user=lon_user,
            preco_max=preco_max,
            distancia_max_metros=distancia_max_metros,
            order_by=order_by,
            lat_ref=lat_ref,
            lon_ref=lon_ref,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
