from fastapi import APIRouter, HTTPException
from services.estado_service import EstadoService
from schemas.estado_schema import Top10EstadoResponse

router = APIRouter(prefix="/api/estados", tags=["Estados"])

# Rota direta do Top 10 da Bahia (Padrão)
@router.get("/ba/top10", response_model=Top10EstadoResponse)
@router.get("/{uf}/top10", response_model=Top10EstadoResponse)
def obter_top10_por_estado(uf: str = "ba"):

    # Retorna as Top 10 cidades mais populosas da Bahia por padrão
    # Se o usuário fornecer um estado diferente, ele retornará as Top 10 cidades mais populosas desse estado.
    
    resultado = EstadoService.obter_top10_cidades(uf)
    
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
        
    return resultado