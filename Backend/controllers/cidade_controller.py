from fastapi import APIRouter, HTTPException, Query
from services.cidade_service import CidadeService
from schemas.cidade_schema import (
    CidadeDetalheResponse,
    ComparacaoCidadesResponse,
    CidadesBuscaListResponse
)

router = APIRouter(prefix="/api/cidades", tags=["Cidades"])

@router.get("/buscar", response_model=CidadesBuscaListResponse)
def buscar_cidades(
    nome: str = Query(..., min_length=2, description="Nome da cidade para buscar (mínimo 2 caracteres)"),
    limite: int = Query(20, ge=1, le=50, description="Limite de resultados")
):
    """Busca cidades pelo nome (busca parcial, case-insensitive)."""
    resultado = CidadeService.buscar_cidades_por_nome(nome, limite)
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=resultado["error"])
    return resultado

@router.get("/{codigo_ibge}", response_model=CidadeDetalheResponse)
def obter_detalhes_cidade(codigo_ibge: str):
    resultado = CidadeService.obter_historico_e_detalhes(codigo_ibge)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

@router.get("/comparar/{codigo_1}/{codigo_2}", response_model=ComparacaoCidadesResponse)
def comparar_duas_cidades(codigo_1: str, codigo_2: str):
    resultado = CidadeService.comparar_cidades(codigo_1, codigo_2)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado